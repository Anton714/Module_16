from fastapi import FastAPI, status, Body, HTTPException, Path
from pydantic import BaseModel, Field
from typing import List, Annotated


app = FastAPI()

users = []


class User(BaseModel):
    id: int = None
    username: str
    age: int


@app.get("/users", response_model=List[User])
async def get_all_users() -> List[User]:
    return users


@app.post("/user/{username}/{age}",  response_model=User)
async def create_user(username: Annotated[str, Path(min_length=5, max_length=20, description="Enter username",
                                                    example="UrbanUser")],
                      age: Annotated[int, Path(ge=18, le=120, description="Enter age", example="29")]) -> User:
    new_id = max((i.id for i in users), default=0) + 1

    new_user = User(id=new_id, username=username, age=age)
    users.append(new_user)
    return new_user

@app.put("/user/{user_id}/{username}/{age}")
async def update_user(user_id: Annotated[int, Path(description="Enter user_id", example="1")],
                      username: Annotated[str,
                      Path(min_length=5, max_length=20, description="Enter username", example="UrbanUser")],
                      age: Annotated[int, Path(ge=18, le=120, description="Enter age", example="29")]) :
    for user in users:
        if user.id == user_id:
            user.username = username
            user.age = age
            return user
    raise HTTPException(status_code=404, detail="User not found.")


@app.delete("/user/{user_id}")
async def delete_user(user_id: Annotated[int, Path(ge=1, le=1111, description="Enter user_id", example="1")]):
    for user in users:
        if user.id == user_id:
            users.remove(user)
            return user
    raise HTTPException(status_code=404, detail="User was not found")



#  uvicorn module_16_4:app