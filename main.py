import logging
import time
from fastapi import Body, FastAPI , HTTPException, Request , status
from pydantic import BaseModel
from typing import Annotated
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


user_dataBase = {"Isaac": {"FirstName": "Isaac" , "LastName": "Ughanze" , "Age": 22 , "Email": "ifennaisaac@gmail.com" , "Height": 162}}


app.add_middleware(
    CORSMiddleware, 
    allow_origins = ["http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class SignUp(BaseModel):
    FirstName: str
    LastName: str
    Age: int
    Email: str
    Height: float



logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("request_logger")


@app.middleware("http")
async def log_request_time(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    logger.info(f"Request to {request.url} took {duration:.4f} seconds.")
    return response


@app.post("/SignUp" ,status_code= status.HTTP_201_CREATED)
async def sign_up(user:Annotated[SignUp, Body()]):
    if user.FirstName in user_dataBase and user_dataBase[user.FirstName]["email"] == user.email:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email and username already exist"
        )
    
    
    user_dataBase[user.FirstName] = user.model_dump()
    
    return  "Profile created successfully"


@app.get("/user" , status_code=status.HTTP_200_OK)
async def get_users():
    return user_dataBase


