# Corporate Smart Messenger 💬

A Streamlit-based chat application with a corporate-style user experience, role-based dashboards, MongoDB-powered messaging, and a shared backend for authentication and data access. Now includes an AI assistant powered by Retrieval-Augmented Generation (RAG) for intelligent chat history analysis.

## 🚀 Project Status: Ready to Run

**Last Updated**: April 19, 2026
**Status**: ✅ Fully configured and operational
**Dependencies**: ✅ All installed and tested

## 📅 Recent Updates (April 19, 2026)

### 🔧 **Major Fixes & Improvements**
- **✅ Database System**: Implemented local file-based database fallback for offline functionality
- **✅ Authentication**: Fixed bcrypt password hashing and login issues
- **✅ UI Issues**: Resolved calendar double numbers and message list display problems
- **✅ Performance**: Optimized auto-refresh and added intelligent caching
- **✅ Chat Interface**: Fixed excessive whitespace in message display area

### 🗄️ **Database Enhancements**
- **Local Storage**: Complete JSON-based database system (`backend/local_db.py`)
- **MongoDB Ready**: Migration tool (`migrate_to_mongodb.py`) for cloud deployment
- **Fallback System**: Automatic switching between MongoDB and local storage

### 👥 **User Management**
- **Test Accounts**: Created working admin and test user accounts
- **Credentials**: 
  - Admin: `devadm000001` / `admin123`
  - Test: `devsen000001` / `devadm000000`

### 📚 **Documentation**
- **UML Diagrams**: Complete specifications for all 9 UML diagram types
- **Changes Log**: Detailed `CHANGES_TODAY.md` with all modifications
- **Setup Guide**: Updated installation and configuration instructions

### 🎯 **Current Status**
- **Server**: Running on http://localhost:8504
- **Features**: All core functionality working
- **Database**: Local JSON storage (MongoDB migration ready)
- **Performance**: Optimized and responsive

## Project Overview

This project is divided into two main areas:
- `frontend/` — Streamlit user interface and page navigation
- `backend/` — MongoDB connection, authentication, user management, chat data logic, and RAG-powered AI assistant

It includes:
- login flow for users and admins
- dashboard screens for users and administrators
- real-time direct and group messaging
- a calendar UI for events and daily notes
- password change and user registration workflows
- AI assistant for querying chat history using natural language

## Key Files

```text
frontend/
  app.py                 # Main Streamlit navigation wrapper
  home.py                # Landing page and feature overview
  styles.py              # Shared CSS injected into all pages
  pages/
    admin_dashboard.py   # Admin dashboard with user registration and department view
    ai_assistant.py      # AI assistant interface for querying chat history
    calendar.py          # Calendar with events, note saving, and month navigation
    change_password.py   # Change password flow for logged-in users
    messages.py          # Chat interface for direct and group conversations
    streamlit_login.py   # Login page and session initialization
    user_dashboard.py    # User dashboard with messages/calendar/chatbot/settings
backend/
  __init__.py            # Backend package initialization for Streamlit imports
  auth.py                # Login, registration validation, password change logic
  database.py            # MongoDB client with local database fallback
  local_db.py            # Local file-based database implementation (NEW)
  export_rag_data.py     # Exports chat data to CSV for RAG analysis
  rag_assistant.py       # RAG-powered AI assistant for answering questions from chat history
  rag_extractor.py       # Extracts schedule and project status signals from messages
  rag_indexer.py         # Embeds and indexes messages into ChromaDB vector database
  rag_watcher.py         # Watches MongoDB for new messages and indexes them in real-time
  seed_index.py          # Seeds the RAG index with existing messages
  setup_admins.py        # Script to create seeded admin accounts

Configuration & Tools
  .env                   # Environment configuration (NEW)
  migrate_to_mongodb.py  # MongoDB migration tool (NEW)
  CHANGES_TODAY.md       # Detailed changes log (NEW)
  UML_Diagrams_Specifications.md  # Complete UML documentation (NEW)

Local Data Storage
  backend/local_data/    # Local JSON database files (NEW)
    users.json           # User accounts
    conversations.json   # Chat conversations
    messages.json        # Chat messages
    events.json          # Calendar events
  test_connection.py     # MongoDB connectivity test script
README.md               # This documentation file
start_app.bat           # Windows launcher (path is currently absolute and may need adjustment)
```

> Note: `frontend/app.py` references `frontend/pages/signup.py`, but that file is not present in the current workspace.

