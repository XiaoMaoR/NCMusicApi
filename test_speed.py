import requests
import time
from concurrent.futures import ThreadPoolExecutor

url = "http://127.0.0.1/api-main"
num_requests = 500
timeout = 5
response_times = []

def fetch_song_info(id):
    payload = {
        "api": "song.main",
        "data": {"ids": str(id)},  # 模拟不同 ID
        "proxy": "",
        "realIP": "",
        "cookie": {}
    }
    start_time = time.time()
    try:
        response = requests.post(url, json=payload, timeout=timeout)
        response.raise_for_status()
        elapsed_time = time.time() - start_time
        response_times.append(elapsed_time)
        print(f"ID: {id}, 响应时间: {elapsed_time:.4f} 秒")
    except requests.RequestException as e:
        print(f"ID: {id}, 请求失败: {e}")

with ThreadPoolExecutor(max_workers=50) as executor:
    executor.map(fetch_song_info, range(1, num_requests + 1))

avg_time = sum(response_times) / len(response_times)
min_time = min(response_times)
max_time = max(response_times)

print(f"\n统计信息：")
print(f"平均响应时间: {avg_time:.4f} 秒")
print(f"最小响应时间: {min_time:.4f} 秒")
print(f"最大响应时间: {max_time:.4f} 秒")