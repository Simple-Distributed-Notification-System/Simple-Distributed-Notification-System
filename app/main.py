# main.py

from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from app.server import websocket_server
from app.client import websocket_client

app = FastAPI()

app.mount("/pages", StaticFiles(directory="pages"), name="pages")

@app.get("/")
async def get_client_page():
    with open("pages/client.html", "r", encoding="utf-8") as f:
        return HTMLResponse(f.read())

@app.get("/server/{id}")
async def get_server_page(id: str):
    if id != "hi":
        return HTMLResponse("Invalid access")
    
    with open("pages/server.html", "r", encoding="utf-8") as f:
        return HTMLResponse(f.read())

@app.websocket("/ws/client/{user_id}")
async def websocket_client_route(websocket: WebSocket, user_id: str):
    await websocket_client(websocket, user_id)

@app.websocket("/ws/server")
async def websocket_server_route(websocket: WebSocket):
    await websocket_server(websocket)