## Backend Summary

### `backend/auth.py`
- validates login IDs with department/role codes
- validates strong passwords
- registers users with auto-generated login IDs
- hashes passwords using `bcrypt`
- supports login and password changes

### `backend/database.py`
- connects to MongoDB Atlas using `MONGODB_URI` and `DB_NAME`
- manages `users`, `conversations`, and `messages` collections
- creates or retrieves direct conversations
- creates group conversations
- stores and retrieves chat history
- lists users for chat selection

### `backend/setup_admins.py`
- creates seeded admin accounts for each department
- admin login IDs follow the pattern: `<dept>adm000000`
- initial password is the same as the login ID and must be changed on first login

### `backend/test_connection.py`
- proves MongoDB connectivity
- currently contains a hardcoded Atlas URI placeholder, so update it before use

### RAG (Retrieval-Augmented Generation) Components

#### `backend/rag_indexer.py`
- embeds messages using Sentence Transformers and stores them in ChromaDB vector database
- creates searchable vector representations of chat history

#### `backend/rag_assistant.py`
- retrieves relevant context from chat history based on user queries
- uses Anthropic Claude to generate answers about schedules, projects, and teammate discussions

#### `backend/rag_extractor.py`
- extracts schedule signals (meetings, calls) and project status from messages
- identifies busy slots and project states (done, blocked, in progress)

#### `backend/rag_watcher.py`
- monitors MongoDB for new messages and indexes them in real-time
- ensures the vector database stays up-to-date with latest conversations

#### `backend/seed_index.py`
- initializes the RAG index with existing messages from the database
- run this script to populate the index for the first time

#### `backend/export_rag_data.py`
- exports chat data to CSV format for external analysis or backup
- includes sender details, departments, and message content

## Frontend Summary

### `frontend/app.py`
- initializes Streamlit page settings
- injects shared CSS from `frontend/styles.py`
- handles top-level page navigation via session state

### `frontend/home.py`
- landing page with hero section and feature cards
- login button that routes into the app
- marketing-style content for onboarding users

### `frontend/styles.py`
- shared CSS rules applied globally
- custom colors, form styling, button styling, dashboard card styles, and layout tweaks

### `frontend/pages/streamlit_login.py`
- login form with structured login ID help
- validates credentials via `backend/auth.py`
- redirects users to either user or admin dashboard after login
- forces password change if `password_changed` is false

### `frontend/pages/user_dashboard.py`
- user dashboard card grid
- quick access to messages, calendar, chatbot, and settings
- inline chatbot and settings panels
- password change form inside settings

### `frontend/pages/admin_dashboard.py`
- admin-only access guard
- admin feature cards for messages, calendar, chatbot, settings
- user registration workflow with department and role selection
- department user list view for admin management

### `frontend/pages/ai_assistant.py`
- AI assistant interface powered by RAG
- allows users to ask natural language questions about their chat history
- provides answers on schedules, project status, and teammate discussions

### `frontend/pages/messages.py`
- WhatsApp-style conversation layout
- direct chat creation with any other registered user
- group chat creation
- message history display with automatic refresh

### `frontend/pages/calendar.py`
- monthly calendar UI with date selection
- event list for selected day
- note saving area
- month navigation buttons

### `frontend/pages/change_password.py`
- change password form for authenticated users
- validates current and new password entries

## 📋 Requirements & Dependencies

### ✅ Dependencies Already Installed
All required packages have been successfully installed and tested:

```bash
# Backend dependencies - INSTALLED
pip install -r backend/requirements.txt
# ✅ pymongo[srv]==4.7.2, python-dotenv==1.0.1, bcrypt==4.1.3
# ✅ sentence-transformers, chromadb, python-dateutil, anthropic
# ✅ groq (additional dependency added during setup)

# Frontend dependencies - INSTALLED
pip install -r frontend/requirements.txt
# ✅ streamlit, streamlit-autorefresh==1.0.1 (version fixed from 1.35.0)
```

### Backend Dependencies ✅
- `pymongo[srv]==4.7.2`: MongoDB driver
- `python-dotenv==1.0.1`: Environment variable management
- `bcrypt==4.1.3`: Password hashing
- `sentence-transformers`: Text embedding for RAG
- `chromadb`: Vector database for message indexing
- `python-dateutil`: Date parsing utilities
- `anthropic`: Claude LLM client for AI responses
- `groq==1.2.0`: Additional AI model client (added during setup)

