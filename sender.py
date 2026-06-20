import urllib.request
import json
import time
import os

# PAMIĘTAJ O UKOŚNIKU NA KOŃCU!
API_URL = "https://kr0pa.pl/api/receive/"

# Ścieżka do czujnika (podmontowana w Dockerze)
TEMP_PATH = "/hostfs/sys/class/thermal/thermal_zone0/temp"

def get_temp():
    try:
        with open(TEMP_PATH, "r") as f:
            return float(f.read().strip()) / 1000.0
    except Exception:
        return 0.0

if __name__ == "__main__":
    print("Agent Docker wystartowal na RPi 3 B+...")
    
    while True:
        payload = {
            "temperature_c": get_temp()
        }
        
        # 1. Pakujemy dane do formatu JSON i zamieniamy na bajty
        json_data = json.dumps(payload).encode('utf-8')
        
        # 2. Tworzymy obiekt zapytania z jawną metodą POST i danymi
        req = urllib.request.Request(API_URL, data=json_data, method='POST')
        
        # 3. Dodajemy nagłówki (Typ danych + Nasze przebranie dla Cloudflare)
        req.add_header('Content-Type', 'application/json')
        req.add_header('User-Agent', 'IoT-Edge-Agent/1.0')
        
        # 4. Wysyłamy paczkę
        try:
            response = urllib.request.urlopen(req, timeout=5)
            print(f"Pomyslnie wyslano: {payload['temperature_c']}°C")
        except Exception as e:
            print(f"Blad sieci: {e}")
            
        # Czekamy 5 sekund przed kolejnym strzałem
        time.sleep(5)
