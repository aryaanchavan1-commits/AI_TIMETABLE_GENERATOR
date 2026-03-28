"""
Database module for AI Timetable Generator
Handles user history, timetables, and chat storage
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional
import uuid

class DatabaseManager:
    def __init__(self, db_file: str = "database.json"):
        self.db_file = db_file
        self._ensure_db_file()
    
    def _ensure_db_file(self):
        """Create database file if it doesn't exist"""
        if not os.path.exists(self.db_file):
            initial_data = {
                'users': {},
                'timetables': {},
                'chat_history': {},
                'tasks': {}
            }
            with open(self.db_file, 'w') as f:
                json.dump(initial_data, f, indent=2)
    
    def _load_db(self) -> Dict[str, Any]:
        """Load database from JSON file"""
        try:
            with open(self.db_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {
                'users': {},
                'timetables': {},
                'chat_history': {},
                'tasks': {}
            }
    
    def _save_db(self, data: Dict[str, Any]):
        """Save database to JSON file"""
        with open(self.db_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    # User Management
    def save_user_data(self, username: str, user_data: Dict[str, Any]):
        """Save user data"""
        db = self._load_db()
        db['users'][username] = user_data
        self._save_db(db)
    
    def get_user_data(self, username: str) -> Optional[Dict[str, Any]]:
        """Get user data"""
        db = self._load_db()
        return db['users'].get(username)
    
    # Timetable Management
    def save_timetable(self, username: str, timetable: Dict[str, Any]) -> str:
        """Save a timetable and return its ID"""
        db = self._load_db()
        
        timetable_id = str(uuid.uuid4())
        timetable['id'] = timetable_id
        timetable['username'] = username
        timetable['created_at'] = datetime.now().isoformat()
        timetable['updated_at'] = datetime.now().isoformat()
        
        if username not in db['timetables']:
            db['timetables'][username] = {}
        
        db['timetables'][username][timetable_id] = timetable
        self._save_db(db)
        
        return timetable_id
    
    def get_timetable(self, username: str, timetable_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific timetable"""
        db = self._load_db()
        
        if username in db['timetables']:
            return db['timetables'][username].get(timetable_id)
        
        return None
    
    def get_user_timetables(self, username: str) -> List[Dict[str, Any]]:
        """Get all timetables for a user"""
        db = self._load_db()
        
        if username in db['timetables']:
            return list(db['timetables'][username].values())
        
        return []
    
    def update_timetable(self, username: str, timetable_id: str, updates: Dict[str, Any]) -> bool:
        """Update a timetable"""
        db = self._load_db()
        
        if username in db['timetables'] and timetable_id in db['timetables'][username]:
            db['timetables'][username][timetable_id].update(updates)
            db['timetables'][username][timetable_id]['updated_at'] = datetime.now().isoformat()
            self._save_db(db)
            return True
        
        return False
    
    def delete_timetable(self, username: str, timetable_id: str) -> bool:
        """Delete a timetable"""
        db = self._load_db()
        
        if username in db['timetables'] and timetable_id in db['timetables'][username]:
            del db['timetables'][username][timetable_id]
            self._save_db(db)
            return True
        
        return False
    
    # Chat History Management
    def save_chat_message(self, username: str, message: Dict[str, Any]):
        """Save a chat message"""
        db = self._load_db()
        
        if username not in db['chat_history']:
            db['chat_history'][username] = []
        
        message['id'] = str(uuid.uuid4())
        message['timestamp'] = datetime.now().isoformat()
        
        db['chat_history'][username].append(message)
        
        # Keep only last 500 messages
        db['chat_history'][username] = db['chat_history'][username][-500:]
        
        self._save_db(db)
    
    def get_chat_history(self, username: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Get chat history for a user"""
        db = self._load_db()
        
        if username in db['chat_history']:
            return db['chat_history'][username][-limit:]
        
        return []
    
    def clear_chat_history(self, username: str):
        """Clear chat history for a user"""
        db = self._load_db()
        
        if username in db['chat_history']:
            db['chat_history'][username] = []
            self._save_db(db)
    
    # Task Management
    def save_task(self, username: str, task: Dict[str, Any]) -> str:
        """Save a task and return its ID"""
        db = self._load_db()
        
        task_id = str(uuid.uuid4())
        task['id'] = task_id
        task['username'] = username
        task['created_at'] = datetime.now().isoformat()
        
        if username not in db['tasks']:
            db['tasks'][username] = {}
        
        db['tasks'][username][task_id] = task
        self._save_db(db)
        
        return task_id
    
    def get_user_tasks(self, username: str) -> List[Dict[str, Any]]:
        """Get all tasks for a user"""
        db = self._load_db()
        
        if username in db['tasks']:
            return list(db['tasks'][username].values())
        
        return []
    
    def update_task(self, username: str, task_id: str, updates: Dict[str, Any]) -> bool:
        """Update a task"""
        db = self._load_db()
        
        if username in db['tasks'] and task_id in db['tasks'][username]:
            db['tasks'][username][task_id].update(updates)
            db['tasks'][username][task_id]['updated_at'] = datetime.now().isoformat()
            self._save_db(db)
            return True
        
        return False
    
    def delete_task(self, username: str, task_id: str) -> bool:
        """Delete a task"""
        db = self._load_db()
        
        if username in db['tasks'] and task_id in db['tasks'][username]:
            del db['tasks'][username][task_id]
            self._save_db(db)
            return True
        
        return False
    
    # Analytics
    def get_user_stats(self, username: str) -> Dict[str, Any]:
        """Get user statistics"""
        db = self._load_db()
        
        stats = {
            'total_timetables': 0,
            'total_tasks': 0,
            'total_chat_messages': 0,
            'last_activity': None
        }
        
        if username in db['timetables']:
            stats['total_timetables'] = len(db['timetables'][username])
        
        if username in db['tasks']:
            stats['total_tasks'] = len(db['tasks'][username])
        
        if username in db['chat_history']:
            stats['total_chat_messages'] = len(db['chat_history'][username])
        
        # Get last activity
        activities = []
        
        if username in db['timetables']:
            for tt in db['timetables'][username].values():
                activities.append(tt.get('updated_at', tt.get('created_at')))
        
        if username in db['tasks']:
            for task in db['tasks'][username].values():
                activities.append(task.get('updated_at', task.get('created_at')))
        
        if activities:
            stats['last_activity'] = max(activities)
        
        return stats
    
    # Backup and Export
    def export_user_data(self, username: str) -> Dict[str, Any]:
        """Export all user data"""
        db = self._load_db()
        
        return {
            'user_data': db['users'].get(username, {}),
            'timetables': db['timetables'].get(username, {}),
            'chat_history': db['chat_history'].get(username, []),
            'tasks': db['tasks'].get(username, {}),
            'exported_at': datetime.now().isoformat()
        }
    
    def import_user_data(self, username: str, data: Dict[str, Any]) -> bool:
        """Import user data"""
        try:
            db = self._load_db()
            
            if 'timetables' in data:
                if username not in db['timetables']:
                    db['timetables'][username] = {}
                db['timetables'][username].update(data['timetables'])
            
            if 'chat_history' in data:
                db['chat_history'][username] = data['chat_history']
            
            if 'tasks' in data:
                if username not in db['tasks']:
                    db['tasks'][username] = {}
                db['tasks'][username].update(data['tasks'])
            
            self._save_db(db)
            return True
        except Exception:
            return False
