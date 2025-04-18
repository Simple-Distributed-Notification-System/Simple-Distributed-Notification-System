# shared_tools.py

import json

server_ws = [None]
clients = []
subscribed_clients = {}  

async def notify_clients_subscribed(message: str):
    for client in subscribed_clients.values():
        await client.send_text(message)

async def send_count():
    return json.dumps({
        "type": "counts",
        "subscribers": len(subscribed_clients),
        "clients": len(clients),
    })

# في shared_tools.py
async def get_clients_data():
    return {
        "type": "clients",
        "subscribers": list(subscribed_clients.keys()),
        "clients": len(clients),
    }
