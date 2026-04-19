"""
Local file-based database fallback for testing without MongoDB
"""
import json
import os
from datetime import datetime, timezone
from pathlib import Path
import uuid
from typing import Any, cast # type: ignore

# Data directory
DATA_DIR = Path(__file__).parent / "local_data"
DATA_DIR.mkdir(exist_ok=True)

USERS_FILE = DATA_DIR / "users.json"
CONVERSATIONS_FILE = DATA_DIR / "conversations.json"
MESSAGES_FILE = DATA_DIR / "messages.json"
EVENTS_FILE = DATA_DIR / "events.json"

def load_json_file(file_path):
    """Load data from JSON file. Returns empty list if not found or empty."""
    if file_path.exists():
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data if isinstance(data, list) else []
        except:
            return []
    return []

def save_json_file(file_path, data):
    """Save data to JSON file"""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, default=str)
        return True
    except Exception as e:
        print(f"Error saving {file_path}: {e}")
        return False

# Simple mock result class
class MockResult:
    def __init__(self, **kwargs):
        self.inserted_id = kwargs.get('inserted_id')
        self.matched_count = kwargs.get('matched_count', 0)
        self.modified_count = kwargs.get('modified_count', 0)
        self.deleted_count = kwargs.get('deleted_count', 0)

# User management
def get_users_collection():
    """Mock users collection"""
    return LocalUsersCollection()

class LocalUsersCollection:
    def find_one(self, query, sort=None):
        users = load_json_file(USERS_FILE)
        
        # Apply sorting if provided
        if sort:
            field, direction = sort[0]
            users = sorted(users, key=lambda x: str(x.get(field, "")), reverse=(direction == -1))

        # Handle regex (prefix) matching for sequencing
        pattern_data = query.get("login_id")
        prefix = None
        if isinstance(pattern_data, dict) and "$regex" in pattern_data:
            prefix = pattern_data["$regex"].lstrip("^")

        for user in users:
            uid = user.get("login_id", "")
            if prefix:
                if uid.startswith(prefix):
                    return user
            elif uid == query.get("login_id"):
                return user
        return None
    
    def find(self, query=None, projection=None):
        users = load_json_file(USERS_FILE)
        if query:
            # Very basic filter support
            filtered = []
            for u in users:
                match = True
                for k, v in query.items():
                    if u.get(k) != v:
                        match = False
                        break
                if match:
                    filtered.append(u)
            users = filtered

        if projection and "password_hash" in projection:
            for user in users:
                user.pop("password_hash", None)
        return users
    
    def insert_one(self, user_data):
        users = load_json_file(USERS_FILE)
        if "_id" not in user_data:
            user_data["_id"] = str(uuid.uuid4())
        user_data["created_at"] = datetime.now(timezone.utc).isoformat()
        users.append(user_data)
        save_json_file(USERS_FILE, users)
        return MockResult(inserted_id=user_data["_id"])
    
    def update_one(self, query, update):
        users = load_json_file(USERS_FILE)
        for i, user in enumerate(users):
            if query.get("login_id") and user.get("login_id") == query["login_id"]:
                if "$set" in update:
                    users[i].update(update["$set"])
                save_json_file(USERS_FILE, users)
                return MockResult(matched_count=1, modified_count=1)
        return MockResult(matched_count=0, modified_count=0)

# Conversation management
def get_conversations_collection():
    return LocalConversationsCollection()

class LocalConversationsCollection:
    def find_one(self, query):
        convs = load_json_file(CONVERSATIONS_FILE)
        for conv in convs:
            if query.get("conversation_id") and conv.get("conversation_id") == query["conversation_id"]:
                return conv
            if query.get("_id") and str(conv.get("_id")) == str(query["_id"]):
                return conv
        return None
    
    def insert_one(self, conv_data):
        convs = load_json_file(CONVERSATIONS_FILE)
        if "_id" not in conv_data:
            conv_data["_id"] = str(uuid.uuid4())
        conv_data["created_at"] = datetime.now(timezone.utc).isoformat()
        convs.append(conv_data)
        save_json_file(CONVERSATIONS_FILE, convs)
        return MockResult(inserted_id=conv_data["_id"])

    def find(self, query=None):
        convs = load_json_file(CONVERSATIONS_FILE)
        if query and "participants" in query:
            p = query["participants"]
            return [c for c in convs if p in c.get("participants", [])]
        return convs

