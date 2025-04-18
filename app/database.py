# database.py

from datetime import datetime, timezone
import uuid
from motor.motor_asyncio import AsyncIOMotorClient
from app.shared_tools import get_clients_data
from app.config import MONGODB_URI_LOCAL

# MongoDB setup
# client = AsyncIOMotorClient() # mongodb atlas server
client = AsyncIOMotorClient(MONGODB_URI_LOCAL)  # local mongodb server
db = client["Notification"]
collection = db["test"]  # collection name

async def insert_notification(message: str):
    clients_data = await get_clients_data()
    await collection.insert_one({
        "_id": str(uuid.uuid4()),
        "type": "notification",
        "message": message,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "subscribed_clients": clients_data["subscribers"]
    })

async def get_notifications():
    notifications = await collection.find().to_list(length=None)
    return notifications