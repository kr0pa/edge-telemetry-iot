# 🌐 Edge-to-Cloud IoT Telemetry System

Profesjonalny system telemetryczny oparty na architekturze rozproszonej (Edge Computing & Cloud). Projekt służy do monitorowania temperatury procesora urządzenia brzegowego (Raspberry Pi 4) w czasie rzeczywistym. Wykorzystuje sprawdzony stos technologiczny, obejmujący konteneryzację, automatyzację rurociągów CI/CD oraz reaktywny frontend.

## 🛠️ Stos Technologiczny

| Architektura | Technologie | Rola w systemie |
| :--- | :--- | :--- |
| **Edge & DevOps** | Docker, GitHub Actions, Terraform | Konteneryzacja agenta IoT, automatyczne budowanie obrazów (multi-arch dla ARM/x86), kodowanie infrastruktury (IaC). |
| **Cloud Backend** | Python, Django, Linode | Odbiór danych telemetrycznych i serwowanie bezstanowego API REST. Przechowywanie danych w postaci szeregów czasowych (Time-Series). |
| **Frontend UI** | HTMX, Alpine.js, Tailwind CSS, ApexCharts | Asynchroniczna komunikacja z serwerem, responsywny interfejs oraz płynna animacja wykresów na podstawie zrzutów JSON. |

## 🚀 Główne Funkcjonalności

- Lekki agent IoT w Pythonie odczytujący parametry sprzętowe bezpośrednio z systemu plików hosta.
- Zautomatyzowany rurociąg CI/CD budujący i publikujący obrazy w rejestrze Docker Hub.
- Bezstanowy endpoint API w chmurze przyjmujący surowe ładunki JSON z urządzeń brzegowych.
- Reaktywny interfejs użytkownika odpytujący serwer asynchronicznie (mechanizm pollingu) i aktualizujący stan DOM bez przeładowywania strony.

## 🏗️ Przepływ Danych (Data Flow)

1. Kontener Docker na Raspberry Pi odczytuje temperaturę z udostępnionego wolumenu systemowego.
2. Agent brzegowy wykonuje żądanie HTTP POST z obiektem JSON do serwera Django hostowanego w chmurze Linode.
3. Serwer waliduje dane i trwale zapisuje je w bazie danych z odpowiednim znacznikiem czasu.
4. Przeglądarka klienta cyklicznie pobiera nową paczkę danych wykorzystując deklaratywne zapytania HTMX.
5. Alpine.js przechwytuje zdarzenie mutacji drzewa DOM i wyzwala ponowne renderowanie wykresów ApexCharts.

## ⚙️ Wdrożenie (Węzeł Brzegowy)

Aby uruchomić agenta telemetrycznego na dowolnym urządzeniu z systemem Linux i środowiskiem Docker, wykonaj poniższe polecenie:

```bash
docker run -d \
  --name iot-agent \
  --restart unless-stopped \
  -v /:/hostfs:ro \
  -v /proc:/hostfs/proc:ro \
  -v /sys:/hostfs/sys:ro \
  kr0pa/edge-telemetry:latest
```

> Uwaga: Flaga podmontowania wolumenu (-v /:/hostfs:ro) jest krytyczna dla prawidłowego działania kontenera. Gwarantuje ona bezpieczny dostęp w trybie "read-only" do plików systemowych hosta w celu sprzętowego odczytu parametrów procesora.