# Message management
def get_messages_collection():
    return LocalMessagesCollection()

class LocalMessagesCollection:
    def find(self, query=None, sort=None, limit=None):
        messages = load_json_file(MESSAGES_FILE)
        if query:
            if "conversation_id" in query:
                messages = [m for m in messages if m.get("conversation_id") == query["conversation_id"]]
        
        if sort:
            field, direction = sort[0]
            messages = sorted(messages, key=lambda x: str(x.get(field, "")), reverse=(direction == -1))
        
        if limit:
            messages = cast(Any, messages)[:limit]
        return messages
    
    def insert_one(self, msg_data):
        messages = load_json_file(MESSAGES_FILE)
        if "_id" not in msg_data:
            msg_data["_id"] = str(uuid.uuid4())
        msg_data["created_at"] = datetime.now(timezone.utc).isoformat()
        messages.append(msg_data)
        save_json_file(MESSAGES_FILE, messages)
        return MockResult(inserted_id=msg_data["_id"])
    
    def find_one(self, query=None, sort=None):
        messages = self.find(query=query, sort=sort, limit=1)
        return messages[0] if messages else None

# Event management
def get_events_collection():
    return LocalEventsCollection()

class LocalEventsCollection:
    def find(self, query=None, sort=None):
        events = load_json_file(EVENTS_FILE)
        if query:
            filtered = []
            for e in events:
                match = True
                for k, v in query.items():
                    if e.get(k) != v:
                        match = False
                        break
                if match:
                    filtered.append(e)
            events = filtered
        
        if sort:
            field, direction = sort[0]
            events = sorted(events, key=lambda x: str(x.get(field, "")), reverse=(direction == -1))
            
        return events
    
    def insert_one(self, event_data):
        events = load_json_file(EVENTS_FILE)
        if "_id" not in event_data:
            event_data["_id"] = str(uuid.uuid4())
        event_data["created_at"] = datetime.now(timezone.utc).isoformat()
        events.append(event_data)
        save_json_file(EVENTS_FILE, events)
        return MockResult(inserted_id=event_data["_id"])
    
    def update_one(self, query, update):
        events = load_json_file(EVENTS_FILE)
        for i, event in enumerate(events):
            if query.get("_id") and str(event.get("_id")) == str(query["_id"]):
                if "$set" in update:
                    events[i].update(update["$set"])
                save_json_file(EVENTS_FILE, events)
                return MockResult(matched_count=1, modified_count=1)
        return MockResult(matched_count=0, modified_count=0)
    
    def delete_one(self, query):
        events = load_json_file(EVENTS_FILE)
        for i, event in enumerate(events):
            if query.get("_id") and str(event.get("_id")) == str(query["_id"]):
                cast(Any, events).pop(i)
                save_json_file(EVENTS_FILE, events)
                return MockResult(deleted_count=1)
        return MockResult(deleted_count=0)

# Initialize with sample data
def initialize_sample_data():
    """Create sample admin users"""
    if not USERS_FILE.exists():
        admin_users = [
            {
                "login_id": "devadm000000",
                "password_hash": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj3bp.Gm.F5e",  # devadm000000
                "first_name": "Admin",
                "last_name": "User",
                "email": "admin@company.com",
                "department": "Development",
                "department_code": "dev",
                "role": "Admin",
                "role_code": "adm",
                "password_changed": False,
                "created_at": datetime.now(timezone.utc).isoformat()
            },
            {
                "login_id": "hrsadm000000",
                "password_hash": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj3bp.Gm.F5e",  # hrsadm000000
                "first_name": "HR",
                "last_name": "Admin",
                "email": "hr@company.com",
                "department": "Human Resources",
                "department_code": "hrs",
                "role": "Admin",
                "role_code": "adm",
                "password_changed": False,
                "created_at": datetime.now(timezone.utc).isoformat()
            }
        ]
        save_json_file(USERS_FILE, admin_users)
        print("Sample admin user created: devadm000000 / devadm000000")
    
    if not CONVERSATIONS_FILE.exists():
        save_json_file(CONVERSATIONS_FILE, [])
    
    if not MESSAGES_FILE.exists():
        save_json_file(MESSAGES_FILE, [])
    
    if not EVENTS_FILE.exists():
        save_json_file(EVENTS_FILE, [])

# Initialize data on import
initialize_sample_data()
