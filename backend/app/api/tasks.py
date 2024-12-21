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

# Load agent registry collection
collection_name = "agent_registry"
agent_collection = chroma_client.get_collection(name=collection_name)

# Initialize Router
router = APIRouter()

# Pydantic model for task submission
class Task(BaseModel):
    description: str = Field(..., example="Summarize EU renewable energy policies.")
    required_capabilities: List[str] = Field(..., example=["data-fetching", "text-summarization"])

# Submit a task and find matching agents
@router.post("/submit")
def submit_task(task: Task):
    try:
        # Query ChromaDB for matching agents
        results = agent_collection.query(
            query_texts=[" ".join(task.required_capabilities)],  # Query capabilities
            n_results=5  # Top 5 matches
        )

        # Format the response
        matches = [
            {
                "agent_id": result["id"],
                "name": result["metadata"]["name"],
                "api_url": result["metadata"]["api_url"],
                "cost_per_query": result["metadata"]["cost_per_query"],
                "currency": result["metadata"]["currency"],
                "capabilities": result["metadata"]["capabilities"]
            }
            for result in results["documents"]
        ]

        if not matches:
            return {"message": "No matching agents found", "task_description": task.description}

        return {
            "message": "Matching agents found",
            "task_description": task.description,
            "matches": matches
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
