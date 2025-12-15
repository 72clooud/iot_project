![Angular](https://img.shields.io/badge/Angular-19.1.4-dd0031?style=for-the-badge&logo=angular)
![TypeScript](https://img.shields.io/badge/TypeScript-5.x-blue?style=for-the-badge&logo=typescript)
![RxJS](https://img.shields.io/badge/RxJS-7.x-B7178C?style=for-the-badge&logo=reactivex)
Kompleksowa aplikacja monitorująca stan jakości powietrza w Polsce w czasie rzeczywistym. System integruje symulowane czujniki IoT, chmurę Azure oraz nowoczesny frontend w Angularze, aby wizualizować dane o zanieczyszczeniach (PM2.5, CO, NO2, O3 i inne).

Strona główna po wejściu do aplikacji
<img width="1917" height="871" alt="image" src="https://github.com/user-attachments/assets/22089b3e-19b8-48e6-88d2-213fb77c0258" />
Pole wyszukiwania miejscowości , użytkownik może wyszukac miasto lub recznie wybrac je na mapie
<img width="1918" height="877" alt="image" src="https://github.com/user-attachments/assets/f826ed8a-c7ac-4324-bb9a-889563dd15c7" />
Panel po wybraniu miescowości 
<img width="1918" height="877" alt="image" src="https://github.com/user-attachments/assets/7f8df32a-e3b4-4949-8d7b-d0599a11c695" />
<img width="370" height="854" alt="image" src="https://github.com/user-attachments/assets/2aaed685-0f1f-409c-a0b1-0e9a5d1eb079" />
Architektura Systemu
Projekt składa się z dwóch głównych warstw. Dane przepływają od symulatorów IoT, przez chmurę, aż do interfejsu użytkownika.

1. Backend & Cloud 
Symulator IoT: Skrypt Python pobierający dane z OpenWeatherMap API i symulujący urządzenia IoT.

Azure IoT Hub & Cosmos DB: Dane trafiają do huba, a następnie wyzwalacz (trigger) zapisuje je w bazie NoSQL Cosmos DB.

FastAPI: Backend wystawia punkty końcowe REST, serwując przetworzone dane historyczne i bieżące do frontendu.

2. Frontend 
Aplikacja typu SPA (Single Page Application) napisana w Angularze (Standalone Components), odpowiedzialna za wizualizację danych i interakcję z użytkownikiem.

Kluczowe funkcjonalności Frontendowe:

Interaktywna Mapa (Leaflet): Implementacja mapy OpenStreetMap z obsługą zdarzeń (kliknięcia, nawigacja).

Geocoding & Wyszukiwanie: Integracja z API Nominatim do wyszukiwania miast i automatycznego centrowania mapy (flyTo).

Wizualizacja Danych (PrimeNG): Prezentacja wskaźników jakości powietrza w wysuwanym panelu bocznym (Drawer).

Logika Biznesowa UI: Dynamiczne obliczanie statusu AQI (kolory, opisy, paski postępu) po stronie klienta.

Schemat przepływu danych w naszej aplikacji
<img width="475" height="570" alt="image" src="https://github.com/user-attachments/assets/0da3f9b7-0954-4830-935f-9059d854e4a7" />


Szczegóły działania aplikacji
System składa się z dwóch niezależnych modułów backendowych. Pierwszy to skrypt symulujący urządzenia IoT, który pobiera i przetwarza dane z API, a następnie wysyła je do Azure IoT Hub. Stamtąd, za pomocą automatycznego wyzwalacza (triggera) w chmurze, dane trafiają do bazy Cosmos DB. Drugi moduł to właściwy backend napisany w FastAPI, który służy do udostępniania tych danych aplikacji frontendowej. Backend oparty na FastAPI wystawia punkty końcowe (endpoints), oczekując na zapytania REST ze strony frontendu, aby zwrócić odpowiednie dane zgromadzone wcześniej w bazie. Frontend napisany w Angularze oraz wykorzystujący komponenty PrimeNG pokazuje użytkownikowi mapę Polski, gdzie może wybrać dowolny punkt z mapy lub wpisać wybraną miejscowość.
Po kliknięciu przez użytkownika wybranego punktu na mapie serwis w Angularze przyjmuje długość i szerokość geograficzną i odpytuje backend. Python odbiera te informacje i sprawdza w bazie danych, gdzie znajduje się najbliższy czujnik powietrza. Pobiera informacje już przygotowane w Azure i wysyła je do frontendu.
Użytkownikowi otwiera się boczne menu ze wszystkimi informacjami na temat stanu jakości powietrza oraz miasto, dokładne współrzędne miejsca, które chciał sprawdzić, datę i godzinę ostatniego pomiaru oraz szczegółowe informacje na temat jakości powietrza (PM2.5, CO, NO2, O3, SO2, NH3, UV Index), w tym ogólny jego stan oparty na wskaźniku AQI, przedstawiony jako progressBar dla jasnego przedstawienia informacji.

Technologie
Frontend:

Angular 17+ (Standalone Components, Signals, Reactive Forms)

PrimeNG (Drawer, Button, ProgressBar, AutoComplete)

Leaflet.js (Mapy)

RxJS (Obsługa asynchroniczności)

SCSS (Stylowanie)

Backend & Dane:

Python (FastAPI)

Azure IoT Hub

Azure Cosmos DB

OpenWeatherMap API (Źródło danych)

Jak uruchomić (Frontend)
Sklonuj repozytorium:
git clone: https://github.com/72Clooud/IoT_project
Zainstaluj zależności:npm install
Uruchom serwer deweloperski:ng serve
Autorzy
Filip Porzucek
Filip Makuch

Uwaga dotycząca uruchomienia (Backend & Cloud)
Projekt wykorzystuje architekturę hybrydową opartą o usługi chmurowe Microsoft Azure (IoT Hub, Cosmos DB). Ze względów bezpieczeństwa, klucze dostępowe do chmury nie są publicznie dostępne w tym repozytorium.


