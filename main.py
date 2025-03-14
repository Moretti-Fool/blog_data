from fastapi import FastAPI, HTTPException
from starlette.responses import RedirectResponse
from schemas import UserCreate, UserUpdate


app = FastAPI()
users = []


@app.get("/")
def root():
    return RedirectResponse(url="/docs")

@app.post("/users/")
def create_user(user: UserCreate):
    """Creates a new user and stores it in memory."""
    user_id = len(users)
    user_dict = user.model_dump()
    user_dict["id"] = user_id
    users.append(user_dict)
    return {"message": "User created successfully", "user": user_dict}

@app.get("/users/")
def read_users():
    """Retrieves all users."""
    return users

@app.get("/users/{user_id}")
def read_user(user_id: int):
    """Fetches a user by their ID. Returns 404 if the user is not found."""
    if user_id >= len(users) or user_id < 0:
        raise HTTPException(status_code=404, detail="User not found")
    return users[user_id]

@app.put("/users/{user_id}")
def update_user(user_id: int, user: UserUpdate):
    """Updates a user's name and/or email. Returns 404 if the user is not found."""
    if user_id >= len(users) or user_id < 0:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user.name:
        users[user_id]["name"] = user.name
    if user.email:
        users[user_id]["email"] = user.email
    
    return {"message": "User updated successfully", "user": users[user_id]}

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    """Deletes a user by ID. Returns 404 if the user is not found."""
    if user_id >= len(users) or user_id < 0:
        raise HTTPException(status_code=404, detail="User not found")
    
    users.pop(user_id)
    return {"message": "User deleted successfully"}

