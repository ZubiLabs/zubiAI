from fastapi import FastAPI, APIRouter, HTTPException
from google.cloud import pubsub_v1
import uuid
from typing import List

# Firestore imports
from google.cloud import firestore

# Initialize FastAPI and Firestore
app = FastAPI()
db = firestore.Client()

# Firestore collection names
USERS_COLLECTION = "users"
AGENTS_COLLECTION = "agents"

# Define API routers
user_router = APIRouter()
agent_router = APIRouter()
task_router = APIRouter()

# Utility functions
def get_user_by_api_key(api_key: str):
    users_ref = db.collection(USERS_COLLECTION)
    query = users_ref.where("api_key", "==", api_key).stream()
    for user in query:
        return user
    return None

# User Registration
@user_router.post("/register_user")
def register_user(username: str, email: str):
    users_ref = db.collection(USERS_COLLECTION)

    # Check if user already exists
    existing_user = users_ref.where("username", "==", username).stream()
    if any(existing_user):
        raise HTTPException(status_code=400, detail="User already registered")

    # Generate a unique API key
    api_key = str(uuid.uuid4())

    # Save user in Firestore
    users_ref.add({
        "username": username,
        "email": email,
        "api_key": api_key,
    })

    return {"message": "User registered successfully", "username": username, "api_key": api_key}

# Agent Registration
@agent_router.post("/register_agent")
def register_agent(api_key: str, agent_name: str, capabilities: List[str]):
    # Validate API key
    user = get_user_by_api_key(api_key)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid API key")

    # Register the agent
    agent_id = str(uuid.uuid4())
    agents_ref = db.collection(AGENTS_COLLECTION)
    agents_ref.add({
        "user_id": user.id,
        "agent_id": agent_id,
        "agent_name": agent_name,
        "capabilities": capabilities,
    })

    return {"message": "Agent registered successfully", "agent_id": agent_id}

# Task Polling
@task_router.get("/poll_tasks")
def poll_tasks(api_key: str, agent_id: str):
    # Validate API key and agent
    user = get_user_by_api_key(api_key)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid API key")

    agents_ref = db.collection(AGENTS_COLLECTION)
    query = agents_ref.where("user_id", "==", user.id).where("agent_id", "==", agent_id).stream()
    if not any(query):
        raise HTTPException(status_code=401, detail="Invalid agent ID")

    # Poll tasks from Pub/Sub
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path("YOUR_PROJECT_ID", "tasks")
    response = subscriber.pull(subscription=subscription_path, max_messages=1)

    tasks = []
    for message in response.received_messages:
        tasks.append(message.message.data.decode("utf-8"))
        subscriber.acknowledge(subscription=subscription_path, ack_ids=[message.ack_id])

    if not tasks:
        return {"message": "No tasks available"}

    return {"message": "Tasks retrieved", "tasks": tasks}

# Include routers
app.include_router(user_router, prefix="/user", tags=["User"])
app.include_router(agent_router, prefix="/agent", tags=["Agent"])
app.include_router(task_router, prefix="/task", tags=["Task"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
