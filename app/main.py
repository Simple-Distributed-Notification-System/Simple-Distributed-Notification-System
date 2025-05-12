import os
from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from app.server import websocket_server
from app.client import websocket_client
from app.config import ID_SERVER, SERVER_URL
from app.database import get_user, update_user

app = FastAPI()

# Start from the Page 
app.mount("/pages", StaticFiles(directory="pages"), name="pages")


@app.get("/")
async def get_client_page():
    with open("pages/client.html", "r", encoding="utf-8") as f:
        return HTMLResponse(f.read())

# Verifies the token sent to the email and matches the token with the client's email
@app.get("/token/{email}/{token}")
async def update_token(token: str, email: str):
    user = await get_user(email)
    if user and user.get("token") == token:
        await update_user(user_id=user["user_id"], token="None1")
        return HTMLResponse("Token verified successfully!")
    return HTMLResponse("Invalid token or email")

@app.get("/server/{id}")
async def get_server_page(id: str):
    # Check if server password is written correctly
    if id != ID_SERVER:
        return HTMLResponse("Invalid access")
    
    with open("pages/server.html", "r", encoding="utf-8") as f:
        return HTMLResponse(f.read())

# Client's Page with the websocket connection
@app.websocket("/ws/client")
async def websocket_client_route(websocket: WebSocket):
    await websocket_client(websocket)

# Server's Page with the websocket connection
@app.websocket("/ws/server")
async def websocket_server_route(websocket: WebSocket):
    await websocket_server(websocket)


if __name__ == "__main__":
    import uvicorn

    print(f"Client Page {SERVER_URL}")
    print(f"Server page: {SERVER_URL}/server/{ID_SERVER}")

    cert_path = os.path.join("app", "certs", "cert.pem")
    key_path = os.path.join("app", "certs", "key.pem")

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        ssl_certfile=cert_path,
        ssl_keyfile=key_path
    )