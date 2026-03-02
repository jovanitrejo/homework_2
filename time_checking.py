import time
import requests

# IP addresses to test
ip_addresses = [
    "34.63.169.199",
    "35.205.122.149"
]

results = {}

# Test /register endpoint 10x for both IPs
for ip in ip_addresses:
    url = f"http://{ip}:8080/register"
    times = []
    
    for i in range(10):
        try:
            start = time.perf_counter()
            response = requests.post(url, json={"username": f"user_{i}"}, timeout=5)
            end = time.perf_counter()
            elapsed = (end - start) * 1000  # Convert to milliseconds
            times.append(elapsed)
            print(f"IP {ip} - /register Call {i+1}: {elapsed:.2f}ms")
        except Exception as e:
            print(f"IP {ip} - /register Call {i+1}: Error - {e}")
    
    if times:
        results[f"{ip}_register"] = {
            "times": times,
        }
    print()

# Test /list endpoint 10x for both IPs
for ip in ip_addresses:
    url = f"http://{ip}:8080/list"
    times = []
    
    for i in range(10):
        try:
            start = time.perf_counter()
            response = requests.get(url, timeout=5)
            end = time.perf_counter()
            elapsed = (end - start) * 1000  # Convert to milliseconds
            times.append(elapsed)
            print(f"IP {ip} - /list Call {i+1}: {elapsed:.2f}ms")
        except Exception as e:
            print(f"IP {ip} - /list Call {i+1}: Error - {e}")
    
    if times:
        results[f"{ip}_list"] = {
            "times": times,        }

# compute averages as a helper function  
def avg_ms(values):
    return sum(values) / len(values) if values else None

# Computes and display averages
print("\nAverage Latency Results")

for ip in ip_addresses:
    reg_key = f"{ip}_register"
    list_key = f"{ip}_list"

    reg_times = results.get(reg_key, {}).get("times", [])
    list_times = results.get(list_key, {}).get("times", [])

    reg_avg = avg_ms(reg_times)
    list_avg = avg_ms(list_times)

    region_label = "us-central1" if ip == ip_addresses[0] else "europe-west1"

    print(f"\nInstance ({region_label}) - IP: {ip}")

    if reg_avg:
        print(f"  /register: {len(reg_times)} samples | avg = {reg_avg:.2f} ms")

    if list_avg:
        print(f"  /list:     {len(list_times)} samples | avg = {list_avg:.2f} ms")
# Clearing
r = requests.post(f"http://{ip_addresses[0]}:8080/clear", timeout=10)
print(ip_addresses[0], r.status_code, r.text)