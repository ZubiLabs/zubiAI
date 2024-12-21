from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.agents import router as agents_router
from app.api.tasks import router as tasks_router

# Initialize FastAPI app
app = FastAPI(
    title="zubiAI Backend",
    description="Backend service for zubiAI platform",
    version="1.0.0"
)

# Configure CORS (optional, adjust origins as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with specific origins for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(agents_router, prefix="/agents", tags=["Agents"])
app.include_router(tasks_router, prefix="/tasks", tags=["Tasks"])

# Health check endpoint
@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok", "message": "Service is running"}

# Run app locally (if using `python main.py`)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
