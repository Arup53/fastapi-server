from fastapi import FastAPI,HTTPException, Depends
from pydantic import BaseModel
from typing import List,Annotated

app= FastAPI() ;

class User(BaseModel):
    name: str
    age : int

class ChoiceBase(BaseModel):
   choice_text = str 
   is_correct = bool

class QuestionBase(BaseModel):
   question_text= str
   choices: List[ChoiceBase]


@app.get('/')
async def home():
    return {"message":'koi'}

@app.post('/users', response_model=User)
async def create_users(user:User):
  return user