# AI Spotify Control

An AI-powered microservice for controlling Spotify using natural language commands. This project uses FastAPI, LangChain/LangGraph, and the Spotify Web API (via Spotipy) to process user requests and execute playback actions.

## Features
- **Natural Language Control**: Pause, resume, skip tracks, and play specific songs or playlists using AI.
- **Spotify Integration**: Full control over playback state, track search, and playlist management.
- **REST API**: Simple FastAPI endpoints to interact with the AI agent.
- **Detailed Logging**: Built-in Python logging for monitoring agent actions and Spotify API calls.

## Prerequisites
- Python 3.10+
- A [Spotify Developer Account](https://developer.spotify.com/dashboard) to create an app and get API credentials.
- An [OpenRouter](https://openrouter.ai/) API key (or any OpenAI-compatible LLM provider).

## Setup

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/AI-Spotify-Control.git
cd AI-Spotify-Control
```

### 2. Environment Variables
Create a `.env` file in the root directory with the following variables:
```env
SPOTIPY_CLIENT_ID="your_spotify_client_id"
SPOTIPY_CLIENT_SECRET="your_spotify_client_secret"
SPOTIPY_REDIRECT_URI="http://127.0.0.1:8888/callback"
OPENROUTER_API_KEY="your_openrouter_api_key"
```
*Note: Ensure the `SPOTIPY_REDIRECT_URI` is added to your Spotify App's "Redirect URIs" in the developer dashboard.*

### 3. Installation
#### Using pip:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Running the Application
```bash
python main.py
```
The API will be available at `http://localhost:8000`.

## API Usage
### Execute Command
**POST** `/execute`
```json
{
  "command": "Play some jazz music"
}
```
**Response:**
```json
{
  "status": "success",
  "result": "Agent successfully processed the command: 'Play some jazz music'"
}
```

### Health Check
**GET** `/ping`
Returns `{"status": "ok", "message": "Spotify Agent is alive and kicking"}`

## Docker Usage
You can also run the application using Docker:

### Build the image:
```bash
docker build -t spotify-agent .
```

### Run the container:
```bash
docker run -p 8000:8000 --env-file .env spotify-agent
```

## Project Structure
- `main.py`: Entry point and FastAPI application.
- `agent/`: AI Agent logic using LangGraph.
  - `agent.py`: Graph definition and execution flow.
  - `tools/`: Spotify control tools.
    - `spotify_tools.py`: LangChain tools interface.
    - `spotify_controller.py`: Low-level Spotify API wrapper.
  - `prompt.py`: System instructions for the LLM.
- `requirements.txt`: Python dependencies.
- `Dockerfile`: Container configuration.
