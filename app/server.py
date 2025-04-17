# server.py

import json
from fastapi import WebSocket, WebSocketDisconnect
from app.shared_tools import server_ws, subscribed_clients, notify_clients_subscribed, send_count

async def websocket_server(websocket: WebSocket):
    try:
        await websocket.accept()
        server_ws[0] = websocket
        await notify_clients_subscribed("Server connected")

        while True:
            data = await websocket.receive_text()
            msg = json.loads(data)
            action = msg.get("action")

            if action == "notify":
                message = msg.get("message", "")
                await notify_clients_subscribed(message)

            elif action == "count":
                await send_count()

    except WebSocketDisconnect:
        server_ws[0]= None
        await notify_clients_subscribed("Server disconnected")
