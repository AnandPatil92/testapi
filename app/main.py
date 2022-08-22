import json

from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import JSONResponse
#from fastapi_jwt_auth import AuthJWT
#from fastapi_jwt_auth.exceptions import AuthJWTException
from pydantic import BaseModel

from app.models.users import Users

from mongoengine import connect

from pymongo import MongoClient
# import pymongo
import dns
from app.config import settings

# client = MongoClient("mongodb+srv://patilanandgmailcom:Anand8431756067@cluster0.lagmjmk.mongodb.net/pgmanangement?retryWrites=true&w=majority")
# #client = MongoClient("mongodb+srv://patilanandgmailcom:Anand8431756067@cluster0.lagmjmk.mongodb.net/db = client.test")
# print(client)

# cluster = "mongodb+srv://patilanandgmailcom:Anand8431756067@cluster0.lagmjmk.mongodb.net/pgmanangement?retryWrites=true&w=majority"
# print(cluster, "connection successful")
# cluster =
#cluster = MongoClient("mongodb+srv://patilanandgmailcom:Anand8431756067@cluster0.lagmjmk.mongodb.net/pgmanagement?retryWrites=true&w=majority")

cluster = "mongodb+srv://patilanandgmailcom:Anand8431756067@cluster0.lcom2x4.mongodb.net/pgapp?ssl=true&retryWrites=true&w=majority"
client = MongoClient(cluster, connect=False)

db = client["pgapp"]

collection = db["users"]

# connect(db, alias='default')
#local connection
connect(db="pgapp", host=cluster, port=27017)

app = FastAPI()


class User(BaseModel):
    username: str
    password: str

class New_users(BaseModel):
    full_name: str
    email: str
    hashed_password: str
    is_active: bool


# in production you can use Settings management
# from pydantic to get secret key from .env
class Settings(BaseModel):
    authjwt_secret_key: str = "ec7cf2d5016eb824699a364543de8b4c2399b7eb96b1beda8a20e2fcc62c6dfe"

# callback to get your configuration
# @AuthJWT.load_config
# def get_config():
#     return Settings()

# exception handler for authjwt
# in production, you can tweak performance using orjson response
# @app.exception_handler(AuthJWTException)
# def authjwt_exception_handler(request: Request, exc: AuthJWTException):
#     return JSONResponse(
#         status_code=exc.status_code,
#         content={"detail": exc.message}
#     )

# provide a method to create access tokens. The create_access_token()
# function is used to actually generate the token to use authorization
# later in endpoint protected
@app.get('/')
def home():
    return {"wel-come to pg application"}

# @app.post('/login', tags=['test'])
# def login(user: User, Authorize: AuthJWT = Depends()):
#     if user.username != "admin" or user.password != "admin":
#         raise HTTPException(status_code=401,detail="Bad username or password")
#
#     # subject identifier for who this token is for example id or username from database
#     access_token = Authorize.create_access_token(subject=user.username)
#     return {"access_token": access_token}

# protect endpoint with function jwt_required(), which requires
# a valid access token in the request headers to access.
# @app.get('/user')
# def user(Authorize: AuthJWT = Depends()):
#     Authorize.jwt_required()
#
#     current_user = Authorize.get_jwt_subject()
#     return {"user": current_user}

@app.post("/add_users")
def add_new_user(user_new: New_users):
    new_users = Users(full_name=user_new.full_name,
                      email=user_new.email,
                      hashed_password=user_new.hashed_password,
                      is_active=user_new.is_active)

    new_users.save()
    return {"Message": "New user added"}


@app.get('/users')
def get_all_users():
    user = Users.objects().to_json()
    print(user)
    user_list = json.loads(user)
    # print(user_list)
    return {"Users": user_list}

@app.get('/get_users/{email}')
def get_single_user(email):
    users_details = Users.objects.get(email=email)
    user_details_dict = {
                            "full_name": users_details.full_name,
                            "email": users_details.email,
                            "hashed_password": users_details.hashed_password,
                            "is_active": users_details.is_active
                        }

    return user_details_dict


@app.get('/search_user')
def search_users(email):
    users = json.loads(Users.objects.filter(email=email).to_json())
    return {"users": users}