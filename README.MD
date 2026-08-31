# Clientra – Flask CRM Application

Clientra is a web application built with Python and Flask that serves as a simple CRM system for managing clients, services, and appointments. The application includes user authentication, CRUD operations, MySQL database integration, form validation, RESTful routes, and a custom JSON API.

---

## Technologies

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
- External API integration (Open-Meteo Weather API)

---

## Project Structure

```text
Clientra/
│
├── app/
│   ├── __init__.py      # Application factory and extension initialization
│   ├── models/          # SQLAlchemy models (User, Client, Service, Appointment)
│   ├── routes/          # Flask Blueprints (CRUD, authentication, API)
│   ├── forms/           # Flask-WTF forms and validation
│   ├── templates/       # Jinja2 HTML templates
│   ├── static/          # CSS and static files
│   └── utils/           # Helper functions (e.g. email)
│
├── migrations/          # Flask-Migrate database migrations
├── requirements.txt     # Python dependencies
├── config.py            # Application configuration
├── app.py               # Application entry point
└── README.md            # Project documentation
```

> Environment variables and sensitive configuration are stored locally in a `.env` file and are not included in the repository.

---

## Features

### Authentication

- User registration
- Login and logout
- Protected routes using `@login_required`
- Each user can access only their own data

### CRUD Operations

**Clients**
- Create, edit and delete clients
- Search functionality
- CSV export

**Services**
- Create, edit and delete services
- Search functionality
- CSV export

**Appointments**
- Create, edit and delete appointments
- Appointment status management

### Database

- MySQL database
- SQLAlchemy ORM
- Relationships between database tables using foreign keys
- Data integrity protection — clients or services cannot be deleted if related appointments exist

### Forms and Validation

- Server-side validation using WTForms
- Client-side HTML validation
- CSRF protection
- Validation error messages displayed in templates

### Dashboard

- Total number of clients, services and appointments
- Number of appointments scheduled for the current day
- Upcoming appointments
- Total revenue
- Revenue and working hours for the current month

### External API Integration

- Current weather data retrieved using the Open-Meteo API

---

## RESTful Routing

Routes follow REST-oriented principles using resources and HTTP methods.

Examples:

```text
GET  /clients
POST /clients/new
POST /clients/<id>/delete
GET  /appointments
```

---

## JSON API

The application includes a custom read-only JSON API.

### `GET /api/appointments`

Returns appointment data in JSON format with filtering support.

### `GET /api/summary`

Returns aggregated data such as:

- Number of records
- Revenue
- Working hours

The API is protected by Flask-Login and returns only data belonging to the currently authenticated user.

---

## Running the Application

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure environment variables

Create a local `.env` file:

```env
SECRET_KEY=your_secret_key
DATABASE_URL=mysql+pymysql://user:password@localhost/clientra
```

### 3. Run the application

```bash
python app.py
```

The application will be available locally at:

```text
http://127.0.0.1:5000
```

---

## About the Project

Clientra was developed as part of my Computer Science studies. The project provided practical experience with Flask application architecture, relational databases, authentication and authorization, CRUD operations, REST APIs, form validation, and external API integration.

## Author

**Luka Mikac**  
Computer Science Student
