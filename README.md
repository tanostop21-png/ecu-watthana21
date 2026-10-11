# ECU-Watthana21 - Vehicle ECU Remapping Tool

## Overview

ECU-Watthana21 is a comprehensive vehicle ECU (Engine Control Unit) and transmission remapping tool that allows users to optimize their vehicle's performance through precise calibration adjustments.

### Features

✅ **User Management**
- User registration and authentication
- JWT-based secure login
- User profile management
- Admin dashboard access

✅ **Vehicle Management**
- Register and manage multiple vehicles
- Track vehicle specifications (make, model, year, VIN, etc.)
- Store engine and transmission information
- Current profile tracking

✅ **ECU Remapping**
- Create custom remapping profiles
- Performance levels: Stock, Eco, Standard, Sport, Extreme
- Precise ECU parameter adjustment
- Transmission settings configuration
- Expected performance gains tracking

✅ **Tuning Sessions**
- Create and track tuning sessions
- Session progress monitoring
- Before/after performance measurements
- Session history and status tracking

✅ **Calibration Logging**
- Automatic logging of all parameter changes
- Change history with timestamps
- Success/failure tracking
- Detailed change descriptions

✅ **Admin Dashboard**
- System statistics and overview
- User management
- Vehicle monitoring
- Session tracking
- Calibration log review

✅ **Desktop Application**
- PyQt6-based desktop GUI
- Real-time API communication
- Vehicle and profile management
- Session monitoring
- Calibration log viewing

✅ **REST API**
- Complete API endpoints for all operations
- JWT token-based authentication
- Role-based access control
- Comprehensive error handling

## Technology Stack

- **Backend**: Flask, Flask-SQLAlchemy, Flask-JWT-Extended
- **Database**: PostgreSQL (configurable)
- **Desktop GUI**: PyQt6
- **Authentication**: JWT (JSON Web Tokens)
- **Security**: Bcrypt password hashing
- **API Documentation**: RESTful endpoints

## Project Structure

```
ecu-watthana21/
├── api/
│   ├── routes/
│   │   ├── auth_routes.py           # Authentication endpoints
│   │   ├── vehicle_routes.py        # Vehicle management
│   │   ├── profile_routes.py        # Remapping profiles
│   │   ├── calibration_routes.py    # Calibration logs
│   │   ├── session_routes.py        # Tuning sessions
│   │   ├── dashboard_routes.py      # Admin dashboard
│   │   └── __init__.py
│   └── __init__.py                  # Flask app factory
├── core/
│   ├── ecu_controller.py            # ECU operations
│   ├── transmission_controller.py   # Transmission operations
│   └── __init__.py
├── models/
│   ├── user.py                      # User model
│   ├── vehicle.py                   # Vehicle model
│   ├── remapping_profile.py         # Profile model
│   ├── calibration_log.py           # Calibration log model
│   ├── tuning_session.py            # Tuning session model
│   └── __init__.py
├── desktop/
│   ├── app.py                       # Desktop application
│   └── __init__.py
├── utils/
│   ├── validators.py                # Data validation
│   ├── logger.py                    # Logging setup
│   └── __init__.py
├── docs/
│   ├── API.md                       # API documentation
│   └── README_TH.md                 # Thai documentation
├── config.py                        # Configuration
├── database.py                      # Database initialization
├── run_server.py                    # Start API server
├── run_desktop.py                   # Start desktop app
├── init_db.py                       # Initialize database
├── requirements.txt                 # Python dependencies
├── .env.example                     # Environment variables example
└── README.md                        # This file
```

## Quick Start

### 1. Prerequisites

- Python 3.8+
- PostgreSQL (optional, can use SQLite)
- pip (Python package manager)

### 2. Installation

```bash
# Clone the repository
git clone https://github.com/tanostop21-png/ecu-watthana21.git
cd ecu-watthana21

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Edit .env with your settings (optional)
# nano .env
```

### 3. Database Setup

```bash
# Initialize database with demo data
python init_db.py
```

This will:
- Create all database tables
- Create admin user: `admin` / `admin123456`
- Create demo user: `demo` / `demo123456`
- Add demo vehicle and remapping profiles

### 4. Running the API Server

```bash
# Start the Flask API server
python run_server.py
```

The API will be available at `http://localhost:5000/api/v1`

### 5. Running the Desktop Application

In a new terminal:

```bash
# Make sure virtual environment is activated
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Start desktop application
python run_desktop.py
```

## API Usage

### Authentication

**Register:**
```bash
curl -X POST http://localhost:5000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "newuser",
    "email": "user@example.com",
    "password": "password123456"
  }'
```

**Login:**
```bash
curl -X POST http://localhost:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "demo",
    "password": "demo123456"
  }'
```

Response:
```json
{
  "status": "success",
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 2,
    "username": "demo",
    "email": "demo@ecu-watthana.com",
    "first_name": "Demo",
    "last_name": "User"
  }
}
```

### Vehicle Management

**List Vehicles:**
```bash
curl -X GET http://localhost:5000/api/v1/vehicle \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Register Vehicle:**
```bash
curl -X POST http://localhost:5000/api/v1/vehicle/register \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "vehicle_id": "VEH_2024_001",
    "make": "BMW",
    "model": "M340i",
    "year": 2024,
    "engine_type": "petrol",
    "transmission_type": "automatic",
    "vin": "WBADT43452G915633",
    "license_plate": "BMW-5678",
    "engine_displacement": 3000,
    "horsepower": 382,
    "torque": 500
  }'
