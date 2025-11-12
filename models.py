# This file defines what your tables look like in the database
from sqlalchemy import Column, Integer, Boolean, Integer, ForeignKey, String # These are SQLAlchemy datatypes and tools to define columns for my table 
from database import Base # remember, this is the parent class that lets SQLAlchemy know these are tables


class Question(Base): # this represents the question table in postgres
    __tablename__= "question" # name of this table 
    
    id = Column(Integer, primary_key= True , index= True) # this column is having id that will be integer
    question_text = Column(String, index= True)# this column is having question_text that will be string

    # relationship with choice table 
    #choice = relationship("Choice" , back_populates= "question" , cascade= "all, delete")

class Choice(Base): #this represents the choice table in postgres
    __tablename__= "choice" # this will be the name of the table

    id = Column(Integer , primary_key= True , index= True) # this column is having id that will be integer 
    choice_text = Column(String , index= True) # this column is having chice text that will be string 

    is_correct = Column(Boolean , default = False) # this column is having is_correct  that will be boolean
    question_id = Column(Integer, ForeignKey("question.id"))  # this column is having id ForeignKey("question.id") means this choice belongs to a specific question.

    # relationship back to the question table 
    #question = relationship("Question" , back_populates = "choice")