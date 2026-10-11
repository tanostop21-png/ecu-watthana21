"""
Database initialization and seeding
"""
import sys
from config import DevelopmentConfig
from api import create_app
from database import db
from models.user import User
from models.vehicle import Vehicle
from models.remapping_profile import RemappingProfile
from datetime import datetime

def init_db():
    """Initialize database and create tables"""
    app = create_app(DevelopmentConfig)
    
    with app.app_context():
        # Drop all tables
        print("Dropping tables...")
        db.drop_all()
        
        # Create all tables
        print("Creating tables...")
        db.create_all()
        
        # Create admin user
        print("Creating admin user...")
        admin = User(
            username='admin',
            email='admin@ecu-watthana.com',
            first_name='Admin',
            last_name='User',
            is_admin=True
        )
        admin.set_password('admin123456')
        db.session.add(admin)
        
        # Create demo user
        print("Creating demo user...")
        user = User(
            username='demo',
            email='demo@ecu-watthana.com',
            first_name='Demo',
            last_name='User'
        )
        user.set_password('demo123456')
        db.session.add(user)
        
        db.session.commit()
        
        # Create demo vehicle
        print("Creating demo vehicle...")
        vehicle = Vehicle(
            user_id=user.id,
            vehicle_id='VEH_2023_001',
            make='Toyota',
            model='Camry',
            year=2023,
            engine_type='petrol',
            transmission_type='automatic',
            vin='JTEBLP5C5M5003000',
            license_plate='ABC-1234',
            engine_displacement=2000,
            horsepower=180,
            torque=350
        )
        db.session.add(vehicle)
        db.session.commit()
        
        # Create demo profiles
        print("Creating demo profiles...")
        profiles_data = [
            {
                'profile_name': 'Stock',
                'description': 'Original factory settings',
                'performance_level': 'stock',
                'ecu_parameters': {
                    'fuel_injection_timing': 50,
                    'ignition_timing': 15,
                    'boost_pressure': 0.5
                },
                'expected_power_gain': 0,
                'expected_torque_gain': 0,
                'fuel_consumption_change': 0
            },
            {
                'profile_name': 'Eco',
                'description': 'Optimized for fuel efficiency',
                'performance_level': 'eco',
                'ecu_parameters': {
                    'fuel_injection_timing': 45,
                    'ignition_timing': 12,
                    'boost_pressure': 0.3
                },
                'expected_power_gain': -5,
                'expected_torque_gain': -10,
                'fuel_consumption_change': -15
            },
            {
                'profile_name': 'Sport',
                'description': 'Enhanced performance',
                'performance_level': 'sport',
                'ecu_parameters': {
                    'fuel_injection_timing': 60,
                    'ignition_timing': 20,
                    'boost_pressure': 1.2
                },
                'expected_power_gain': 30,
                'expected_torque_gain': 50,
                'fuel_consumption_change': 15
            }
        ]
        
        for profile_data in profiles_data:
            profile = RemappingProfile(
                vehicle_id=vehicle.id,
                profile_id=f"PROF_{profile_data['profile_name'].upper()}_001",
                profile_name=profile_data['profile_name'],
                description=profile_data['description'],
                performance_level=profile_data['performance_level'],
                ecu_parameters=profile_data['ecu_parameters'],
                expected_power_gain=profile_data['expected_power_gain'],
                expected_torque_gain=profile_data['expected_torque_gain'],
                fuel_consumption_change=profile_data['fuel_consumption_change'],
                is_default=(profile_data['performance_level'] == 'stock')
            )
            db.session.add(profile)
        
        db.session.commit()
        
        print("\n" + "="*50)
        print("Database initialized successfully!")
        print("="*50)
        print("\nDemo Credentials:")
        print("  Username: admin")
        print("  Password: admin123456")
        print("  Email: admin@ecu-watthana.com")
        print("\n  Username: demo")
        print("  Password: demo123456")
        print("  Email: demo@ecu-watthana.com")
        print("="*50)

if __name__ == '__main__':
    init_db()
