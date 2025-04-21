# client.py

from fastapi import WebSocket, WebSocketDisconnect
from app.shared_tools import server_ws, subscribed_clients, clients, get_clients_count

async def websocket_client(websocket: WebSocket, user_id: str):
    await websocket.accept()
    clients.append(websocket)
    if server_ws[0]:
        await server_ws[0].send_text(await get_clients_count())
    try:
        while True:
            data = await websocket.receive_text()
            
            if data == "subscribe":
                subscribed_clients[user_id] = websocket
            elif data == "unsubscribe":
                subscribed_clients.pop(user_id, None)

            if server_ws[0]:
                await server_ws[0].send_text(await get_clients_count())

    except WebSocketDisconnect:
        clients.remove(websocket)
        subscribed_clients.pop(user_id, None)
        if server_ws[0]:
            await server_ws[0].send_text(await get_clients_count())

