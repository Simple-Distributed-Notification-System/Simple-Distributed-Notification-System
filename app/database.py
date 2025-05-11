# database.py

import uuid
from datetime import datetime, timezone
from motor.motor_asyncio import AsyncIOMotorClient
from app.config import MONGODB_URI_LOCAL, MONGODB_URI_REMOTE

# MongoDB setup
client = AsyncIOMotorClient(MONGODB_URI_LOCAL) # Uncomment this line to use local MongoDB
# client = AsyncIOMotorClient(MONGODB_URI_REMOTE)  # Uncomment this line to use remote MongoDB
db = client["Notification"]
collection_notification = db["NOTY"]  # collection name
collection_user = db["USERS"]  # collection name for users

async def insert_notification(message: str):
    id = str(uuid.uuid4())  
    date = datetime.now(timezone.utc).isoformat()

    cursor = collection_user.find({"subscribed": True})
    subscribed_ids = [user["_id"] async for user in cursor]

    await collection_notification.insert_one({
        "_id": id,
        "type": "notification",
        "message": message,
        "timestamp": date,
        "subscribed_clients": subscribed_ids
    })

    await collection_user.update_many(
        {"subscribed": True},
        {"$push": {
            "messages": {
                "_id": id,
                "message": message,
                "timestamp": date
            }
        }}
    )

async def get_notifications():
    notifications = await collection_notification.find().to_list(length=None)
    return notifications

async def get_all_users_subscribed():
    users = await collection_user.find({"subscribed": True}).to_list(length=None)
    return users

async def insert_user(user_id: str, email: str, token: str = None):
    await collection_user.insert_one({
        "_id": user_id,
        "type": "user",
        "email": email,
        "subscribed": False, 
        "messages": [],
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "timeLogin": datetime.now(timezone.utc).isoformat(),
        "token": token,
        "online": False
    })

async def get_all_users():
    users = await collection_user.find().to_list(length=None)
    return [
        {
            "user_id": user["_id"],
            "email": user["email"],
            "subscribed": user["subscribed"],
            "messages": user["messages"],
            "timestamp": user["timestamp"],
            "timeLogin": user["timeLogin"],
            "token": user["token"],
            "online": user.get("online", False)  # Use get with default for backward compatibility
        }
        for user in users
    ]    

async def get_user(email: str):
    user = await collection_user.find_one({"email": email})
    if user:
        return {
            "user_id": user["_id"],
            "email": user["email"],
            "subscribed": user["subscribed"],
            "messages": user["messages"],
            "timestamp": user["timestamp"],
            "timeLogin": user["timeLogin"],
            "token": user["token"],
            "online": user.get("online", False)  # Use get with default for backward compatibility
        }

async def update_user(user_id: str, token: str = None, subscribed: bool = None, online: bool = None):
    if subscribed != None:
        await collection_user.update_one({"_id": user_id}, {"$set": {"subscribed": subscribed}})
    if token:
        await collection_user.update_one({"_id": user_id}, {"$set": {"token": token}})
    if token == "None1":
        await collection_user.update_one({"_id": user_id}, {"$set": {"token": None}})
    if online != None:
        await collection_user.update_one({"_id": user_id}, {"$set": {"online": online}})
    
    await collection_user.update_one({"_id": user_id}, {"$set": {"timeLogin": datetime.now(timezone.utc).isoformat()}})