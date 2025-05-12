
# Real-time Notification System with WebSocket

This project is a real-time WebSocket-based system built with Websocket + FastAPI (Backend) and HTML/CSS/JavaScript (frontend). It enables real-time communication between a server and multiple clients, supporting live notifications.

---

## 🔧 Project Structure

```bash
Project/
│
├── app/                           # Backend 
│   ├── certs/                     # SSL/TLS certificates
│   │   ├── cert.pem
│   │   └── key.pem
│   ├── main.py                    # Websocket + FastAPI entry point
│   ├── config.py                  # Environment configurations
│   ├── database.py                # MongoDB operations
│   ├── server.py                  # Server WebSocket logic
│   ├── client.py                  # Client WebSocket logic
│   ├── msg.py                     # Email notifications handler
│   └── shared_tools.py            # Shared utilities
│
├── pages/                         # Frontend (HTML/CSS/JS)
│   ├── client.html
│   ├── server.html
│   ├── css/
│   │   ├── client.css
│   │   ├── common.css
│   │   └── server.css
│   ├── js/
│   │   ├── client.js
│   │   └── server.js
│   └── images/
│       ├── Server Background.png
│       ├── favicon_client.ico
│       ├── favicon_server.ico
│       └── favicon_login.ico
│
├── .env                           # Environment variables
├── .gitignore                     # Files ignored by Git
├── requirements.txt               # Python libraries
└── README.md                      # Project documentation
```

---

## 🚀 Features

- Real-time bi-directional communication (WebSockets)
- Live tracking of connected users
- Server dashboard shows live data and messages
- Responsive web UI using FastAPI backend

---

## 📦 Requirements

- Python 3.8+
- FastAPI
- uvicorn
- websockets
- python-dotenv
- pymongo
- pydantic
- bcrypt
- motor

---

## ▶️ Running the Project

1. Clone the repository:
  
    ```bash
      git clone https://github.com/Simple-Distributed-Notification-System/Simple-Distributed-Notification-System.git
    ```

2. Navigate into the directory:

    ```bash
      cd Project
    ```

3. Install dependencies:

    ```bash
      pip install -r requirements.txt
    ```

4. Run the server:

    ```bash
      python -m app.main
    ```

5. Open your browser to:

   - Server Dashboard: <https://127.0.0.1:8000/server/{ID_SERVER}>
   - Client Page: <https://127.0.0.1:8000/>

---

## 🔌 WebSocket Routes

- `/ws/server` — for server dashboard communication
- `/ws/client` — for client subscriptions

---

## 📚 How It Works

- Clients subscribe via `/ws/client`
- Server monitors via `/ws/server`
- Server broadcasts updates and shows real-time stats

---

## 📌 Future Enhancements

- Enable file sharing (e.g., images, documents) by server to clients
- Improve error handling and reconnection strategy
- Add theme support (dark/light mode) 
- Optimize performance for high concurrent clients
