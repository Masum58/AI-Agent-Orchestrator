# AI Agent Service

A robust, intelligent AI Agent Chat Service built with FastAPI. This service orchestrates conversational AI interactions with long-term memory integration using Pinecone vector database and OpenAI models.

##  Features

- **Conversational Memory**: Retains context across chats using Pinecone Vector Database.
- **AI Orchestrator**: Manages prompts, models, and query executions.
- **RESTful API**: Fast and scalable API endpoints built with FastAPI.
- **Multi-User Support**: Tracks user specific conversation IDs and history.
- **Logging & Monitoring**: Built-in middleware for request logging and error handling.

##  Memory Architecture (RAG)

This project implements a Retrieval-Augmented Generation (RAG) pattern, incorporating a robust two-tier memory system:

### 1. Short-term Memory (Instance Memory)
- **Purpose**: Keeps track of the immediate conversational context.
- **How it works**: Fetches the **last 5 messages** of the current user session from the database.
- **Benefit**: Allows the AI to understand pronouns (e.g., "it", "they") and follow-up questions seamlessly within the active conversation.

### 2. Long-term Memory (Experience Memory)
- **Purpose**: Persistently stores and retrieves historical knowledge and user preferences across multiple sessions.
- **How it works**: Uses a hybrid approach combining:
  - **Traditional Database**: Retrieves exact keyword matches.
  - **Pinecone Vector Database**: Performs semantic search (fetching the top 15 results) to find contextually relevant past interactions across all sessions.
- **Benefit**: Ensures the AI "learns" from the user over time. By pulling and deduplicating data from both sources into the prompt, the agent remembers preferences and historical context.

Whenever an interaction occurs, the new user query and AI response are automatically saved to *both* the traditional database and the Pinecone Vector Space, ensuring continuous learning.

## 🛠️ Tech Stack

- **Framework**: FastAPI
- **LLM Provider**: OpenAI
- **Vector Database**: Pinecone
- **Server**: Uvicorn
- **HTTP Client**: HTTPX / Requests

## 📋 Prerequisites

Make sure you have the following installed:
- Python 3.9+
- OpenAI API Key
- Pinecone API Key

## ⚙️ Installation

1. **Clone the repository** (if applicable) or navigate to the project directory:
   ```bash
   cd ai-agent-service_jaysea_aus
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install the dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## 🔐 Environment Variables

Create a `.env` file in the root directory based on the project requirements. You will need:
```env
OPENAI_API_KEY=your_openai_api_key
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_ENV=your_pinecone_environment
# Add other necessary config vars as needed
```

##  Running the Application

Run the application locally using Uvicorn:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The application will be accessible at: `http://localhost:8000`

## 📖 API Documentation

Once the server is running, FastAPI provides interactive API documentation automatically:
- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

### Key Endpoints:

#### 1. Health Check
- **Endpoint**: `GET /`
- **Description**: Verifies if the service is running.

#### 2. AI Chat
- **Endpoint**: `POST /chat`
- **Description**: Send a message to the AI agent and receive a response.
- **Payload Example**:
  ```json
  {
    "user_query": "Hello, how can you help me?",
    "conversation_id": "conv_12345",
    "user_id": "user_789"
  }
  ```

## 📁 Project Structure

```text
├── app/
│   ├── orchestrator/      # Agent logic and execution flow
│   ├── services/          # External API integrations (Pinecone, OpenAI)
│   ├── core/              # Core configurations and logging
│   └── context/           # Prompt builders and context management
├── main.py                # FastAPI application entry point
├── requirements.txt       # Project dependencies
└── .env                   # Environment configurations
```
