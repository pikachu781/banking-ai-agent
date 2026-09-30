# banking-ai-agent
AI-powered banking assistant with voice interaction, RAG, memory, banking services, and intelligent query routing.
# 🏦 AI Banking Assistant

An intelligent **AI-powered banking assistant** that combines traditional banking services with **Generative AI, RAG, long-term memory, voice interaction, and intelligent query routing**.

The system allows users to interact with banking services using natural-language queries instead of navigating through multiple banking screens.

---

## 🚀 Features

### 🔐 Authentication & Security

* User registration and login
* JWT-based authentication
* BCrypt password encryption
* Email verification
* Role-based access
* Protected Angular routes

### 💳 Banking Services

* Account details
* Account balance
* Transaction history
* Card details and status
* Credit card information
* Loan details and status
* Fixed Deposit (FD)
* FD interest calculation
* EMI calculation
* Interest rate information
* KYC management

### 🤖 AI Banking Assistant

* Natural-language banking queries
* Intelligent query classification
* Banking database queries
* General AI conversations
* Task-based banking operations
* AI-generated responses

### 🧠 RAG & Memory

* Long-term user memory
* Conversation history
* Semantic memory search
* ChromaDB vector database
* Embeddings using `nomic-embed-text`
* Memory importance scoring
* Memory conflict detection
* Memory replacement/deactivation
* Context-aware responses

### 🎤 Voice AI

* Voice-based interaction
* AI response generation
* Text-to-Speech integration
* Voice assistant architecture

### 🧭 Intelligent Navigation

The AI can understand navigation requests and redirect users to the appropriate banking page.

For example:

```text
"Show my transactions"
        ↓
AI detects transaction intent
        ↓
/transactions
```

---

# 🏗️ System Architecture

```text
                    ┌─────────────────────┐
                    │      Angular       │
                    │     Frontend       │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    Spring Boot      │
                    │    Backend API      │
                    │                     │
                    │ JWT + Security      │
                    │ Banking APIs        │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │      FastAPI        │
                    │     AI Service      │
                    └──────────┬──────────┘
                               │
                ┌──────────────┼──────────────┐
                │              │              │
                ▼              ▼              ▼
        ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
        │ Query Router│ │  RAG/Memory │ │   Tasks     │
        └─────────────┘ └──────┬──────┘ └─────────────┘
                               │
                     ┌─────────┴─────────┐
                     ▼                   ▼
                ┌─────────┐         ┌──────────┐
                │ ChromaDB│         │  Ollama  │
                │         │         │  Mistral │
                └─────────┘         └──────────┘
```

---

# 🧩 Technology Stack

## Frontend

* Angular
* TypeScript
* Bootstrap
* Bootstrap Icons
* HTML5
* CSS3
* RxJS

## Backend

* Java 17
* Spring Boot 3
* Spring Security
* JWT
* BCrypt
* REST APIs
* MySQL

## AI Service

* Python 3.11
* FastAPI
* SQLAlchemy
* Ollama
* Mistral
* ChromaDB
* Embeddings
* RAG
* AI Memory

---

# 📁 Project Structure

```text
ai-banking-assistant/
│
├── frontend/
│   └── V-AI-AGENT/
│       ├── src/
│       ├── package.json
│       └── angular.json
│
├── backend/
│   └── login-backend/
│       ├── src/
│       ├── pom.xml
│       └── ...
│
├── ai-service/
│   ├── app/
│   │   ├── main.py
│   │   ├── routers/
│   │   ├── services/
│   │   ├── models/
│   │   └── ...
│   ├── requirements.txt
│   └── ...
│
├── .gitignore
└── README.md
```

---

# 🔄 AI Query Flow

The AI assistant first determines what type of request the user has made.

```text
User Query
     │
     ▼
Query Router
     │
     ├── REALTIME
     │       ↓
     │   Banking MySQL
     │
     ├── RETRIEVAL
     │       ↓
     │   RAG + Memory
     │
     ├── TASK
     │       ↓
     │   Banking Tools
     │
     └── GENERAL
             ↓
        Generative AI
```