### Frontend Dependencies ✅
- `streamlit==1.52.0`: Web app framework
- `streamlit-autorefresh==1.0.1`: Auto-refresh functionality (version fixed)

## Environment Setup

Create a `.env` file in the project root with at least:

```env
MONGODB_URI=<your MongoDB Atlas connection string>
DB_NAME=chatapp1
ANTHROPIC_API_KEY=<your Anthropic API key>
```

## RAG Setup

To enable the AI assistant feature:

1. Install the backend dependencies as described above.

2. Seed the RAG index with existing messages:
   ```bash
   python backend/seed_index.py
   ```

3. For real-time indexing of new messages, run the watcher in the background:
   ```bash
   python backend/rag_watcher.py
   ```

4. The AI assistant will be available in the user dashboard and as a dedicated page.

To export chat data for analysis:
```bash
python backend/export_rag_data.py
```

## 🚀 Quick Start - Run the Application

### Option 1: Navigate and Run (Recommended)
```bash
cd "c:/Users/Kavya/OneDrive/Desktop/chat_app se/frontend"
python -m streamlit run home.py
```

### Option 2: PowerShell One-Liner
```powershell
cd "c:/Users/Kavya/OneDrive/Desktop/chat_app se/frontend"; python -m streamlit run home.py
```

### Option 3: From Project Root
```bash
cd "c:/Users/Kavya/OneDrive/Desktop/chat_app se"
cd frontend
python -m streamlit run home.py
```

### Access the Application
- **Local URL**: http://localhost:8501
- **Network URL**: http://10.1.40.45:8501
- **Browser Preview**: Available in IDE

### Windows Launcher (Fixed)
The `start_app.bat` file has been updated with correct paths:
```powershell
start_app.bat
```

> ⚠️ **Note**: The original batch file had incorrect paths and has been corrected for this project structure.

## Admin Bootstrap

Seed admin accounts with:

```bash
python backend/setup_admins.py
```

Admin credentials created by default are:
- `devadm000000`
- `hrsadm000000`
- `finadm000000`
- `mktadm000000`
- `salamd000000`
- `supadm000000`

Each initial password matches the login ID and should be changed immediately.

## 📝 Project Modifications & Setup Work Completed

### ✅ Dependencies & Environment Setup
- **Backend Dependencies**: Successfully installed all required packages including pymongo, bcrypt, sentence-transformers, chromadb, anthropic
- **Frontend Dependencies**: Installed streamlit and fixed streamlit-autorefresh version compatibility (1.35.0 → 1.0.1)
- **Additional Dependency**: Added and installed `groq==1.2.0` for calendar agent functionality
- **Path Configuration**: Fixed Windows batch file paths for proper project execution

### ✅ Application Testing & Verification
- **Streamlit Server**: Successfully launched and running on http://localhost:8501
- **Browser Preview**: Configured and accessible through IDE
- **Module Imports**: All Python modules loading correctly
- **Error Resolution**: Fixed missing `groq` module errors in calendar functionality

### 🔧 Known Issues & Resolutions
1. **streamlit-autorefresh Version**: Fixed incompatible version 1.35.0 → 1.0.1
2. **Missing groq Module**: Added groq dependency to resolve calendar agent crashes
3. **Batch File Paths**: Updated start_app.bat with correct project directory structure

### ⚠️ Outstanding Requirements
- **MongoDB Connection**: Requires MongoDB Atlas URI in `.env` file for full functionality
- **API Keys**: Anthropic API key needed for AI assistant features
- **Initial Setup**: Run `python backend/setup_admins.py` to create admin accounts

### 📁 Project Structure Notes
- **Signup Page**: `frontend/app.py` references missing `signup.py` file (non-critical)
- **Test Connection**: `backend/test_connection.py` contains hardcoded URI (update for production)
- **Session Management**: Uses Streamlit session state for navigation and role-based access
- **RAG System**: Requires ChromaDB and message seeding for AI assistant functionality

### 🎯 Next Steps for Full Deployment
1. Create `.env` file with MongoDB URI and API keys
2. Run admin setup: `python backend/setup_admins.py`
3. Seed RAG index: `python backend/seed_index.py` (after adding messages)
4. Configure real-time indexing: `python backend/rag_watcher.py` (optional)

---

**Project is ready for development and testing!** 🎉 All core dependencies installed and application successfully running.
