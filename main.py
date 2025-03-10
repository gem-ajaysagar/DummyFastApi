from pydantic import BaseModel
from typing import Optional
from fastapi import FastAPI, HTTPException
import random
import time


# Initialize FastAPI app
app = FastAPI(
    title="My API",
    description="This is my awesome FastAPI application",
    version="0.1.0",
    # docs_url=None,  # Disable Swagger UI
    # redoc_url=None,  # Disable ReDoc
)

# Pydantic model to handle POST data
class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

# GET endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI!"}
    # raise HTTPException(status_code=500, detail="Internal Server Error")

# POST endpoint
@app.post("/items/")
def create_item(item: Item):
    total_price = item.price + (item.tax if item.tax else 0)
    return {"name": item.name, "total_price": total_price, "description": item.description}

# Route that intentionally raises a 500 Internal Server Error
@app.get("/internal-server-error")
def internal_server_error():
    raise HTTPException(status_code=500, detail="Internal Server Error")

# Route that intentionally raises a 408 Request Timeout
@app.get("/timeout-error")
def timeout_error():
    time.sleep(5)  # Simulate a long-running operation
    raise HTTPException(status_code=408, detail="Request Timeout")

# Route that intentionally raises a 400 Bad Request with custom error
@app.get("/bad-request")
def bad_request():
    raise HTTPException(status_code=400, detail="Bad Request - Invalid Input")

# Route that randomly raises an error for demonstration
@app.get("/random-error")
def random_error():
    error_type = random.choice(["500", "408", "400"])
    if error_type == "500":
        raise HTTPException(status_code=500, detail="Random Internal Server Error")
    elif error_type == "408":
        time.sleep(5)  # Simulate timeout error
        raise HTTPException(status_code=408, detail="Random Timeout Error")
    else:
        raise HTTPException(status_code=400, detail="Random Bad Request Error")

# uvicorn main:app --reload
