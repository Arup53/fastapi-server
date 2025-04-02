from fastapi import FastAPI
from pydantic import BaseModel

app= FastAPI() ;

class User(BaseModel):
    name: str
    age : int

@app.get('/')
async def home():
    return {"message":'koi'}

@app.post('/users', response_model=User)
async def create_users(user:User):
  return user