### Example

User:

```text
What is my account balance?
```

The system identifies this as a realtime banking query and retrieves the relevant information from the banking database.

Another example:

```text
What is my career goal?
```

The system searches the user's stored memories using semantic similarity and provides the relevant memory.

---

# 🧠 Memory System

The project includes a persistent AI memory system.

Memory information contains:

```text
User ID
Memory Content
Memory Type
Importance
Created Date
Active Status
```

Example:

```text
Memory:
User wants to become a Python developer.

Type:
GOAL

Importance:
9
```

The memory system uses:

```text
User Query
     ↓
Embedding
     ↓
ChromaDB Search
     ↓
Relevant Memories
     ↓
AI Context
     ↓
Response
```

---

# 🗄️ Database

The project uses MySQL for application and banking data.

Main banking entities include:

* Users
* Bank Accounts
* Transactions
* Cards
* Credit Cards
* Loans
* Fixed Deposits
* Conversations
* Messages
* Memories

ChromaDB is used separately for semantic memory retrieval.

---

# 🔒 Security

Security features include:

* JWT authentication
* BCrypt password hashing
* Protected frontend routes
* Role-based authorization
* Authenticated API requests
* Environment-based secret configuration

> **Important:** Never commit `.env` files, passwords, JWT secrets, API keys, or access tokens to GitHub.

Use `.env.example` files containing placeholders instead.

---

# ⚙️ Installation

## 1. Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/ai-banking-assistant.git
cd ai-banking-assistant
```

---

## 2. Start MySQL

Create the required database:

```sql
CREATE DATABASE voice_ai_db;
```

Configure the database credentials in your local environment/configuration.

---

# ▶️ Start FastAPI AI Service

Navigate to the AI service:

```bash
cd ai-service
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start FastAPI:

```bash
uvicorn app.main:app --port 8000
```

API:

```text
http://localhost:8000
```

Swagger documentation:

```text
http://localhost:8000/docs
```

---

# ▶️ Start Spring Boot Backend

Open the Spring Boot project and run:

```bash
mvn spring-boot:run
```

Backend:

```text
http://localhost:8080
```

---

# ▶️ Start Angular Frontend

Navigate to the Angular project:

```bash
cd frontend/V-AI-AGENT
```

Install packages:

```bash
npm install
```

Start the development server:

```bash
ng serve
```

Open:

```text
http://localhost:4200
```

---

# 🔑 Environment Variables

Do not upload your real `.env` file to GitHub.

Example:

```env
DATABASE_URL=your_database_url
OLLAMA_MODEL=mistral:latest
```

Keep actual secrets only in your local environment.

---

# 🧪 Example AI Queries

The assistant can handle queries such as:

```text
What is my account balance?

Show my recent transactions.

What is my loan status?

Show my card details.

Calculate EMI for a 5 lakh loan.

What are the current FD interest rates?

Show my fixed deposits.

What is my account status?

Take me to the transactions page.
```

The assistant can also handle general conversations:

```text
Hello

How are you?

Explain what a fixed deposit is.
```

---

# 📊 Project Highlights

This project demonstrates practical implementation of:

* Full-stack development
* REST API architecture
* JWT authentication
* Banking database design
* AI integration
* Generative AI
* RAG
* Vector databases
* Semantic search
* Long-term AI memory
* Query classification
* Intelligent navigation
* Voice AI architecture
* Angular + Spring Boot + FastAPI integration

---

# 🔮 Future Improvements

Planned features include:

* WhatsApp integration
* Advanced voice commands
* Speech-to-Text improvements
* Text-to-Speech improvements
* Banking transaction actions
* Advanced fraud detection
* AI financial insights
* Notification system
* Admin dashboard
* Production deployment
* Cloud database integration

---

# 👨‍💻 Author

**Niranjana Barik**

B.Tech Computer Science Engineering

Odisha, India

---

## ⭐ Project

If you find this project useful, consider giving the repository a ⭐ on GitHub.
