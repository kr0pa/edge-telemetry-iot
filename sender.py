import time
import os
import requests

API_URL = "https://kropa.pl/api/receive/"  # Twój endpoint w Django

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
        
        payload = {
            "device_id": "raspberry-pi-edge",
            "cpu_temp": temp
        }
        
        try:
            response = requests.post(API_URL, json=payload, timeout=5)
            print(f"Wysłano dane: Temperatura CPU: {temp}°C | Status API: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Problem z połączeniem z API: {e}")
            
        time.sleep(10)

if __name__ == "__main__":
    main()
