
import uvicorn
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pathlib import Path

from src.internal.db import initialize_db,initialize_db_aws
from src.repository.users import UserRepository
from src.router.user import UsersRouter

app = FastAPI()
# db = initialize_db()
db = initialize_db_aws()

user_repository = UserRepository(db)
user_router = UsersRouter(user_repository)

app.include_router(user_router.router)
temp_dir = Path.joinpath(Path.cwd(),"src/views")
templates = Jinja2Templates(directory=temp_dir)


@app.get('/',response_class=HTMLResponse)
async def index(request: Request):
    message = "Welcome to SETU Modules Portal"
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "message": message,
        })

if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=5002, log_level="info", reload=True)