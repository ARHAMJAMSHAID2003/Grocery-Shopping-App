# FreshMart — Grocery Shopping App 

A full-stack grocery shopping application built with **Django REST Framework** (backend) and **React Native + Expo** (frontend), featuring products, email OTP verification, and Cash on Delivery.

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Django 5.2, Django REST Framework, SimpleJWT |
| Frontend | React Native 0.81, Expo SDK 54, React Navigation |
| Database | MySQL 8.0 |
| Auth | JWT (access + refresh tokens), Email OTP verification |

## Features

- User registration with **email OTP verification** (Gmail SMTP)
- JWT-based authentication
- Product catalog with **15 categories** and **220+ products**
- Product search and category filtering
- Size/weight picker with price multipliers (Dairy, Beverages, Meat, etc.)
- Shopping cart with stock validation
- Order placement with automatic stock deduction
- Order history (user-specific)
- **Cash on Delivery** payment
- Responsive on web and mobile (iOS/Android via Expo Go)
- All prices in **PKR**

## Project Structure

```
├── api/                    # Django app (models, views, serializers, urls)
├── grocery_api/            # Django project settings
├── grocery-app/            # React Native / Expo frontend
│   ├── screens/            # LoginScreen, HomeScreen, CartScreen, etc.
│   ├── components/         # ProductCard
│   └── services/           # api.js (Axios config)
├── database_setup.sql      # Full MySQL dump (import to set up DB)
├── requirements.txt        # Python dependencies
├── manage.py               # Django management
├── *.csv                   # Raw dataset files

```

## Setup Instructions

### 1. Database

```bash
# Create the database and import the dump from database_setup.sql
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS grocery_db;"
mysql -u root -p grocery_db < database_setup.sql
```

### 2. Backend (Django)

```bash
# Create virtual environment
python -m venv grocery-api-env

# Activate it
# Windows:
.\grocery-api-env\Scripts\Activate.ps1
# macOS/Linux:
source grocery-api-env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Update grocery_api/settings.py with your MySQL password
# (look for DATABASES > PASSWORD)

# Update EMAIL_HOST_USER and EMAIL_HOST_PASSWORD in settings.py
# if using your own Gmail for OTP

# Run the server
python manage.py runserver 0.0.0.0:8000
```

### 3. Frontend (React Native / Expo)

```bash
cd grocery-app

# Install dependencies
npm install

# Update the IP address in services/api.js
# Set it to your machine's local IP for mobile testing

# Start Expo
npx expo start

# For mobile (iPhone/Android via Expo Go):
npx expo start --tunnel
```

### 4. Access

- **Web**: http://localhost:8000/api/ (API), http://localhost:8080 (Frontend)
- **Mobile**: Scan QR code from Expo with Expo Go app

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/register/` | Register new user |
| POST | `/api/login/` | Login (returns JWT) |
| POST | `/api/send-otp/` | Send OTP to email |
| POST | `/api/verify-otp/` | Verify OTP code |
| POST | `/api/resend-otp/` | Resend OTP |
| GET | `/api/products/` | List all products |
| GET/POST | `/api/cart/` | Cart operations |
| GET/POST | `/api/orders/` | Order operations |

## Screenshots

The app includes:
- Login page with grocery-themed hero section
- Product grid with category filters and search
- Product detail with size/weight picker
- Shopping cart with item management
- Order history




