# UML Diagrams Specifications - Corporate Smart Messenger

## Project Overview
Corporate Smart Messenger is a Streamlit-based chat application with role-based access control, real-time messaging, calendar integration, and AI-powered features. The system consists of a frontend (Streamlit UI), backend (Python services), and database layer (MongoDB/Local file storage).

---

## 8.1 Data Flow Diagram (DFD)

### Level 0 DFD - Context Diagram
**External Entities:**
- User (Admin/Employee)
- AI Services (Anthropic Claude, Groq)
- MongoDB Atlas/Local Storage

**Central Process:**
- Corporate Smart Messenger System

**Data Flows:**
- User Credentials → Authentication
- Chat Messages → Message Processing
- Calendar Events → Event Management
- User Requests → AI Assistant
- System Responses → User Interface

### Level 1 DFD - Detailed Processes

**Process 1: Authentication Module**
- Input: Login ID, Password, Registration Data
- Output: Session Token, User Profile, Error Messages
- Data Store: Users Collection
- Sub-processes: Validate Credentials, Create Session, Manage Roles

**Process 2: Message Management**
- Input: Message Content, Recipient Info, Conversation ID
- Output: Sent Messages, Conversation History, Notifications
- Data Store: Messages Collection, Conversations Collection
- Sub-processes: Send Message, Retrieve History, Manage Conversations

**Process 3: Calendar System**
- Input: Event Details, Date Selection, User Preferences
- Output: Calendar View, Event Reminders, Scheduled Events
- Data Store: Events Collection
- Sub-processes: Create Event, Extract Tasks, Auto-refresh Calendar

**Process 4: AI Assistant**
- Input: User Queries, Chat History, Calendar Data
- Output: AI Responses, Extracted Events, Schedule Insights
- External: Anthropic API, Groq API
- Sub-processes: Process Query, Analyze Context, Generate Response

**Process 5: User Management**
- Input: User Details, Department Info, Role Assignments
- Output: User Profiles, Access Control, Department Lists
- Data Store: Users Collection
- Sub-processes: Register User, Update Profile, Manage Permissions

---

## 8.2 Use Case Diagram

### Actors
**Primary Actors:**
- Admin (System Administrator)
- User (Regular Employee)

**Secondary Actors:**
- AI Assistant (Automated Service)
- Calendar Agent (Background Process)

### Use Cases

**Admin Use Cases:**
- UC-01: Login to System
- UC-02: Register New Users
- UC-03: Manage User Accounts
- UC-04: View Department Statistics
- UC-05: Access Admin Dashboard
- UC-06: Monitor System Activity
- UC-07: Manage Calendar Events
- UC-08: Send Messages to Users

**User Use Cases:**
- UC-09: Login to System
- UC-10: Update Profile
- UC-11: Change Password
- UC-12: Send Direct Messages
- UC-13: Participate in Group Chats
- UC-14: View Message History
- UC-15: Create Calendar Events
- UC-16: View Calendar
- UC-17: Add Daily Notes
- UC-18: Query AI Assistant
- UC-19: Access User Dashboard

**General Use Cases:**
- UC-20: Auto-refresh Interface
- UC-21: Receive Notifications
- UC-22: Extract Events from Chat
- UC-23: Sync Calendar Data

### Relationships
- «include» Login to System for all other use cases
- «extend» AI Assistant for Calendar Event Extraction
- «extend» Auto-refresh for Real-time Messaging
- Generalization: Admin is a specialized type of User

---

## 8.3 Class Diagram

### Core Classes

**User Class**
```python
class User:
    - login_id: str
    - password_hash: str
    - first_name: str
    - last_name: str
    - email: str
    - department: str
    - department_code: str
    - role: str
    - role_code: str
    - password_changed: bool
    - created_at: datetime
    + validate_login_id(): bool
    + validate_password(): bool
    + update_profile(): bool
    + change_password(): bool
```

**Message Class**
```python
class Message:
    - message_id: ObjectId
    - conversation_id: str
    - sender_id: str
    - content: str
    - timestamp: datetime
    - message_type: str
    + send(): bool
    + edit(): bool
    + delete(): bool
    + get_history(): List[Message]
```

**Conversation Class**
```python
class Conversation:
    - conversation_id: str
    - is_group: bool
    - name: str
    - participants: List[str]
    - created_at: datetime
    - last_message: str
    - last_message_time: datetime
    + create_direct_conversation(): Conversation
    + create_group_conversation(): Conversation
    + add_participant(): bool
    + remove_participant(): bool
```