```

### Remapping Profiles

**List Profiles:**
```bash
curl -X GET http://localhost:5000/api/v1/profile/vehicle/1 \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Create Profile:**
```bash
curl -X POST http://localhost:5000/api/v1/profile \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "vehicle_id": 1,
    "profile_name": "Custom Sport",
    "description": "Custom sport tuning profile",
    "performance_level": "sport",
    "ecu_parameters": {
      "fuel_injection_timing": 65,
      "ignition_timing": 22,
      "boost_pressure": 1.3
    },
    "expected_power_gain": 35,
    "expected_torque_gain": 60
  }'
```

### Admin Dashboard

**Dashboard Statistics:**
```bash
curl -X GET http://localhost:5000/api/v1/dashboard/stats \
  -H "Authorization: Bearer ADMIN_TOKEN"
```

**List All Users:**
```bash
curl -X GET http://localhost:5000/api/v1/dashboard/users \
  -H "Authorization: Bearer ADMIN_TOKEN"
```

**List All Vehicles:**
```bash
curl -X GET http://localhost:5000/api/v1/dashboard/vehicles \
  -H "Authorization: Bearer ADMIN_TOKEN"
```

**List All Sessions:**
```bash
curl -X GET http://localhost:5000/api/v1/dashboard/sessions \
  -H "Authorization: Bearer ADMIN_TOKEN"
```

## Configuration

Edit `.env` file to configure:

```bash
# Application Settings
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key-change-this

# Database
# SQLite
DATABASE_URL=sqlite:///ecu_watthana.db
# PostgreSQL
# DATABASE_URL=postgresql://user:password@localhost/ecu_watthana

# JWT Settings
JWT_SECRET_KEY=your-jwt-secret-key-change-this
JWT_ACCESS_TOKEN_EXPIRES=3600

# Server Settings
API_HOST=0.0.0.0
API_PORT=5000

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/app.log
```

## Database Switching

### Use SQLite (Default)
```bash
DATABASE_URL=sqlite:///ecu_watthana.db
```

### Use PostgreSQL

1. Install PostgreSQL
2. Create database:
```bash
createdb ecu_watthana
```

3. Update `.env`:
```bash
DATABASE_URL=postgresql://username:password@localhost/ecu_watthana
```

4. Install psycopg2:
```bash
pip install psycopg2-binary
```

## Development

### Adding New API Routes

1. Create route file in `api/routes/`
2. Define Blueprint and endpoints
3. Register blueprint in `api/__init__.py`

### Adding New Database Models

1. Create model in `models/`
2. Define SQLAlchemy model class
3. Import in `models/__init__.py`
4. Run `python init_db.py` to recreate tables

### Desktop App Development

The desktop app uses PyQt6. To extend:

1. Edit `desktop/app.py`
2. Add new tabs/dialogs
3. Implement API calls using `APIClient`

## Testing

```bash
# Run tests
pytest tests/

# Run with coverage
pytest --cov=. tests/
```

## Production Deployment

### Prerequisites

- PostgreSQL database
- Python 3.8+
- Gunicorn or similar WSGI server
- Nginx or Apache for reverse proxy

### Steps

1. Set `FLASK_ENV=production` in `.env`
2. Update `SECRET_KEY` and `JWT_SECRET_KEY`
3. Configure PostgreSQL connection
4. Install production dependencies:
```bash
pip install gunicorn
```

5. Run with Gunicorn:
```bash
gunicorn -w 4 -b 0.0.0.0:5000 "api:create_app()"
```

6. Set up Nginx reverse proxy
7. Configure SSL/TLS certificates

## Troubleshooting

### Port Already in Use
```bash
# Change API_PORT in .env to different port
API_PORT=5001
```

### Database Connection Error
```bash
# Check DATABASE_URL in .env
# For PostgreSQL, ensure database exists and user has access
# For SQLite, ensure write permissions in project directory
```

### Desktop App Connection Failed
```bash
# Ensure API server is running
# Check API_HOST and API_PORT match in desktop app
# Check firewall settings
```

## Contributing

1. Fork repository
2. Create feature branch: `git checkout -b feature/your-feature`
3. Make changes with tests
4. Commit changes: `git commit -am 'Add feature'`
5. Push to branch: `git push origin feature/your-feature`
6. Submit pull request

## License

MIT License - See LICENSE file for details

## Support

For issues, questions, or suggestions:
- Create GitHub issue
- Email: support@ecu-watthana.com

## Changelog

### Version 1.0.0 (2024)
- Initial MVP release
- User authentication and registration
- Vehicle management
- ECU remapping profiles
- Tuning sessions
- Calibration logging
- Admin dashboard
- Desktop application
- REST API

## Roadmap

- [ ] Mobile app (iOS/Android)
- [ ] Advanced diagnostics
- [ ] Real-time ECU communication
- [ ] Performance graphs and analytics
- [ ] Backup/restore functionality
- [ ] Multi-language support
- [ ] Cloud synchronization
- [ ] Community profiles sharing

---

**ECU-Watthana21** - Professional Vehicle ECU Remapping Tool

*Optimize your vehicle's performance with precision*
