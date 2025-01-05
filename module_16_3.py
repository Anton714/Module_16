from fastapi import FastAPI, Path
from typing import Annotated

app = FastAPI()

users = {"1": "Имя: Example, возраст: 18"}


@app.get("/")
async def get_all_users() -> dict:
    return users


@app.get("/user/{user_id}")
async def get_user(user_id: Annotated[(int, Path(description="Enter user_id", example="1"))]) -> str:
    return users[str(user_id)]


@app.post("/user/{username}/{age}")
async def create_user(username: Annotated[str, Path(min_length=5, max_length=20, description="Enter username",
                                                    example="UrbanUser")],
                      age: Annotated[int, Path(ge=18, le=120, description="Enter age", example="29")]) -> str:
    current_index = str(int(max(users, key=int)) + 1)
    users[current_index] = f"Имя: {username}, возраст: {age}."
    return f"User {current_index} is registered!"


@app.put("/user/{user_id}/{username}/{age}")
async def update_user(user_id: Annotated[(int, Path(description="Enter user_id", example="1"))],
                      username: Annotated[str,
                      Path(min_length=5, max_length=20, description="Enter username", example="UrbanUser")],
                      age: Annotated[int, Path(ge=18, le=120, description="Enter age", example="29")]) -> str:
    users[str(user_id)] = f"Имя: {username}, возраст: {age}."
    return f"User {user_id} has been updated."


@app.delete("/user/{user_id}")
async def delete_(user_id: Annotated[(int, Path(description="Enter user_id", example="1"))]) -> str:
    users.pop(str(user_id))
    return f"User {user_id} has been deleted."
