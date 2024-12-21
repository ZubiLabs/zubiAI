from fastapi import FastAPI, HTTPException, Request
from typing import Callable, Dict, Any
import uvicorn

class ZubiAgent:
    def __init__(self, name: str, capabilities: list, cost_per_query: float, currency: str):
        self.name = name
        self.capabilities = capabilities
        self.cost_per_query = cost_per_query
        self.currency = currency
        self.task_handler: Callable[[Dict[str, Any]], Dict[str, Any]] = None
        self.app = FastAPI()

        # Define a health check endpoint
        @self.app.get("/health")
        def health_check():
            return {"status": "ok", "message": f"{self.name} is running"}

        # Define the task endpoint
        @self.app.post("/task")
        async def handle_task(request: Request):
            if not self.task_handler:
                raise HTTPException(status_code=500, detail="Task handler not implemented")
            try:
                task_data = await request.json()
                return self.task_handler(task_data)
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

    def set_task_handler(self, handler: Callable[[Dict[str, Any]], Dict[str, Any]]):
        """
        Register the task handler for processing incoming tasks.
        """
        self.task_handler = handler

    def run(self, host: str = "0.0.0.0", port: int = 8000):
        """
        Start the agent's API server.
        """
        uvicorn.run(self.app, host=host, port=port)
