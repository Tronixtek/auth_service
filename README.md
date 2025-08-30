
# Django Authentication Service

A simple authentication system using **Django + DRF**, with:
- PostgreSQL as the database
- JWT for authentication
- Redis for password reset tokens
- Swagger API docs

## Docker Desktop Setup

1. **Install Docker Desktop**
	 - Download and install from https://www.docker.com/products/docker-desktop/

2. **Clone the repository**
	 - `git clone <your-repo-url>`
	 - `cd auth_service`

3. **Build and start the containers**
	 - Open Docker Desktop and ensure it is running.
	 - In your project folder, run:
		 ```powershell
		 docker-compose up --build
		 ```

4. **Apply migrations**
	 - In a new terminal, run:
		 ```powershell
		 docker-compose exec web python manage.py migrate
		 ```

5. **Create a superuser (admin login)**
	 - Run:
		 ```powershell
		 docker-compose exec web python manage.py createsuperuser
		 ```

6. **Access the app**
	 - Django server: [http://localhost:8000](http://localhost:8000)
	 - Admin panel: [http://localhost:8000/admin/](http://localhost:8000/admin/)
	 - Swagger docs: `/api/docs/` (if enabled)

## API Endpoints
- `POST /api/auth/register/` — Register a new user
- `POST /api/auth/login/` — Login and get JWT tokens
- `POST /api/auth/refresh/` — Refresh JWT access token
- `POST /api/auth/forgot-password/` — Request password reset
- `POST /api/auth/reset-password/` — Reset password with token

## Example Request Bodies

**Register:**
```json
{
	"email": "user@example.com",
	"full_name": "User Name",
	"password": "YourPassword123"
}
```

**Login:**
```json
{
	"email": "user@example.com",
	"password": "YourPassword123"
}
```

**Token Refresh:**
```json
{
	"refresh": "<your_refresh_token>"
}
```

**Forgot Password:**
```json
{
	"email": "user@example.com"
}
```

**Reset Password:**
```json
{
	"token": "<reset_token_from_forgot_password>",
	"password": "NewPassword123"
}
```

## Stopping the Project
To stop all containers:
```powershell
docker-compose down
```

## Notes
- All backend endpoints are tested using Postman or similar tools.
- No frontend is included; you can build one separately if needed.
