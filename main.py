from fastapi import FastAPI,HTTPException, Depends
from pydantic import BaseModel,EmailStr, Field
from typing import List,Annotated, Optional
import models
from models import Users, Complaints, Resolved
from database import engine, SessionLocal
from sqlalchemy.orm import Session


app= FastAPI() ;
models.Base.metadata.create_all(bind=engine)

class User(BaseModel):
    name: str = Field(..., min_length=1)
    email: EmailStr  # Validates format automatically
 
class Complaint(BaseModel):
    complain_text: str = Field(..., min_length=5)
    complain_tone: Optional[str] = None  # optional if tone analysis is done later
    complain_tone_score: Optional[float] = None  # optional for same reason
    user_email: EmailStr

class ResolutionCreate(BaseModel):
    resolved: str = Field(default="processing")  # Default value for API input
    complaint_id: int    

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()   

db_dependency= Annotated[Session, Depends(get_db)]

# @app.get('/')
# async def home():
#     return {"message":'koi'}

# @app.post('/users', response_model=User)
# async def create_users(user:User):
#   return user

# @app.post("/questions/")
# async def create_questions(question: QuestionBase, db: db_dependency):
#     db_question = models.Questions(question_text=question.question_text)
#     db.add(db_question)
#     db.commit()
#     db.refresh(db_question)  # Ensure the ID is available after commit

#     for choice in question.choices:
#         db_choice = models.Choices(choice_text=choice.choice_text, is_correct=choice.is_correct, question_id=db_question.id)
#         db.add(db_choice)

#     db.commit()
#     return {"message": "Question and choices added successfully"}      

@app.post("/users/")
def create_user(user: User, db: Session = Depends(get_db)):
    # Check for existing email
    existing_user = db.query(Users).filter(Users.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists")

    new_user = Users(name=user.name, email=user.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {
        "id": new_user.id,
        "name": new_user.name,
        "email": new_user.email
    }


@app.post("/complaints/")
def create_complaint(complaint: Complaint, db: Session = Depends(get_db)):
    # Check if the user exists by email
    user = db.query(Users).filter(Users.email == complaint.user_email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Create the complaint
    new_complaint = Complaints(
        complain_text=complaint.complain_text,
        complain_tone=complaint.complain_tone,
        complain_tone_score=complaint.complain_tone_score,
        user_email=complaint.user_email,
    )
    db.add(new_complaint)
    db.commit()
    db.refresh(new_complaint)

    # Automatically create a resolution entry with "processing" status
    new_resolution = Resolved(
        resolved="processing",
        complaint_id=new_complaint.id  # Link to the newly created complaint
    )
    db.add(new_resolution)
    db.commit()
    db.refresh(new_resolution)

    return {
        "complaint": new_complaint,
        "resolution": new_resolution
    }