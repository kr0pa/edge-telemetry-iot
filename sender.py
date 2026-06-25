import time
import os
import requests
import psutil

psutil.PROCFS_PATH = '/hostfs/proc'
API_URL = "https://kr0pa.pl/api/receive/"

def get_cpu_temperature():
    try:
        # Czytamy temperaturę z systemu przez podmontowany hostfs
        with open('/hostfs/sys/class/thermal/thermal_zone0/temp', 'r') as f:
            temp_raw = f.read()
        # Dzielimy przez 1000, aby uzyskać stopnie Celsjusza (np. 43.5)
        return round(float(temp_raw) / 1000.0, 1)
    except Exception as e:
        print(f"Błąd odczytu temperatury CPU: {e}")
        return 0.0

def main():
    print("Uruchomiono Agenta Telemetrii (Tylko Temperatura CPU)...")
    while True:
        temp = get_cpu_temperature()
        cpu_load = psutil.cpu_percent(interval=1)
        ram_usage = psutil.virtual_memory().percent

        payload = {
            "device_id": "raspberry-pi-edge",
            "cpu_temp": temp,
            "cpu_load": cpu_load,
            "ram_usage": ram_usage
        }

        try:
            response = requests.post(API_URL, json=payload, timeout=5)
            print(f"Wysłano dane: Temperatura CPU: {temp}°C | Obciążenie CPU: {cpu_load}% | Zużycie RAM: {ram_usage}% | Status API: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Problem z połączeniem z API: {e}")

        time.sleep(10)

if __name__ == "__main__":
    main()
