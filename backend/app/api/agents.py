from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List
import chromadb
from chromadb.config import Settings

# Initialize ChromaDB client
chroma_client = chromadb.Client(Settings(
    chroma_db_impl="duckdb+parquet",
    persist_directory="./chroma_data"  # Directory to persist data
))

# Ensure agent registry collection exists
collection_name = "agent_registry"
if collection_name not in chroma_client.list_collections():
    chroma_client.create_collection(name=collection_name)
agent_collection = chroma_client.get_collection(name=collection_name)

# Initialize Router
router = APIRouter()

# Pydantic model for agent registration
class Agent(BaseModel):
    name: str = Field(..., example="SummarizerAgent")
    capabilities: List[str] = Field(..., example=["text-summarization"])
    api_url: str = Field(..., example="http://localhost:8001/api")
    cost_per_query: float = Field(..., ge=0.0, example=0.01)
    currency: str = Field(..., example="USD")

# Register a new agent
@router.post("/register")
def register_agent(agent: Agent):
    try:
        # Add agent to ChromaDB
        agent_id = f"{agent.name}-{agent.api_url}"  # Unique ID for the agent
        agent_collection.add(
            ids=[agent_id],
            metadatas=[{
                "name": agent.name,
                "api_url": agent.api_url,
                "cost_per_query": agent.cost_per_query,
                "currency": agent.currency,
                "capabilities": agent.capabilities
            }]
        )
        return {"message": "Agent registered successfully", "agent_id": agent_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

# Retrieve all agents
@router.get("/")
def get_agents():
    try:
        agents = agent_collection.get(include=["metadatas", "ids"])
        return [{"id": agent["id"], **agent["metadata"]} for agent in agents]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
