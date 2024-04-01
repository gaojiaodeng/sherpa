import sys
import os
import re
from datetime import datetime


def main(argv):
    # 日志文件所在目录
    log_directory = argv[0]

    # 关键字列表
    start_send = "Starting to send audio"
    start_recv = "received first word"
    end_send = "Sent Done Signal"
    end_recv = "Done!"

    # 正则表达式用于匹配时间戳
    timestamp_pattern = r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}.\d{3}'

    # 遍历目录中的所有文件
    for filename in os.listdir(log_directory):
        if filename.endswith('.log'):  # 确保是日志文件
            file_path = os.path.join(log_directory, filename)

            # 用于存储时间戳的字典，键为关键字，值为时间戳
            timestamps = {}

            # 读取日志文件并查找关键字的时间戳
            with open(file_path, 'r') as file:
                found_start_send = False
                found_start_recv = False
                found_end_send = False
                for line in file:
                    if not found_start_send:
                        if start_send in line:
                            # 查找时间戳
                            timestamp_match = re.search(timestamp_pattern, line)
                            if timestamp_match:
                                timestamps[start_send] = timestamp_match.group()
                                found_start_send = True
                    else:
                        if not found_start_recv:
                            if start_recv in line:
                                # 查找时间戳
                                timestamp_match = re.search(timestamp_pattern, line)
                                if timestamp_match:
                                    timestamps[start_recv] = timestamp_match.group()
                                    found_start_recv = True
                        else:
                            if not found_end_send:
                                if end_send in line:
                                    # 查找时间戳
                                    timestamp_match = re.search(timestamp_pattern, line)
                                    if timestamp_match:
                                        timestamps[end_send] = timestamp_match.group()
                                        found_end_send = True
                            else:
                                if end_recv in line:
                                    # 查找时间戳
                                    timestamp_match = re.search(timestamp_pattern, line)
                                    if timestamp_match:
                                        timestamps[end_recv] = timestamp_match.group()
                                        break  # 找到第二个关键字后跳出循环

            # 检查是否找到了所有关键字的时间戳
            if len(timestamps) == 4:
                # 将时间戳字符串转换为datetime对象
                datetime_start_send = datetime.strptime(timestamps[start_send], '%Y-%m-%d %H:%M:%S.%f')
                datetime_start_recv = datetime.strptime(timestamps[start_recv], '%Y-%m-%d %H:%M:%S.%f')
                datetime_end_send = datetime.strptime(timestamps[end_send], '%Y-%m-%d %H:%M:%S.%f')
                datetime_end_recv = datetime.strptime(timestamps[end_recv], '%Y-%m-%d %H:%M:%S.%f')

                # 计算时间差
                start_delay = datetime_start_recv - datetime_start_send
                end_delay = datetime_end_recv - datetime_end_send

                start_delay_miliseconds = start_delay.seconds * 1000 + start_delay.microseconds // 1000
                end_delay_miliseconds = end_delay.seconds * 1000 + end_delay.microseconds // 1000

                # 打印文件名和时间差
                print(
                    f"In file {filename}, start delay: {start_delay_miliseconds} ms, end delay: {end_delay_miliseconds} ms ")
            else:
                print(f"Not all keywords were found in file {filename}.")


if __name__ == "__main__":
    main(sys.argv[1:])
