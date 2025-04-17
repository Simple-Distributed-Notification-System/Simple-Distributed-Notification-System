# Real-time Notification & Chat App with FastAPI + WebSocket

This project is a real-time WebSocket-based system built using FastAPI for the backend and HTML/CSS/JavaScript for the frontend. It enables real-time updates between a server and multiple clients. The server tracks the number of connected users and subscribers and supports sending/receiving notifications.

---

## Project Structure
   ```bash
    Project/
    │
    ├── app/
    │   ├── main.py             # FastAPI entry point
    │   ├── server.py           # Handles WebSocket logic for the server dashboard
    │   ├── client.py           # Handles WebSocket logic for client subscribers
    │   └── shared_tools.py     # Shared utilities for managing WebSocket connections
    │
    ├── pages/
    │   ├── client.html         # Client UI (subscriber interface)
    │   ├── server.html         # Server UI (dashboard to view counts/messages)
    │   ├── css/
    │   │   ├── client.css      # Styling for client UI
    │   │   └── server.css      # Styling for server UI
    │   ├── js/
    │   │   ├── client.js       # JavaScript for client-side WebSocket handling
    │   │   └── server.js       # JavaScript for server-side WebSocket handling
    │   └── images/
    │       └── Server Background.png  # Optional background image
    │
    └── README.md               # Project documentation
  ```
---

## Features

- Real-time bi-directional communication using WebSockets  
- Live tracking of connected clients and subscribers  
- Clients can send messages/notifications to the server  
- Server dashboard displays messages and user counts in real time  
- Responsive web-based UI with FastAPI backend

---

## Requirements

- Python 3.8+  
- FastAPI  
- Uvicorn

Install dependencies:

  ```bash
  pip install fastapi uvicorn
  ```

---

## Running the Project

1. Navigate to the project directory:
  ```bash
    cd Project
  ```
2. Start the FastAPI server:
  ```bash
    python -m uvicorn app.main:app --reload
  ```
3. Open your browser and visit:

- Server Dashboard: http://127.0.0.1:8000/server  
- Client Page: http://127.0.0.1:8000/

---

## WebSocket Routes

- /ws/server: WebSocket connection for the server dashboard  
- /ws/client: WebSocket connection for individual clients

---

## How It Works

- Clients connect and subscribe via the /ws/client WebSocket route  
- The server connects via /ws/server to monitor and manage communication  
- Clients can send notifications, and the server updates connection stats in real time  
- All communication is handled live using WebSockets for instant feedback

---

## TODO (Optional Enhancements)

- Add user authentication for clients  
- Store and display message history  
- Show timestamps for each message  
- Improve UI responsiveness on mobile devices
