"""
Desktop Application - ECU-Watthana21 Remapping Tool
"""
import sys
import json
from pathlib import Path
try:
    from PyQt6.QtWidgets import (
        QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
        QPushButton, QLabel, QLineEdit, QTabWidget, QTableWidget, QTableWidgetItem,
        QMessageBox, QComboBox, QSpinBox, QDoubleSpinBox, QFormLayout,
        QProgressBar, QTextEdit, QDialog, QInputDialog
    )
    from PyQt6.QtCore import Qt, QThread, pyqtSignal
    from PyQt6.QtGui import QFont, QColor
except ImportError:
    print("PyQt6 not installed. Install with: pip install PyQt6")
    sys.exit(1)

import requests
from datetime import datetime

class APIClient:
    """HTTP Client for API communication"""
    
    def __init__(self, base_url="http://localhost:5000/api/v1"):
        self.base_url = base_url
        self.token = None
        self.headers = {}
    
    def set_token(self, token):
        """Set JWT token"""
        self.token = token
        self.headers = {"Authorization": f"Bearer {token}"}
    
    def register(self, username, email, password, first_name="", last_name=""):
        """Register new user"""
        data = {
            "username": username,
            "email": email,
            "password": password,
            "first_name": first_name,
            "last_name": last_name
        }
        response = requests.post(f"{self.base_url}/auth/register", json=data)
        return response.json(), response.status_code
    
    def login(self, username, password):
        """Login user"""
        data = {"username": username, "password": password}
        response = requests.post(f"{self.base_url}/auth/login", json=data)
        return response.json(), response.status_code
    
    def get_profile(self):
        """Get user profile"""
        response = requests.get(f"{self.base_url}/auth/profile", headers=self.headers)
        return response.json(), response.status_code
    
    def list_vehicles(self):
        """List user's vehicles"""
        response = requests.get(f"{self.base_url}/vehicle", headers=self.headers)
        return response.json(), response.status_code
    
    def register_vehicle(self, vehicle_data):
        """Register new vehicle"""
        response = requests.post(f"{self.base_url}/vehicle/register", 
                                json=vehicle_data, headers=self.headers)
        return response.json(), response.status_code
    
    def list_profiles(self, vehicle_id):
        """List profiles for vehicle"""
        response = requests.get(f"{self.base_url}/profile/vehicle/{vehicle_id}", 
                               headers=self.headers)
        return response.json(), response.status_code
    
    def create_profile(self, vehicle_id, profile_data):
        """Create remapping profile"""
        profile_data['vehicle_id'] = vehicle_id
        response = requests.post(f"{self.base_url}/profile", 
                                json=profile_data, headers=self.headers)
        return response.json(), response.status_code
    
    def list_sessions(self, vehicle_id):
        """List tuning sessions"""
        response = requests.get(f"{self.base_url}/session/vehicle/{vehicle_id}", 
                               headers=self.headers)
        return response.json(), response.status_code
    
    def get_calibration_logs(self, vehicle_id):
        """Get calibration logs"""
        response = requests.get(f"{self.base_url}/calibration/vehicle/{vehicle_id}", 
                               headers=self.headers)
        return response.json(), response.status_code


