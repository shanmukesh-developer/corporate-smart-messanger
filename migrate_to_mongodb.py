"""
Migration script to move local JSON data to MongoDB
"""
import json
import os
from pathlib import Path
from pymongo import MongoClient # type: ignore
from dotenv import load_dotenv # type: ignore
from datetime import datetime, timezone

load_dotenv()

# Local data paths
DATA_DIR = Path(__file__).parent / "backend" / "local_data"
USERS_FILE = DATA_DIR / "users.json"
CONVERSATIONS_FILE = DATA_DIR / "conversations.json"
MESSAGES_FILE = DATA_DIR / "messages.json"
EVENTS_FILE = DATA_DIR / "events.json"

def migrate_to_mongodb():
    """Migrate local JSON data to MongoDB"""
    
    # Get MongoDB configuration
    mongodb_uri = os.getenv("MONGODB_URI")
    db_name = os.getenv("DB_NAME", "chatapp1")
    
    if not mongodb_uri or mongodb_uri == "mongodb+srv://username:password@cluster.mongodb.net/" or "username:password" in mongodb_uri:
        print("❌ MONGODB_URI is missing or contains placeholder values!")
        print("Please update your .env file with your actual MongoDB Atlas connection string.")
        print("Example: MONGODB_URI=mongodb+srv://admin:secret@mycluster.a1b2c.mongodb.net/")
        return False
    
    try:
        # Connect to MongoDB
        print("🔄 Connecting to MongoDB...")
        client = MongoClient(mongodb_uri, serverSelectionTimeoutMS=10000)
        client.admin.command("ping")
        print("✅ Connected to MongoDB successfully")
        
        db = client[db_name]
        
        # Migrate Users
        if USERS_FILE.exists():
            print("📤 Migrating users...")
            with open(USERS_FILE, 'r', encoding='utf-8') as f:
                users = json.load(f)
            
            if users:
                # Clear existing users
                db["users"].delete_many({})
                # Insert users
                db["users"].insert_many(users)
                print(f"✅ Migrated {len(users)} users")
        
        # Migrate Conversations
        if CONVERSATIONS_FILE.exists():
            print("📤 Migrating conversations...")
            with open(CONVERSATIONS_FILE, 'r', encoding='utf-8') as f:
                conversations = json.load(f)
            
            if conversations:
                # Clear existing conversations
                db["conversations"].delete_many({})
                # Insert conversations
                db["conversations"].insert_many(conversations)
                print(f"✅ Migrated {len(conversations)} conversations")
        
        # Migrate Messages
        if MESSAGES_FILE.exists():
            print("📤 Migrating messages...")
            with open(MESSAGES_FILE, 'r', encoding='utf-8') as f:
                messages = json.load(f)
            
            if messages:
                # Clear existing messages
                db["messages"].delete_many({})
                # Insert messages
                db["messages"].insert_many(messages)
                print(f"✅ Migrated {len(messages)} messages")
        
        # Migrate Events
        if EVENTS_FILE.exists():
            print("📤 Migrating events...")
            with open(EVENTS_FILE, 'r', encoding='utf-8') as f:
                events = json.load(f)
            
            if events:
                # Clear existing events
                db["events"].delete_many({})
                # Insert events
                db["events"].insert_many(events)
                print(f"✅ Migrated {len(events)} events")
        
        print("\n🎉 Migration completed successfully!")
        print(f"📍 Database: {db_name}")
        print(f"🌐 MongoDB URI: {mongodb_uri}")
        
        client.close()
        return True
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        return False

def show_local_data():
    """Show current local data statistics"""
    print("📊 Current Local Data:")
    
    for file_path, name in [
        (USERS_FILE, "Users"),
        (CONVERSATIONS_FILE, "Conversations"), 
        (MESSAGES_FILE, "Messages"),
        (EVENTS_FILE, "Events")
    ]:
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            print(f"  • {name}: {len(data)} records")
        else:
            print(f"  • {name}: 0 records (file not found)")

if __name__ == "__main__":
    print("🔄 MongoDB Migration Tool")
    print("=" * 40)
    
    # Show current data
    show_local_data()
    print()
    
    # Check .env file
    if not os.path.exists(".env"):
        print("❌ .env file not found!")
        print("Creating sample .env file...")
        
        sample_env = """# MongoDB Configuration
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/
DB_NAME=chatapp1

# API Keys (optional for full functionality)
ANTHROPIC_API_KEY=your_anthropic_key_here
GROQ_API_KEY=your_groq_key_here

# Calendar Agent Settings
CALENDAR_AGENT_POLL_INTERVAL=15
"""
        
        with open(".env", "w") as f:
            f.write(sample_env)
        print("✅ Created .env file. Please update with your MongoDB credentials.")
        print()
    
    # Perform migration
    success = migrate_to_mongodb()
    
    if success:
        print("\n📝 Next Steps:")
        print("1. Restart the Streamlit application")
        print("2. The app will now use MongoDB instead of local files")
        print("3. Your data is safely stored in MongoDB Atlas")
    else:
        print("\n📝 Troubleshooting:")
        print("1. Update MONGODB_URI in .env file")
        print("2. Ensure your IP is whitelisted in MongoDB Atlas")
        print("3. Check your MongoDB credentials")