**CalendarEvent Class**
```python
class CalendarEvent:
    - event_id: ObjectId
    - title: str
    - date: str
    - time: str
    - type: str
    - assigned_to: str
    - created_by: str
    - status: str
    - confidence: float
    - extraction_method: str
    + create_event(): ObjectId
    + update_status(): bool
    + delete_event(): bool
    + get_events_by_date(): List[CalendarEvent]
```

**Authentication Class**
```python
class Authentication:
    - session_state: dict
    - current_user: User
    + login(login_id, password): tuple[bool, str, User]
    + logout(): void
    + register_user(user_data): tuple[bool, str]
    + validate_session(): bool
    + get_user_role(): str
```

### Relationships
- User "1" --- "*" Message (sends)
- User "*" --- "*" Conversation (participates)
- Conversation "1" --- "*" Message (contains)
- User "1" --- "*" CalendarEvent (creates/assigned)
- Authentication "1" --- "1" User (manages)

### Inheritance
- Admin extends User
- RegularUser extends User

---

## 8.4 Object Diagram

### Instance Example: Admin User Session

**Objects:**
- adminUser: User
  - login_id = "devadm000000"
  - first_name = "Admin"
  - last_name = "User"
  - department = "Development"
  - role = "Admin"

- authSession: Authentication
  - current_user = adminUser
  - session_state = {logged_in: true, role: "admin"}

- conversation1: Conversation
  - conversation_id = "direct_devadm000000_devdev000001"
  - is_group = false
  - participants = ["devadm000000", "devdev000001"]

- message1: Message
  - conversation_id = "direct_devadm000000_devdev000001"
  - sender_id = "devadm000000"
  - content = "Welcome to the team!"
  - timestamp = "2026-04-19T10:30:00Z"

- event1: CalendarEvent
  - title = "Team Meeting"
  - date = "2026-04-20"
  - time = "2:00 PM"
  - assigned_to = "devdev000001"
  - status = "pending"

### Links
- adminUser → authSession (manages)
- adminUser → message1 (sends)
- adminUser → conversation1 (participates)
- conversation1 → message1 (contains)
- adminUser → event1 (creates)

---

## 8.5 Package Diagram

### Package Structure

**Frontend Package**
- pages/
  - streamlit_login.py
  - user_dashboard.py
  - admin_dashboard.py
  - messages.py
  - calendar.py
  - ai_assistant.py
  - change_password.py
- app.py
- home.py
- styles.py

**Backend Package**
- auth.py
- database.py
- local_db.py
- calendar_agent.py
- rag_assistant.py
- rag_indexer.py
- rag_watcher.py
- task_extractor.py

**RAG Package**
- rag_store/
  - vector_db/
  - embeddings/
  - indexed_data/

**Data Package**
- local_data/
  - users.json
  - conversations.json
  - messages.json
  - events.json

### Dependencies
- Frontend → Backend (imports)
- Backend → Data (reads/writes)
- Backend → RAG (AI processing)
- Frontend ← Backend (data flow)

---

## 8.6 Sequence Diagram

### Scenario: User Login and Send Message

**Actors:**
- User
- Streamlit Frontend
- Authentication Service
- Database
- Message Service

**Sequence:**

1. User → Frontend: Enter credentials
2. Frontend → Auth Service: login(login_id, password)
3. Auth Service → Database: find_user(login_id)
4. Database → Auth Service: user_data
5. Auth Service → Auth Service: validate_password()
6. Auth Service → Frontend: (success, message, user_data)
7. Frontend → Frontend: update_session_state()
8. Frontend → User: Display dashboard

**Message Sending Sequence:**

9. User → Frontend: Type message and click send
10. Frontend → Message Service: send_message(conversation_id, sender_id, content)
11. Message Service → Database: insert_message(message_data)
12. Database → Message Service: message_id
13. Message Service → Database: update_conversation_last_message()
14. Message Service → Frontend: message_sent_confirmation
15. Frontend → Frontend: auto_refresh(5_seconds)
16. Frontend → User: Display new message

### Calendar Event Extraction Sequence

1. Message Service → Task Extractor: extract_tasks_from_message()
2. Task Extractor → AI Service: analyze_message_for_events()
3. AI Service → Task Extractor: extracted_tasks
4. Task Extractor → Database: create_event(event_data)
5. Database → Task Extractor: event_id
6. Frontend → Database: get_user_events() (auto-refresh)
7. Database → Frontend: events_data
8. Frontend → User: Display new calendar event

