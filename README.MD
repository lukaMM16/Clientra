# Clientra – Flask CRM aplikacija

Clientra je web aplikacija izrađena u Pythonu (Flask) koja služi kao jednostavni CRM sustav za upravljanje klijentima, uslugama i terminima. Aplikacija omogućuje autentikaciju korisnika, CRUD operacije, rad s bazom podataka (MySQL), validaciju formi, RESTful rute te vlastiti JSON API.

---

## Korištene tehnologije
- Python 3
- Flask
- Flask-SQLAlchemy
- Flask-WTF
- Flask-Login
- Flask-Migrate
- MySQL (PyMySQL)
- HTML / Jinja2
- CSS
- RESTful routing
- JSON API
- Vanjski API (Open-Meteo – weather)

---

## Struktura projekta

Clientra/
│
├── app/
│ ├── init.py # create_app(), inicijalizacija ekstenzija
│ ├── models/ # SQLAlchemy modeli (User, Client, Service, Appointment)
│ ├── routes/ # Flask blueprint rute (CRUD, auth, API)
│ ├── forms/ # Flask-WTF forme i validacija
│ ├── templates/ # Jinja2 HTML predlošci
│ ├── static/ # CSS i statičke datoteke
│ └── utils/ # Pomoćne funkcije (npr. email)
│
├── migrations/ # Flask-Migrate migracije baze
├── requirements.txt # Python ovisnosti
├── config.py # Konfiguracija aplikacije
├── .env # Varijable okruženja
├── app.py # Pokretanje aplikacije
└── README.md # Dokumentacija



---

## Funkcionalnosti aplikacije

### Autentikacija (Flask-Login)
- Registracija korisnika
- Prijava i odjava
- Zaštita ruta pomoću `@login_required`
- Svaki korisnik vidi isključivo svoje podatke

### CRUD operacije
- Klijenti – dodavanje, uređivanje, brisanje, pretraga, CSV export
- Usluge – dodavanje, uređivanje, brisanje, pretraga, CSV export
- Termini – dodavanje, uređivanje, brisanje, status termina

### Baza podataka
- MySQL baza podataka
- SQLAlchemy ORM
- Relacije između tablica (foreign keys)
- Očuvanje integriteta podataka (nije moguće obrisati klijenta/uslugu ako postoje termini)

### Flask-WTF forme i validacija
- Serverska validacija pomoću WTForms
- Klijentska validacija (HTML atributi)
- CSRF zaštita
- Prikaz validacijskih grešaka u templateima

### Dashboard
- Ukupan broj klijenata, usluga i termina
- Broj termina za današnji dan
- Nadolazeći termini
- Ukupni prihod
- Prihod i sati rada za tekući mjesec

### Vanjski API
- Dohvat trenutnog vremena pomoću Open-Meteo API-ja

---

## RESTful routing
Rute su imenovane prema REST principima (imenice + HTTP metode), npr.:
GET /clients
POST /clients/new
POST /clients/<id>/delete
GET /appointments


---

## JSON API (bonus funkcionalnost)

Aplikacija sadrži vlastiti read-only JSON API:

- `GET /api/appointments`  
  Vraća termine u JSON formatu uz mogućnost filtriranja

- `GET /api/summary`  
  Vraća agregirane podatke (broj zapisa, prihod, sati rada)

API je zaštićen Flask-Loginom i vraća samo podatke prijavljenog korisnika.

---

## Pokretanje aplikacije

### 1. Instalacija ovisnosti
U root direktoriju projekta pokrenuti:

```bash
pip install -r requirements.txt
2. Konfiguracija

Kreirati .env datoteku s primjerom:

SECRET_KEY=your_secret_key
DATABASE_URL=mysql+pymysql://user:password@localhost/clientra

3. Pokretanje aplikacije
python app.py


Aplikacija će biti dostupna na adresi:

http://127.0.0.1:5000