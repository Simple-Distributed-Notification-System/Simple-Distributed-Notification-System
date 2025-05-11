import json
import uuid
from email_validator import validate_email, EmailNotValidError
from datetime import datetime, timedelta, timezone
from starlette import status
from fastapi import WebSocket, WebSocketDisconnect
from app.shared_tools import server_ws, subscribed_clients, clients , get_clients_count
from app.message import send_email
from app.database import insert_user, get_user, update_user

async def websocket_client(websocket: WebSocket):
    user_id = None 
    try:
        
        await websocket.accept()
        login = False

        if server_ws[0]:
            await server_ws[0].send_text(await get_clients_count())

        while True:
            data = await websocket.receive_text()

            data = json.loads(data)
            action = data.get("action")
            
            if action == "user_id":
                user_id = data.get("user_id")

            if action == "login":
                email = data.get("email")

                try:
                    validate_email(email)

                except EmailNotValidError as e:
                    await websocket.send_json({"type": "error_email", "message": f"Invalid email format: {str(e)}"})
                    continue

                user = await get_user(email)

                if user:
                    login = True
                    user_id = user["user_id"]

                    if user["token"] is not None:
                        await websocket.send_json({"type": "error_token", "message": "Token already sent."})
                        continue

                    last_login_time = datetime.fromisoformat(user["timeLogin"]).replace(tzinfo=timezone.utc)
                    current_time = datetime.now(timezone.utc)

                    time_diff = current_time - last_login_time
                    if time_diff >= timedelta(minutes=5):
                        token = str(uuid.uuid4())
                        await update_user(user_id, token=token, online=False) 
                        await send_email(user["email"], token)  
                        await websocket.send_json({"type": "success", "message": "Token sent to your email."})
                        continue
                    else:
                        await update_user(user_id, online=True)
                        await websocket.send_json({"type": "success", "message": "Login successful."})
                        await websocket.send_json({
                            "type": "success",
                            "isSubscribed": user.get("subscribed", False),
                            "messages": user.get("messages", [])
                        })                    
                    if user["subscribed"]:
                        subscribed_clients[user_id] = websocket
                else:
                    user_id = str(uuid.uuid4())
                    token = str(uuid.uuid4())
                    await insert_user(user_id, email, token)
                    await send_email(email, token)
                    await websocket.send_json({"type": "success", "message": "Account created. Token sent to your email."})
                    continue

                clients[user_id] = websocket

            elif action == "subscribe" and login:
                subscribed_clients[user_id] = websocket
                await update_user(user_id, subscribed=True)
                await websocket.send_json({
                    "type": "success",
                    "isSubscribed": True,
                    "message": "Subscribed successfully"
                })

            elif action == "unsubscribe" and login:
                subscribed_clients.pop(user_id, None)
                await update_user(user_id, subscribed=False)
                await websocket.send_json({
                    "type": "success",
                    "isSubscribed": False,
                    "message": "Unsubscribed successfully"
                })

            if server_ws[0]:
                await server_ws[0].send_text(await get_clients_count())

    except WebSocketDisconnect:
        if user_id:
            clients.pop(user_id, None)
            subscribed_clients.pop(user_id, None)
            await update_user(user_id, online=False)
            if server_ws[0]:
                await server_ws[0].send_text(await get_clients_count())

    except Exception as e:
        if user_id:
            print(f"WebSocket Error ({user_id}):", e)
            clients.pop(user_id, None)
            subscribed_clients.pop(user_id, None)
            await update_user(user_id, online=False)
            if server_ws[0]:
                try:
                    await server_ws[0].send_text(await get_clients_count())
                except:
                    pass
