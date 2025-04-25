#  Ticket Booking System

A web-based ticket booking system for managing shows, seat selections, and user bookings. Built with Django, Dockerized for easy deployment, and integrated with Jenkins for CI/CD automation.

---

##  Project Overview

This application allows users to:
- Register and log in to their account
- View available shows and details
- Select showtimes and reserve seats
- Manage their bookings
- Admins can manage shows, showtimes, and bookings from a custom admin panel

---

## 🛠️ Tech Stack Used

- **Backend**: Django (Python)
- **Frontend**: HTML, CSS (Bootstrap)
- **Database**: PostgreSQL
- **Containerization**: Docker, Docker Compose
- **CI/CD**: Jenkins
- **Authentication**: Django’s built-in auth system
- **Others**: Gunicorn (for production), Whitenoise (for static files)

---

## ⚙️ Setup & Run Instructions

### 🔧 Prerequisites
- Docker
- Docker Compose
- Git

### 🚀 Quickstart

```bash
# Clone the repository
[git clone https://github.com/](https://github.com/aquaticmr/ticketbooking.git)
cd ticket_booking_system

# Build and run the containers
docker-compose up --build


# Access the app
Visit http://localhost:8000
```

# 🐳 Running Without Docker
## Create virtual environment
```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

## Install dependencies
pip install -r requirements.txt

## Run migrations
python manage.py migrate

## Create superuser
python manage.py createsuperuser

## Run the server
python manage.py runserver

```

# 📸 Screenshots
![Screenshot 2025-04-25 204626](https://github.com/user-attachments/assets/2ea1c11b-6be9-4b58-8517-5cde23f2e632)
![Screenshot 2025-04-25 211206](https://github.com/user-attachments/assets/aed01ce3-b640-44d0-9747-5ec5ada93479)
![Screenshot 2025-04-25 212553](https://github.com/user-attachments/assets/917107be-9d16-4d90-b4b5-8ecfa4cc4936)
![a1f56d38-95a4-4db0-83e7-f18ec308b16e](https://github.com/user-attachments/assets/7cb01039-2cf0-43b7-b1d1-db4a0c73130f)
![WhatsApp Image 2025-04-25 at 8 54 05 PM](https://github.com/user-attachments/assets/8df409a3-d277-49ab-a071-3b9aefbfb5fa)
![Screenshot 2025-04-25 212553](https://github.com/user-attachments/assets/917107be-9d16-4d90-b4b5-8ecfa4cc4936)




# 🐳 Docker Usage
Dockerfile and docker-compose.yml are configured to:

Run the Django app with Gunicorn

Use a separate PostgreSQL container

Automatically collect static files

To restart the service:

docker-compose down
docker-compose up --build

# ⚙️ Jenkins Usage
Jenkinsfile included for automating the build and test process.

Example stages:

Pull latest code

Build Docker image

Run tests

Deploy to Docker container

Ensure Jenkins is set up to trigger on push to the repository and Docker is installed on the Jenkins host.

# 📂 Project Structure
```

ticket_booking_system/
├── bookings/              
├── shows/                 
├── users/                 
├── admin_panel/           
├── templates/             
├── static/                
├── ticket_booking/        
├── Dockerfile             
├── docker-compose.yml     
├── Jenkinsfile            
├── requirements.txt       
└── manage.py

```

