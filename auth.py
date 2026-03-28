"""
Authentication system for AI Timetable Generator
Handles user registration, login, and session management
"""

import streamlit as st
import bcrypt
import json
import os
from datetime import datetime
from typing import Optional, Dict, Any

class AuthManager:
    def __init__(self, users_file: str = "users.json"):
        self.users_file = users_file
        self._ensure_users_file()
    
    def _ensure_users_file(self):
        """Create users file if it doesn't exist"""
        if not os.path.exists(self.users_file):
            with open(self.users_file, 'w') as f:
                json.dump({}, f)
    
    def _load_users(self) -> Dict[str, Any]:
        """Load users from JSON file"""
        try:
            with open(self.users_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}
    
    def _save_users(self, users: Dict[str, Any]):
        """Save users to JSON file"""
        with open(self.users_file, 'w') as f:
            json.dump(users, f, indent=2)
    
    def hash_password(self, password: str) -> str:
        """Hash password using bcrypt"""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def verify_password(self, password: str, hashed: str) -> bool:
        """Verify password against hash"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    
    def register_user(self, username: str, email: str, password: str) -> tuple[bool, str]:
        """Register a new user"""
        users = self._load_users()
        
        # Check if username already exists
        if username in users:
            return False, "Username already exists"
        
        # Check if email already exists
        for user_data in users.values():
            if user_data.get('email') == email:
                return False, "Email already registered"
        
        # Validate inputs
        if len(username) < 3:
            return False, "Username must be at least 3 characters"
        
        if len(password) < 6:
            return False, "Password must be at least 6 characters"
        
        if '@' not in email:
            return False, "Invalid email format"
        
        # Create user
        users[username] = {
            'email': email,
            'password': self.hash_password(password),
            'created_at': datetime.now().isoformat(),
            'last_login': None,
            'history': [],
            'preferences': {}
        }
        
        self._save_users(users)
        return True, "Registration successful"
    
    def login_user(self, username: str, password: str) -> tuple[bool, str]:
        """Login user"""
        users = self._load_users()
        
        if username not in users:
            return False, "Invalid username or password"
        
        user = users[username]
        
        if not self.verify_password(password, user['password']):
            return False, "Invalid username or password"
        
        # Update last login
        users[username]['last_login'] = datetime.now().isoformat()
        self._save_users(users)
        
        return True, "Login successful"
    
    def get_user(self, username: str) -> Optional[Dict[str, Any]]:
        """Get user data"""
        users = self._load_users()
        return users.get(username)
    
    def update_user_history(self, username: str, history_entry: Dict[str, Any]):
        """Add entry to user history"""
        users = self._load_users()
        
        if username in users:
            if 'history' not in users[username]:
                users[username]['history'] = []
            
            history_entry['timestamp'] = datetime.now().isoformat()
            users[username]['history'].append(history_entry)
            
            # Keep only last 100 entries
            users[username]['history'] = users[username]['history'][-100:]
            
            self._save_users(users)
    
    def get_user_history(self, username: str) -> list:
        """Get user history"""
        users = self._load_users()
        
        if username in users:
            return users[username].get('history', [])
        
        return []
    
    def update_user_preferences(self, username: str, preferences: Dict[str, Any]):
        """Update user preferences"""
        users = self._load_users()
        
        if username in users:
            users[username]['preferences'] = preferences
            self._save_users(users)
    
    def get_user_preferences(self, username: str) -> Dict[str, Any]:
        """Get user preferences"""
        users = self._load_users()
        
        if username in users:
            return users[username].get('preferences', {})
        
        return {}

def render_login_page(auth_manager: AuthManager) -> Optional[str]:
    """Render login/register page"""
    st.markdown("""
    <style>
    .auth-container {
        max-width: 400px;
        margin: 0 auto;
        padding: 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.3);
    }
    .auth-title {
        color: white;
        text-align: center;
        font-size: 2rem;
        margin-bottom: 1.5rem;
        font-weight: bold;
    }
    .auth-subtitle {
        color: rgba(255,255,255,0.8);
        text-align: center;
        margin-bottom: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="auth-container">', unsafe_allow_html=True)
    st.markdown('<div class="auth-title">📅 AI Timetable Generator</div>', unsafe_allow_html=True)
    st.markdown('<div class="auth-subtitle">Your intelligent productivity companion</div>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["🔐 Login", "📝 Register"])
    
    with tab1:
        st.markdown("### Welcome Back!")
        login_username = st.text_input("Username", key="login_username")
        login_password = st.text_input("Password", type="password", key="login_password")
        
        if st.button("Login", use_container_width=True, type="primary"):
            if login_username and login_password:
                success, message = auth_manager.login_user(login_username, login_password)
                if success:
                    st.session_state['authenticated'] = True
                    st.session_state['username'] = login_username
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)
            else:
                st.warning("Please fill in all fields")
    
    with tab2:
        st.markdown("### Create Account")
        reg_username = st.text_input("Username", key="reg_username")
        reg_email = st.text_input("Email", key="reg_email")
        reg_password = st.text_input("Password", type="password", key="reg_password")
        reg_confirm = st.text_input("Confirm Password", type="password", key="reg_confirm")
        
        if st.button("Register", use_container_width=True, type="primary"):
            if reg_username and reg_email and reg_password and reg_confirm:
                if reg_password != reg_confirm:
                    st.error("Passwords do not match")
                else:
                    success, message = auth_manager.register_user(reg_username, reg_email, reg_password)
                    if success:
                        st.success(message)
                        st.info("Please login with your new account")
                    else:
                        st.error(message)
            else:
                st.warning("Please fill in all fields")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    return None

def check_authentication() -> bool:
    """Check if user is authenticated"""
    return st.session_state.get('authenticated', False)

def get_current_user() -> Optional[str]:
    """Get current logged in username"""
    return st.session_state.get('username')

def logout():
    """Logout current user"""
    st.session_state['authenticated'] = False
    st.session_state['username'] = None
    st.rerun()
