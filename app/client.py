from fastapi import WebSocket, WebSocketDisconnect
from starlette import status
from app.shared_tools import server_ws, subscribed_clients, clients, get_clients_count

async def websocket_client(websocket: WebSocket, user_id: str):
    await websocket.accept()

    if user_id in clients:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION, reason="User already connected.")
        return

    clients[user_id] = websocket

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
        clients.pop(user_id, None)
        subscribed_clients.pop(user_id, None)
        if server_ws[0]:
            await server_ws[0].send_text(await get_clients_count())
