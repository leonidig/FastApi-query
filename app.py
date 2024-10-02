from fastapi import FastAPI, Header, Path, Query
from typing import Optional
from datetime import datetime

app = FastAPI()

@app.get("/users/{user_id}")
async def greet_user(
    user_id: int = Path(..., description="Enter Your User ID"),
    timestamp: Optional[str] = Query(None, description="Enter Time Stamp Or Empty", alias="Time-Stamp"),  
    x_client_version: str = Header(description="Enter X-Client-Version", alias="X-Client-Version")  
):
    if timestamp is None:
        timestamp = datetime.now().isoformat()

    return {
        "greeting": f"hi, user {user_id}",
        "user_id": user_id,
        "timestamp": timestamp,
        "X-Client-Version": x_client_version
    }