---

## 8.7 Collaboration Diagram

### Message Flow Collaboration

**Objects:**
- UserController
- MessageController
- DatabaseManager
- CalendarAgent
- AIAssistant

**Collaboration Pattern:**

1. UserController → MessageController: sendMessage(content, recipient)
2. MessageController → DatabaseManager: storeMessage(message)
3. MessageController → CalendarAgent: analyzeMessage(message)
4. CalendarAgent → AIAssistant: extractEventDetails(message)
5. AIAssistant → CalendarAgent: eventDetails
6. CalendarAgent → DatabaseManager: storeEvent(event)
7. DatabaseManager → MessageController: confirmation
8. MessageController → UserController: success

### Authentication Collaboration

1. UserController → AuthController: login(credentials)
2. AuthController → DatabaseManager: findUser(login_id)
3. DatabaseManager → AuthController: userData
4. AuthController → AuthController: verifyPassword()
5. AuthController → DatabaseManager: updateLastLogin()
6. AuthController → UserController: authResult

---

## 8.8 Component Diagram

### System Components

**Presentation Layer Components**
- StreamlitUI
  - LoginComponent
  - DashboardComponent
  - MessageComponent
  - CalendarComponent
  - AIAssistantComponent

**Business Logic Components**
- AuthenticationComponent
  - LoginService
  - RegistrationService
  - SessionManager
- MessageComponent
  - MessageService
  - ConversationService
  - NotificationService
- CalendarComponent
  - EventService
  - TaskExtractor
  - CalendarAgent

**Data Layer Components**
- DatabaseComponent
  - MongoDBAdapter
  - LocalFileAdapter
  - DataMapper
- AIComponent
  - AnthropicAdapter
  - GroqAdapter
  - RAGProcessor

### Interfaces
- IAuthentication (validate, login, logout)
- IMessaging (send, receive, history)
- ICalendar (create, update, delete events)
- IDataStorage (save, retrieve, update)
- IAIProcessor (analyze, extract, respond)

### Component Dependencies
- StreamlitUI → AuthenticationComponent
- StreamlitUI → MessageComponent
- StreamlitUI → CalendarComponent
- MessageComponent → DatabaseComponent
- CalendarComponent → AIComponent
- All Components → DatabaseComponent

---

## 8.9 Deployment Diagram

### Node Architecture

**Client Nodes**
- Web Browser (Chrome, Firefox, Safari)
- Operating System (Windows, macOS, Linux)
- Network Connection (Internet/Intranet)

**Application Server Node**
- Streamlit Server
  - Python 3.13 Runtime
  - Streamlit Framework
  - Frontend Components
  - Backend Services

**Database Nodes**
- MongoDB Atlas (Cloud)
  - Primary Database
  - Collections: users, conversations, messages, events
- Local File Storage (Fallback)
  - JSON Files
  - Local Data Directory

**AI Service Nodes**
- Anthropic Claude API
  - Natural Language Processing
  - AI Assistant Responses
- Groq API
  - Calendar Event Extraction
  - Message Analysis

**Development Environment**
- Development Machine
  - IDE (VS Code)
  - Local Testing Server
  - Git Repository

### Connections
- Browser ←→ Streamlit Server (HTTP/WebSocket)
- Streamlit Server ←→ MongoDB Atlas (MongoDB Protocol)
- Streamlit Server ←→ Local Storage (File System)
- Streamlit Server ←→ Anthropic API (HTTPS)
- Streamlit Server ←→ Groq API (HTTPS)

### Artifacts
- chat_app_frontend.war (Streamlit Application)
- backend_services.jar (Python Backend)
- database_config.json (Database Configuration)
- ai_api_keys.env (API Keys Configuration)

---

## Summary

This comprehensive UML documentation covers all aspects of the Corporate Smart Messenger system:

1. **Data Flow Diagrams** show how data moves through authentication, messaging, calendar, and AI modules
2. **Use Case Diagrams** detail all user interactions with the system
3. **Class Diagrams** define the core data structures and their relationships
4. **Object Diagrams** provide concrete instances of the system in operation
5. **Package Diagrams** organize the codebase into logical modules
6. **Sequence Diagrams** illustrate the order of operations for key scenarios
7. **Collaboration Diagrams** show how components communicate
8. **Component Diagrams** break down the system into reusable parts
9. **Deployment Diagrams** describe the physical architecture and deployment setup

These specifications can be used with Claude or any UML diagramming tool to generate visual diagrams for documentation, presentations, or system design reviews.
