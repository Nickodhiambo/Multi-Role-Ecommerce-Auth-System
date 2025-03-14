# Multi-Role User Authentication API

This project is a Django Rest Framework (DRF) API that supports a multi-role user authentication system for an e-commerce platform. The API allows customers and vendors to sign up via dedicated endpoints and log in through a common endpoint that directs users to their respective dashboards based on their role. The system ensures robust security through JSON Web Tokens (JWT) and One-Time Passwords (OTP) during sign-up.

## Features

### Authentication
- **Role-Based Sign-Up**: Separate endpoints for customers and vendors.
- **Unified Login Endpoint**: Single login endpoint for all users, with role-based redirection to either the vendor or customer dashboard.
- **JWT Security**: Secure user authentication with access and refresh tokens.
- **OTP Verification**: Email-based OTP for secure account verification upon sign-up.

### Database
- **SQLite**: Lightweight database used for development and testing.

### Scalability
- Modular and extensible design to support additional roles or features in the future.

## Endpoints

### Authentication
1. `POST /accounts/api/signup/customer/`
    - Registers a new customer.
    - Requires: `username`, `email`, `password`, and `role=customer`
    - Add can add other customer-specific details.

2. `POST /accounts/api/auth/signup/vendor/`
    - Registers a new vendor.
    - Requires: `username`, `email`, `password`, `role=vendor`
    - You can add other vendor-specific details like business name.

3. `POST accounts/api/login/`
    - Logs in users and directs them to their respective dashboards based on role.
    - Requires: `email` and `password`.

4. `POST /api/verify-email/`
    - Verifies the OTP sent to the user's email during sign-up.
    - Requires: `email` and `otp`.

5. `POST /accounts/api/logout/`
    - Logs out a user.

6. `POST /accounts/api/check-user/`
    - Checks if a user exists in the database
    - Requires `email`

### Dashboards
- Vendor and customer dashboards (accessible after successful login).

## Security Measures
- Passwords are hashed using Django's `make_password` utility.
- OTPs are generated and verified for secure account activation.
- JWT ensures secure and stateless user sessions.

## Technologies Used
- **Django**: Web framework for building the API.
- **Django Rest Framework (DRF)**: Toolkit for building REST APIs.
- **SQLite**: Database for development and testing.
- **JWT**: For secure user authentication.

## Setup Instructions

### Prerequisites
- Python 3.8+
- Django 4.0+

### Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/Nickodhiambo/Multi-Role-Ecommerce-Auth-System.git
    ```

2. Create a virtual environment and activate it:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Apply migrations:
    ```bash
    python manage.py migrate
    ```

5. Run the server:
    ```bash
    python manage.py runserver
    ```

6. Test the endpoints using tools like Postman or curl.

## Testing
- Write and run test cases for each endpoint using Django's test framework.
- Example command to run tests:
    ```bash
    python manage.py test
    ```

## Future Enhancements
- Integrate social authentication (e.g., Google, Facebook).
- Use a more robust database like PostgreSQL for production.
- Add support for additional user roles.
- Enhance OTP mechanism to include SMS verification.

---