class LoginDialog(QDialog):
    """Login Dialog"""
    
    def __init__(self, api_client):
        super().__init__()
        self.api_client = api_client
        self.user_data = None
        self.init_ui()
    
    def init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("ECU-Watthana21 Login")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        layout.addWidget(title)
        
        # Form
        form_layout = QFormLayout()
        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        
        form_layout.addRow("Username:", self.username_input)
        form_layout.addRow("Password:", self.password_input)
        layout.addLayout(form_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        login_btn = QPushButton("Login")
        register_btn = QPushButton("Register")
        
        login_btn.clicked.connect(self.login)
        register_btn.clicked.connect(self.open_register)
        
        button_layout.addWidget(login_btn)
        button_layout.addWidget(register_btn)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        self.setWindowTitle("ECU-Watthana21 Login")
    
    def login(self):
        """Handle login"""
        username = self.username_input.text()
        password = self.password_input.text()
        
        if not username or not password:
            QMessageBox.warning(self, "Error", "Please enter username and password")
            return
        
        response, status = self.api_client.login(username, password)
        
        if status == 200:
            self.api_client.set_token(response['access_token'])
            self.user_data = response['user']
            self.accept()
        else:
            QMessageBox.critical(self, "Login Failed", response.get('error', 'Unknown error'))
    
    def open_register(self):
        """Open register dialog"""
        # Simple register dialog
        username, ok = QInputDialog.getText(self, "Register", "Username:")
        if not ok:
            return
        
        email, ok = QInputDialog.getText(self, "Register", "Email:")
        if not ok:
            return
        
        password, ok = QInputDialog.getText(self, "Register", "Password:", 
                                           QLineEdit.EchoMode.Password)
        if not ok:
            return
        
        response, status = self.api_client.register(username, email, password)
        
        if status == 201:
            QMessageBox.information(self, "Success", "Registration successful. Please login.")
        else:
            QMessageBox.critical(self, "Registration Failed", 
                               response.get('error', 'Unknown error'))


class MainWindow(QMainWindow):
    """Main Application Window"""
    
    def __init__(self, api_client, user_data):
        super().__init__()
        self.api_client = api_client
        self.user_data = user_data
        self.current_vehicle = None
        self.init_ui()
        self.load_vehicles()
    
    def init_ui(self):
        """Initialize UI"""
        self.setWindowTitle(f"ECU-Watthana21 - {self.user_data['username']}")
        self.setGeometry(100, 100, 1200, 700)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Tabs
        tabs = QTabWidget()
        
        # Vehicle Tab
        self.vehicle_tab = self.create_vehicle_tab()
        tabs.addTab(self.vehicle_tab, "Vehicles")
        
        # Profile Tab
        self.profile_tab = self.create_profile_tab()
        tabs.addTab(self.profile_tab, "Profiles")
        
        # Session Tab
        self.session_tab = self.create_session_tab()
        tabs.addTab(self.session_tab, "Sessions")
        
        # Logs Tab
        self.logs_tab = self.create_logs_tab()
        tabs.addTab(self.logs_tab, "Calibration Logs")
        
        layout.addWidget(tabs)
        
        # Status bar
        self.statusBar().showMessage(f"Welcome, {self.user_data['first_name']} {self.user_data['last_name']}")
    
    def create_vehicle_tab(self):
        """Create vehicle management tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Table
        self.vehicle_table = QTableWidget()
        self.vehicle_table.setColumnCount(6)
        self.vehicle_table.setHorizontalHeaderLabels(
            ["Year", "Make", "Model", "VIN", "Engine Type", "Transmission"]
        )
        self.vehicle_table.itemSelectionChanged.connect(self.on_vehicle_selected)
        layout.addWidget(self.vehicle_table)
        
        # Buttons
        button_layout = QHBoxLayout()
        add_btn = QPushButton("Add Vehicle")
        refresh_btn = QPushButton("Refresh")
        
        add_btn.clicked.connect(self.add_vehicle)
        refresh_btn.clicked.connect(self.load_vehicles)
        
        button_layout.addWidget(add_btn)
        button_layout.addWidget(refresh_btn)
        layout.addLayout(button_layout)
        
        return widget
    
    def create_profile_tab(self):
        """Create profile management tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Table
        self.profile_table = QTableWidget()
        self.profile_table.setColumnCount(4)
        self.profile_table.setHorizontalHeaderLabels(
            ["Profile Name", "Level", "Power Gain", "Active"]
        )
        layout.addWidget(self.profile_table)
        
        # Buttons
        button_layout = QHBoxLayout()
        create_btn = QPushButton("Create Profile")
        refresh_btn = QPushButton("Refresh")
        
        create_btn.clicked.connect(self.create_profile)
        refresh_btn.clicked.connect(self.load_profiles)
        
        button_layout.addWidget(create_btn)
        button_layout.addWidget(refresh_btn)
        layout.addLayout(button_layout)
        
        return widget
    
    def create_session_tab(self):
        """Create session management tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Table
        self.session_table = QTableWidget()
        self.session_table.setColumnCount(5)
        self.session_table.setHorizontalHeaderLabels(
            ["Session Name", "Status", "Progress", "HP Gain", "Date"]
        )
        layout.addWidget(self.session_table)
        
        # Buttons
        button_layout = QHBoxLayout()
        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self.load_sessions)
        button_layout.addWidget(refresh_btn)
        layout.addLayout(button_layout)
        
        return widget
    
    def create_logs_tab(self):
        """Create calibration logs tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Table
        self.logs_table = QTableWidget()
        self.logs_table.setColumnCount(5)
        self.logs_table.setHorizontalHeaderLabels(
            ["Parameter", "Old Value", "New Value", "Type", "Status"]
        )
        layout.addWidget(self.logs_table)
        
        # Button
        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self.load_logs)
        layout.addWidget(refresh_btn)
        
        return widget
    
    def load_vehicles(self):
        """Load vehicles from API"""
        try:
            response, status = self.api_client.list_vehicles()
            if status == 200:
                self.vehicle_table.setRowCount(0)
                for i, vehicle in enumerate(response.get('vehicles', [])):
                    self.vehicle_table.insertRow(i)
                    self.vehicle_table.setItem(i, 0, QTableWidgetItem(str(vehicle['year'])))
                    self.vehicle_table.setItem(i, 1, QTableWidgetItem(vehicle['make']))
                    self.vehicle_table.setItem(i, 2, QTableWidgetItem(vehicle['model']))
                    self.vehicle_table.setItem(i, 3, QTableWidgetItem(vehicle['vin']))
                    self.vehicle_table.setItem(i, 4, QTableWidgetItem(vehicle['engine_type']))
                    self.vehicle_table.setItem(i, 5, QTableWidgetItem(vehicle['transmission_type']))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load vehicles: {str(e)}")
    
    def on_vehicle_selected(self):
        """Handle vehicle selection"""
        rows = self.vehicle_table.selectedIndexes()
        if rows:
            self.current_vehicle = rows[0].row()
            self.load_profiles()
            self.load_sessions()
            self.load_logs()
    
    def load_profiles(self):
        """Load profiles from API"""
        if not self.current_vehicle:
            return
        
        try:
            vehicle_id = self.vehicle_table.item(self.current_vehicle, 0).text()
            # Note: This would need actual vehicle ID from the response
            QMessageBox.information(self, "Info", "Profile loading would be implemented here")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load profiles: {str(e)}")
    
    def load_sessions(self):
        """Load sessions from API"""
        if not self.current_vehicle:
            return
        
        try:
            QMessageBox.information(self, "Info", "Session loading would be implemented here")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load sessions: {str(e)}")
    
    def load_logs(self):
        """Load calibration logs from API"""
        if not self.current_vehicle:
            return
        
        try:
            QMessageBox.information(self, "Info", "Log loading would be implemented here")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load logs: {str(e)}")
    
    def add_vehicle(self):
        """Add new vehicle"""
        QMessageBox.information(self, "Info", "Add vehicle form would be implemented here")
    
    def create_profile(self):
        """Create new profile"""
        QMessageBox.information(self, "Info", "Create profile form would be implemented here")


def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    
    # Create API client
    api_client = APIClient()
    
    # Show login dialog
    login_dialog = LoginDialog(api_client)
    if login_dialog.exec() == QDialog.DialogCode.Accepted:
        # Show main window
        main_window = MainWindow(api_client, login_dialog.user_data)
        main_window.show()
        sys.exit(app.exec())
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
