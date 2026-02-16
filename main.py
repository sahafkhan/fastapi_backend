from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from uuid import uuid4

app = FastAPI(title="Feature Update API")

# ---- Model ----
class User(BaseModel):
    id: str
    name: str
    age: int

# In-memory storage
users: List[User] = []

# ---- Routes ----
@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/")
def root():
    return {"message": "API is running"}


@app.post("/users", response_model=User)
def create_user(name: str, age: int):
    new_user = User(id=str(uuid4()), name=name, age=age)
    users.append(new_user)
    return new_user

@app.get("/users", response_model=List[User])
def get_users():
    return users

@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: str):
    for user in users:
        if user.id == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")
