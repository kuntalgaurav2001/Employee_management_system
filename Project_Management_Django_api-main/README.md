# Employee Management System

A full-stack web application for managing employees, projects, finances, teams, meetings, and more. Built with Django (backend) and React (frontend).

---

## Table of Contents
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Setup Instructions](#setup-instructions)
  - [Backend (Django)](#backend-django)
  - [Frontend (React)](#frontend-react)
- [Deployment Guide](#deployment-guide)
  - [Deploying on Heroku](#deploying-on-heroku)
  - [Deploying on Render](#deploying-on-render)
- [Usage](#usage)
- [License](#license)

---

## Features
- Employee management (CRUD)
- Team and meeting scheduling
- Project and proposal tracking
- Financial management (income, expenses)
- User authentication and permissions
- Modern, responsive UI

---

## Tech Stack
- **Backend:** Django, Django REST Framework
- **Frontend:** React, Vite
- **Database:** SQLite (default), PostgreSQL (recommended for production)
- **Deployment:** Heroku, Render, or any VPS

---

## Project Structure
```
Employee_Management_system/
├── Project_Management_Django_api-main/   # Django backend
│   ├── app/                              # Core project management logic
│   ├── finances/                         # Financial management
│   ├── peoples/                          # Employee, teams, meetings
│   ├── project_management/               # Django settings
│   ├── manage.py                         # Django CLI
│   ├── requirements.txt                  # Python dependencies
│   └── ...
├── Project_Management_Django-main/       # React frontend
│   ├── src/                              # React source code
│   ├── public/                           # Static assets
│   ├── package.json                      # JS dependencies
│   └── ...
```

---

## Setup Instructions

### Backend (Django)
1. **Navigate to backend directory:**
   ```sh
   cd Project_Management_Django_api-main
   ```
2. **(Optional) Create and activate a virtual environment:**
   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```
3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
4. **Apply migrations:**
   ```sh
   python manage.py migrate
   ```
5. **Collect static files:**
   ```sh
   python manage.py collectstatic
   ```
6. **Create a superuser (admin):**
   ```sh
   python manage.py createsuperuser
   ```
7. **Run the development server:**
   ```sh
   python manage.py runserver
   ```

### Frontend (React)
1. **Navigate to frontend directory:**
   ```sh
   cd Project_Management_Django-main
   ```
2. **Install dependencies:**
   ```sh
   npm install
   ```
3. **Run the development server:**
   ```sh
   npm run dev
   ```
4. **Build for production:**
   ```sh
   npm run build
   ```
   The production build will be in the `dist/` folder.

---

## Deployment Guide

### Deploying on Heroku
1. **Install the Heroku CLI:** [Heroku CLI Install Guide](https://devcenter.heroku.com/articles/heroku-cli)
2. **Login to Heroku:**
   ```sh
   heroku login
   ```
3. **Create a Heroku app:**
   ```sh
   heroku create
   ```
4. **Add a PostgreSQL add-on (recommended):**
   ```sh
   heroku addons:create heroku-postgresql:hobby-dev
   ```
5. **Set environment variables (SECRET_KEY, DEBUG, etc.) in Heroku dashboard.**
6. **Push your code:**
   ```sh
   git push heroku main
   ```
7. **Run migrations on Heroku:**
   ```sh
   heroku run python manage.py migrate
   ```
8. **Collect static files on Heroku:**
   ```sh
   heroku run python manage.py collectstatic
   ```
9. **Deploy frontend:**
   - Option 1: Serve React build with Django (copy `dist/` to Django static directory)
   - Option 2: Deploy React separately on Vercel/Netlify

### Deploying on Render
1. **Create a new Web Service for Django backend.**
2. **Connect your GitHub repo.**
3. **Set build/start commands:**
   - Build: `pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput`
   - Start: `gunicorn project_management.wsgi`
4. **Set environment variables in Render dashboard.**
5. **Deploy frontend as a Static Site (optional) or serve with Django.**

---

## Usage
- Access the app at the deployed URL or `http://localhost:8000` (backend) and `http://localhost:5173` (frontend) in development.
- Log in with your superuser/admin account.
- Use the dashboard to manage employees, projects, finances, teams, and more.

---

## License
This project is for educational and demonstration purposes. Please check with the author for production/commercial use.
