from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os

app = FastAPI()

@app.get("/")
async def root():
    return {"deploy "}