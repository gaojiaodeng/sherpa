import sys
from pydub import AudioSegment


def main(argv):
    # 加载MP3文件
    audio_file = argv[0]
    audio = AudioSegment.from_file(audio_file)
    # 打印采样率
    print("Sample rate: ", audio.frame_rate)


if __name__ == "__main__":
    main(sys.argv[1:])

