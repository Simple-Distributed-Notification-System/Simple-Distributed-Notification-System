import json
from datetime import datetime, timezone
from app.database import get_all_users, get_all_users_subscribed


server_ws = [None]
clients = {}
subscribed_clients = {}  

async def get_clients_count():
    return json.dumps({
        "type": "counts",
        "clients": len(await get_all_users()),
        "subscribersOnline": len(subscribed_clients),
        "online": len(clients),
        "allSubscribers": len(await get_all_users_subscribed()),
    })

async def notify_clients_subscribed(message: str):
    for client in subscribed_clients.values():
        try:
            await client.send_json({
                "type": "notification",
                "message": message,
                "timestamp": datetime.now(timezone.utc).isoformat()
            })
        except Exception as e:
            print(f"Failed to notify client: {e}")
