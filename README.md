# Geek Text API

## Project Overview
Geek Text is a RESTful backend API for an online bookstore focused on technology-related books.  
This project is developed for the **CEN 4010 – Software Engineering** course and follows the Scrum methodology.

The system provides REST endpoints that handle business logic and data persistence for the application.

---

## Architecture
- Backend: FastAPI (Python)
- Database: MySQL
- API Style: REST
- Data Format: JSON

---

### Project Structure

```text
Geek-Text-API/
├── app/
│   ├── main.py
│   ├── api/
│   │   └── routers/
│   ├── models/
│   ├── schemas/
│   └── services/
├── .gitignore
├── README.md
└── requirements.txt

```
---

## Running the Application
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
2. Start the server:
   uvicorn app.main:app --reload
3. The API will be available at:
   http://127.0.0.1:8000

---

## Notes
This is a backend-only project with no user interface.

Database credentials and environment variables are not committed to the repository.

This project is for academic purposes only
