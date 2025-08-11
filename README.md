<div align="center">

# 🚀 Live Project

**A real-time multimodal AI assistant built with Google Gemini API**

[![Python](https://img.shields.io/badge/Python-3.12+-3776ab?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![UV](https://img.shields.io/badge/UV-Package%20Manager-4051b5?style=for-the-badge)](https://docs.astral.sh/uv/)
[![Google Gemini](https://img.shields.io/badge/Google%20Gemini-AI-4285f4?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev/)
[![WebSocket](https://img.shields.io/badge/WebSocket-Real--time-ff6b6b?style=for-the-badge)](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API)

---

*Featuring WebSocket-based communication, audio streaming, and Google Sheets integration*

</div>

## ✨ Features

- 🤖 **Real-time AI Chat**: WebSocket-based communication with Google Gemini AI
- 🎙️ **Audio Support**: Real-time audio recording and streaming capabilities
- 📊 **Google Sheets Integration**: Direct integration with Google Sheets via cloud functions
- 🎯 **Multimodal Interface**: Support for text, audio, and media interactions
- 📱 **Mobile Responsive**: Optimized for both desktop and mobile devices
- ☁️ **Cloud Functions**: Serverless backend processing with Google Cloud Functions

## 📁 Project Structure

```
📦 live-project
├── 🌐 client/               # Frontend web application
│   ├── 📂 src/             # JavaScript modules (API, audio, media, utils)
│   ├── 🎨 styles/          # CSS styling for desktop and mobile
│   └── 📄 index.html       # Main application entry point
├── 🐍 server/              # Python WebSocket server
│   ├── ⚙️ config/          # Configuration and system instructions
│   ├── 💎 core/            # Core server modules (WebSocket, Gemini client, etc.)
│   └── 🚀 server.py        # Main server entry point
├── ☁️ cloud-functions/     # Google Cloud Functions
│   └── 📊 sheet-assistant/ # Google Sheets integration function
└── 📋 pyproject.toml       # UV package configuration
```

## 📋 Prerequisites

- 🐍 **Python 3.12+**
- 📦 **UV** package manager ([installation guide](https://docs.astral.sh/uv/getting-started/installation/))
- 🔧 **Git**
- ☁️ **Google Cloud Account** (for Gemini API and Cloud Functions)

## 🚀 Getting Started

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/Shridhar7-8/live-project.git
cd live-project
```

### 2️⃣ Install Dependencies

Using UV to manage dependencies (no manual virtual environment needed):

```bash
# Install all dependencies - UV handles the virtual environment automatically
uv sync
```

### 3️⃣ Configure Environment Variables

Create a `.env` file in the `server/` directory:

```bash
cd server
# Copy the example environment file (if available) or create new one
touch .env
```

Add your configuration to `.env`:
```env
GEMINI_API_KEY=your_gemini_api_key_here
LOG_LEVEL=INFO
# Add other required environment variables
```

### 4️⃣ Run the Server

```bash
# UV automatically handles the virtual environment
uv run server/server.py
```

> 🎯 The WebSocket server will start on the default port (usually 8765).

### 5️⃣ Run the Client

Open the client in a web browser:

```bash
# Serve the client directory with a simple HTTP server
cd client

# Option 1: Using UV to run Python's built-in server
uv run python -m http.server 8080

# Option 2: Using Node.js (if available)
npx serve .

# Option 3: Simply open index.html in your browser
# For local development, you can open file:///path/to/client/index.html
```

> 🌐 Visit `http://localhost:8080` in your browser to access the application.

## 🛠️ Development

### 📦 Adding Dependencies

Use UV to add new Python dependencies:

```bash
# Add a new dependency
uv add package-name

# Add a development dependency
uv add --dev package-name

# Update dependencies
uv sync
```


## ⚙️ Configuration

- 🖥️ **Server Configuration**: Edit `server/config/config.py`
- 🤖 **System Instructions**: Modify `server/config/system-instruction.txt` for AI behavior
- 🌐 **Client Configuration**: Update API endpoints in `client/src/api/gemini-api.js`

