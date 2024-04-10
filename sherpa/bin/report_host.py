import sys
import os

import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

import requests
import psutil
import logging


def encrypt_byte(input_bytes, key_base64):
    key = base64.b64decode(key_base64)
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(input_bytes) + padder.finalize()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    return ciphertext


def from_json_to_base64(json_str, key_base64):
    try:
        json_bytes = json_str.encode('utf-8')
        encrypted_bytes = encrypt_byte(json_bytes, key_base64)
        data_base64 = base64.b64encode(encrypted_bytes).decode('utf-8')
        return data_base64
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def get_cpu_usage():
    return psutil.cpu_percent()


def get_memory_info():
    mem = psutil.virtual_memory()
    total_mem_gb = round(mem.total / (1024.0 ** 3), 1)
    available_mem_gb = round(mem.available / (1024.0 ** 3), 1)
    used_mem_gb = round(mem.used / (1024.0 ** 3), 1)
    return total_mem_gb, available_mem_gb, used_mem_gb


def get_public_ip():
    try:
        response = requests.get('http://ifconfig.me')
        response.raise_for_status()
        return response.text.strip()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching IP address: {e}")
        return None


def get_host_info(now, sample_rate, language, port, session_count, session_limit, public_ip):
    physical_cores = psutil.cpu_count(logical=False)
    cpu_usage = get_cpu_usage()
    if public_ip is None:
        public_ip = get_public_ip()
    total_mem, available_mem, used_mem = get_memory_info()
    pid = os.getpid()
    formatted_time = now.strftime('%Y/%m/%d-%H:%M:%S')

    data = {
        "cpuCount": physical_cores,
        "cpuUsage": cpu_usage,
        "ipOut": public_ip,
        "memLeftG": available_mem,
        "memTotalG": total_mem,
        "memUsedG": used_mem,
        "modelSource": "SELF_BUILT",
        "modelType": "ASR",
        "paramMap": {"sample_rate": sample_rate, "lang": language},
        "port": port,
        "priority": 1,
        "processId": pid,
        "sessionCount": session_count,
        "sessionLimit": session_limit,
        "currentDate": formatted_time
    }
    return data


def send_host_report(data_base64, host_info):
    url = 'http://dn-ai-model-admin.tzwebpre.com:8080/ai-model-admin/config/report-host'

    headers = {
        'Content-Type': 'application/json',
        'synCode': data_base64,
    }

    response = requests.post(url, headers=headers, json=host_info)
    if response.status_code == 200:
        logging.info(f"request success!: {response.json()}")
    else:
        logging.info(f"request fail! code：{response.status_code}, text:{response.text}")
        print(f"request fail! code：{response.status_code}")
        print(response.text)


def main(argv):
    print("test begin")
    json_str = get_json_str()
    data_base64 = from_json_to_base64(json_str, "iMuSfa346s3JLJXjH1DSyQ==")
    print(f"data_base64: {data_base64}")
    host_info = get_host_info("16000", "en", 9002, 2, 10)
    print(f"host_info:{host_info}")
    send_host_report(data_base64, host_info)
    print("test end")


if __name__ == "__main__":
    main(sys.argv[1:])
