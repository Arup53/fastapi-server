# for db schema defining

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Questions(Base):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True, index=True)
    question_text = Column(String, index=True)

class Choices(Base):
    __tablename__ = 'choices'

    id = Column(Integer, primary_key=True, index=True)
    choice_text = Column(String, index=True)
    is_correct = Column(Boolean, default=False)
    question_id = Column(Integer, ForeignKey("questions.id"))


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)

    # Relationship to Complaints
    complaints = relationship("Complaints", back_populates="user", cascade="all, delete")

class Complaints(Base):
    __tablename__ = "complaints"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    complain_text = Column(Text, nullable=False, index=True)  # Using Text for longer complaints
    complain_tone = Column(String, index=True, nullable=True)  # Can be 'negative', 'neutral', 'positive'
    complain_tone_score = Column(Float, index=True, nullable=True)  # Score should be float for better precision
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    # Relationship with Users
    user = relationship("Users", back_populates="complaints")
    
  