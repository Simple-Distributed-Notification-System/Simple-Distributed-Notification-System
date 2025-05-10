# database.py

import uuid
from datetime import datetime, timezone
from motor.motor_asyncio import AsyncIOMotorClient
from app.shared_tools import get_clients_data
from app.config import MONGODB_URI_LOCAL, MONGODB_URI_REMOTE

# MongoDB setup
# client = AsyncIOMotorClient(MONGODB_URI_LOCAL) # Uncomment this line to use local MongoDB
client = AsyncIOMotorClient(MONGODB_URI_REMOTE)  # Uncomment this line to use remote MongoDB
db = client["Notification"]
collection_notification = db["NOTY"]  # collection name
collection_user = db["USERS"]  # collection name for users

async def insert_notification(message: str):
    clients_data = await get_clients_data()
    await collection_notification.insert_one({
        "_id": str(uuid.uuid4()),  # Use UUID for unique ID generation
        "type": "notification",
        "message": message,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "subscribed_clients": clients_data["subscribers"],
    })

async def get_notifications():
    notifications = await collection_notification.find().to_list(length=None)
    return notifications

async def insert_user(user_id: str, email: str, token: str = None):
    await collection_user.insert_one({
        "_id": user_id,
        "type": "user",
        "email": email,
        "subscribed": False, 
        "msg": [],
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "timeLogin": datetime.now(timezone.utc).isoformat(),
        "token": token,
    })

async def get_all_users():
    users = await collection_user.find().to_list(length=None)
    return [
        {
            "user_id": user["_id"],
            "email": user["email"],
            "subscribed": user["subscribed"],
            "msg": user["msg"],
            "timestamp": user["timestamp"],
            "timeLogin": user["timeLogin"],
            "token": user["token"],
        }
        for user in users
    ]

async def update_all_users_subscribed(msg: str):
    await collection_user.update_many(
        {"subscribed": True},
        {"$push": {"msg": msg}}
    )

async def get_user(email: str):
    user = await collection_user.find_one({"email": email})
    if user:
        return {
            "user_id": user["_id"],
            "email": user["email"],
            "subscribed": user["subscribed"],
            "msg": user["msg"],
            "timestamp": user["timestamp"],
            "timeLogin": user["timeLogin"],
            "token": user["token"],
        }

async def update_user(user_id: str, token: str = None, msg: list = None, subscribed: bool = None):
    if msg:
        await collection_user.update_one({"_id": user_id}, {"$set": {"msg": msg}})
    if subscribed != None:
        await collection_user.update_one({"_id": user_id}, {"$set": {"subscribed": subscribed}})
    if token:
        await collection_user.update_one({"_id": user_id}, {"$set": {"token": token}})
    if token == "None1":
        await collection_user.update_one({"_id": user_id}, {"$set": {"token": None}})
    
    await collection_user.update_one({"_id": user_id}, {"$set": {"timeLogin": datetime.now(timezone.utc).isoformat()}})