from fastapi import FastAPI, HTTPException, Depends, Request
from pydantic import BaseModel


app = FastAPI()

@app.get('/')
def home():
    return {"wel-come to pg application"}
