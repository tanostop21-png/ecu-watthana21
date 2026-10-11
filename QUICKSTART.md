# ECU-Watthana21 Quick Start Guide

## Installation (Linux/Mac)

### 1. Automatic Installation

```bash
bash install.sh
```

This script will:
- Check Python version
- Create virtual environment
- Install all dependencies
- Initialize database with demo data
- Create .env configuration file

### 2. Manual Installation

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Initialize database
python init_db.py
```

## Installation (Windows)

### 1. Automatic Installation

Double-click `install.bat`

Or run in Command Prompt:
```batch
install.bat
```

### 2. Manual Installation

```batch
# Create virtual environment
python -m venv venv
venv\Scripts\activate.bat

# Install dependencies
pip install -r requirements.txt

# Copy environment file
copy .env.example .env

# Initialize database
python init_db.py
```

## Running the Application

### Terminal 1: Start API Server

```bash
# Linux/Mac
source venv/bin/activate
python run_server.py

# Windows
venv\Scripts\activate.bat
python run_server.py
```

Server will start at: `http://localhost:5000`

### Terminal 2: Start Desktop Application

```bash
# Linux/Mac
source venv/bin/activate
python run_desktop.py

# Windows
venv\Scripts\activate.bat
python run_desktop.py
```

## Demo Login

- **Admin Account:**
  - Username: `admin`
  - Password: `admin123456`
  - Role: Administrator (access to dashboard)

- **Demo Account:**
  - Username: `demo`
  - Password: `demo123456`
  - Role: Regular User

## Testing Installation

Run test script:

```bash
python test_installation.py
```

## API Testing

### Using cURL

**Login:**
```bash
curl -X POST http://localhost:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"demo","password":"demo123456"}'
```

**List Vehicles:**
```bash
curl -X GET http://localhost:5000/api/v1/vehicle \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Using Postman

1. Import API endpoints from `/docs/API.md`
2. Set up authentication with JWT token
3. Test endpoints

## Troubleshooting

### Port 5000 Already in Use

Edit `.env`:
```
API_PORT=5001
```

### Database Error

Reinitialize database:
```bash
rm ecu_watthana.db  # or delete file on Windows
python init_db.py
```

### PyQt6 Installation Issues

On Linux, you may need:
```bash
sudo apt-get install python3-pyqt6
```

Or try:
```bash
pip install --upgrade PyQt6
```

## Next Steps

1. **Create New User:** Register through desktop app or API
2. **Add Vehicle:** Register your vehicle details
3. **Create Profile:** Set up remapping profile
4. **Monitor Changes:** Track calibration logs
5. **Use Dashboard:** Access admin dashboard for statistics

## Documentation

- Full API documentation: `docs/API.md`
- Thai language guide: `docs/README_TH.md`
- Architecture details: `README.md`

## Support

For issues:
1. Check logs: `logs/app.log`
2. Verify installation: `python test_installation.py`
3. Review configuration: `.env` file
4. Check GitHub issues

## Development

To extend the application:

1. **Add API Endpoint:** Create new route file in `api/routes/`
2. **Add Database Model:** Create new model in `models/`
3. **Extend Desktop App:** Edit `desktop/app.py`
4. **Add Tests:** Create test files in `tests/`

## More Information

See `README.md` for complete documentation.
