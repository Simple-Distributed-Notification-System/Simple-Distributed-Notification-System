# clint.py

import asyncio
import json
import uuid
from email_validator import validate_email, EmailNotValidError
from datetime import datetime, timedelta, timezone
from starlette import status
from fastapi import WebSocket, WebSocketDisconnect
from app.shared_tools import server_ws, subscribed_clients, clients, guests , get_clients_count
from app.message import send_email
from app.database import insert_user, get_user, update_user

async def websocket_client(websocket: WebSocket):
    user_id = None  # Initialize user_id to avoid reference before assignment
    try:
        # Accept the new WebSocket connection
        await websocket.accept()
        guests[websocket] = True
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
                    # Validate the email format
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

                    # Check if 5 minutes have passed since the last login
                    time_diff = current_time - last_login_time
                    if time_diff >= timedelta(minutes=5):
                        token = str(uuid.uuid4())
                        await update_user(user_id, token=token, online=False)  # Update token
                        await send_email(user["email"], token)  # Send email with token
                        await websocket.send_json({"type": "success", "message": "Token sent to your email."})
                        continue
                    else:
                        # Update last login time
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

                # Update to new user ID
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
        # Handle the WebSocket disconnect event
        if user_id:
            guests.pop(websocket, None)
            clients.pop(user_id, None)
            subscribed_clients.pop(user_id, None)
            await update_user(user_id, online=False)
            if server_ws[0]:
                await server_ws[0].send_text(await get_clients_count())

    except Exception as e:
        # Handle other exceptions
        if user_id:
            print(f"WebSocket Error ({user_id}):", e)
            # Clean up in case of error
            guests.pop(websocket, None)
            clients.pop(user_id, None)
            subscribed_clients.pop(user_id, None)
            await update_user(user_id, online=False)
            if server_ws[0]:
                try:
                    await server_ws[0].send_text(await get_clients_count())
                except:
                    pass
