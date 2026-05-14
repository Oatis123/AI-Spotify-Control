# 🎵 AI Spotify Controller

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688.svg)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An intelligent microservice that allows you to control your Spotify playback using natural language. Powered by **FastAPI**, **LangGraph**, and **Spotipy**, this agent understands complex requests and executes them across your Spotify devices.

---

## ✨ Features

*   **🗣️ Natural Language Control:** Just tell the agent what to do: *"Play some jazz"*, *"Skip this track"*, or *"Find my 'Workout' playlist and play it"*.
*   **🧠 Intelligent Routing:** Uses **LangGraph** to maintain state and intelligently decide which tools to call based on your intent.
*   **⚡ Async Execution:** Commands are processed in the background, ensuring the API remains responsive.
*   **🔍 Advanced Search:** Search for tracks, albums, or playlists and play them instantly by ID or name.
*   **📱 Device Awareness:** Automatically targets your active Spotify device or a preferred one (configured in the controller).
*   **🔄 Playback Management:** Supports pause, resume, next, previous, shuffle, and repeat modes.

---

## 🏗️ Architecture

The project is structured as a modular microservice:

*   **`main.py`**: FastAPI entry point with background task orchestration.
*   **`agent/`**: The brain of the system.
    *   **`agent.py`**: Defines the LangGraph workflow and state management.
    *   **`tools/`**: Specialized Spotify tools and the low-level `SpotifyController`.
*   **Spotipy**: Handles OAuth2 authentication and Spotify Web API interaction.

---

## 🚀 Getting Started

### 1. Prerequisites

*   Python 3.10 or higher.
*   A [Spotify Developer](https://developer.spotify.com/dashboard/) account.

### 2. Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/your-username/AI-Spotify-Control.git
cd AI-Spotify-Control
pip install -r requirements.txt
```

### 3. Environment Setup

Create a `.env` file in the root directory and add your Spotify credentials:

```env
SPOTIPY_CLIENT_ID='your_client_id'
SPOTIPY_CLIENT_SECRET='your_client_secret'
SPOTIPY_REDIRECT_URI='http://localhost:8080'
```

*Note: Make sure the `REDIRECT_URI` is also whitelisted in your Spotify App Dashboard.*

---

## 🛠️ Usage

### Start the Server

```bash
python main.py
```
The API will be available at `http://localhost:8000`.

### Interaction Examples

**Check if the service is alive:**
```bash
curl http://localhost:8000/ping
```

**Execute a command:**
```bash
curl -X POST "http://localhost:8000/execute" \
     -H "Content-Type: application/json" \
     -d '{"command": "play some lofi hip hop"}'
```

**Control playback:**
```bash
curl -X POST "http://localhost:8000/execute" \
     -H "Content-Type: application/json" \
     -d '{"command": "skip to the next track and turn on shuffle"}'
```

---

## 🛠️ Configuration

You can set a preferred device in `agent/tools/spotify_controller.py`:

```python
sc = SpotifyController(device_name="Your-Device-Name")
```

---

## 📝 License

Distributed under the MIT License. See `LICENSE` for more information.

---

*Made with ❤️*
