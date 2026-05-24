# N8tive AI Agent Framework

A full-stack, cloud-ready AI Agent Framework where users can create and interact with customizable AI agents — each with unique roles, tones, and purposes.

## 🏗️ Architecture

- **Frontend**: React + Vite + Tailwind CSS + Framer Motion
- **Backend**: FastAPI (Python 3.10+) on AWS EC2
- **Database**: SQLite (local) or PostgreSQL (production)
- **Model**: OpenAI-compatible API (expandable to Claude, Llama, etc.)
- **Hosting**: EC2 with Nginx reverse proxy and HTTPS via Certbot

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ and npm
- Python 3.10+
- OpenAI API key (or compatible API)

### Quick Start (Recommended)

Use the provided startup scripts:

**Terminal 1 - Backend:**
```bash
cd "N8tive AI"
./start-backend.sh
```

**Terminal 2 - Frontend:**
```bash
cd "N8tive AI"
./start-frontend.sh
```

The backend will run on `http://localhost:8000` and frontend on `http://localhost:5173`.

### Manual Setup

#### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file from `.env.example`:
```bash
cp .env.example .env
```

5. Edit `.env` and add your API keys:
```env
OPENAI_API_KEY=your_openai_api_key_here
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000
USE_DATABASE=true
```

6. Run the backend server:
```bash
uvicorn main:app --reload
```

The backend will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create `.env` file from `.env.example`:
```bash
cp .env.example .env
```

4. Edit `.env` and set the API URL:
```env
VITE_API_URL=http://localhost:8000
```

5. Run the development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:5173`

## 📁 Project Structure

```
N8tive AI/
├── backend/
│   ├── main.py              # FastAPI application entry point
│   ├── routes/
│   │   ├── chat.py          # Chat endpoint with streaming
│   │   ├── agents.py        # Agent CRUD operations
│   │   └── config.py        # Configuration endpoint
│   ├── utils/
│   │   ├── model_handler.py # OpenAI API handler
│   │   └── memory_manager.py # Database and memory management
│   ├── data/                # SQLite database and JSON storage
│   ├── requirements.txt     # Python dependencies
│   └── .env.example         # Environment variables template
│
└── frontend/
    ├── src/
    │   ├── components/
    │   │   ├── ChatWindow.jsx    # Main chat interface
    │   │   ├── ChatBubble.jsx    # Individual message bubbles
    │   │   ├── Sidebar.jsx       # Agent list and navigation
    │   │   ├── SettingsModal.jsx # Agent creation/editing
    │   │   └── AgentCard.jsx     # Agent display card
    │   ├── utils/
    │   │   └── api.js            # API communication utilities
    │   ├── App.jsx              # Main application component
    │   └── main.jsx             # Application entry point
    ├── package.json
    └── .env.example
```

## 🔧 Features

### Core Features

- **Multi-Agent Support**: Create and manage multiple AI agents with unique personalities
- **Customizable Agents**: Set name, role, system prompt, tone, temperature, and model
- **Streaming Chat**: Real-time token streaming for responsive conversations
- **Persistent Memory**: Each agent maintains its own chat history
- **Export Conversations**: Export chats as TXT or JSON
- **Dark/Light Mode**: Toggle between themes
- **Modern UI**: Beautiful interface with Framer Motion animations

### API Endpoints

#### Chat
- `POST /api/chat` - Send a message and get streaming response

#### Agents
- `GET /api/agents` - List all agents
- `GET /api/agents/{agent_id}` - Get specific agent
- `POST /api/agents` - Create new agent
- `PUT /api/agents/{agent_id}` - Update agent
- `DELETE /api/agents/{agent_id}` - Delete agent
- `GET /api/agents/{agent_id}/history` - Get chat history
- `DELETE /api/agents/{agent_id}/history` - Clear chat history

#### Config
- `GET /api/config` - Get available models and settings

## 🌐 Deployment

### AWS EC2 Deployment

See [DEPLOYMENT.md](./DEPLOYMENT.md) for detailed deployment instructions.

### Quick Deployment Steps

1. Set up EC2 instance with Ubuntu 22.04
2. Install Python, Node.js, and Nginx
3. Clone repository and configure environment variables
4. Set up Nginx reverse proxy
5. Configure SSL with Certbot
6. Set up systemd services for backend
7. Build and serve frontend

## 🔒 Security

- API keys stored in `.env` files (never committed)
- CORS configured for allowed origins only
- HTTPS required for production
- Input validation on all endpoints
- Rate limiting recommended (add middleware)

## 📝 Development

### Running Tests

Backend:
```bash
cd backend
pytest
```

Frontend:
```bash
cd frontend
npm test
```

### Building for Production

Frontend:
```bash
cd frontend
npm run build
```

The built files will be in `frontend/dist/`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

MIT License

## 🆘 Support

For issues and questions, please open an issue on the repository.

