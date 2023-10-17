import uvicorn
from typing import List
from uuid import uuid4
from fastapi import FastAPI
from models import Gender, Role, User
app = FastAPI()

# default_credit=100
# db: List[User] = [
#     User(
#     id=uuid4(),
#     first_name="John",
#     last_name="Doe",
#     gender=Gender.male,
#     aws_credit =default_credit,
#     roles=[Role.user],
#     ),
#     User(
#     id=uuid4(),
#     first_name="Jane",
#     last_name="Doe",
#     gender=Gender.female,
#     aws_credit =default_credit,
#     roles=[Role.user],
#     ),
#     User(
#     id=uuid4(),
#     first_name="James",
#     last_name="Gabriel",
#     gender=Gender.male,
#     aws_credit =default_credit,
#     roles=[Role.user],
#     ),
#     User(
#     id=uuid4(),
#     first_name="Eunit",
#     last_name="Eunit",
#     gender=Gender.male,
#     aws_credit =default_credit,
#     roles=[Role.lecturer, Role.user],
#     ),
# ]

@app.get("/")
async def root():
    return {"greeting":"Welcome to Cloud Architecture Module"}

# @app.get("/api/v1/users")
# async def get_users():
#     return db

# @app.post("/api/v1/users")
# async def create_user(user: User):
#  db.append(user)
#  return {"id": user.id}


if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=5001, log_level="info", reload=True)