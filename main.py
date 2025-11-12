from fastapi import FastAPI, Depends
from pydantic import BaseModel
from typing import List, Annotated
import models
from database import engine, Sessionlocal
from sqlalchemy.orm import  Session
from fastapi import HTTPException

app = FastAPI()
models.Base.metadata.create_all(bind=engine)  # tells SQLAlchemy to create all tables in the database if they don’t exist.


class ChoiceBase(BaseModel):  # Pydantic Schemas: These define how incoming JSON data should look when a user sends a request.
    choice_text: str
    is_correct: bool


class QuestionBase(BaseModel):
    question_text: str
    choices: List[ChoiceBase]

#  now adding the response model 
'''class ChoiceResponse(BaseModel):
    id: int
    choice_text: str
    is_correct: bool

    class Config: 
        orm_mode = True  # allows directly reading from SQLAlchemy models
        # tells pydentic it can read from Sqlalchemy model object (not just dict)

# now adding the response model to return questions
class QuestionResponse(BaseModel): # this response model also includes nested choice
    id : int
    question_text : str
    choices : List[ChoiceResponse]
    
    class Config:
        orm_mode = True
'''

def get_db():  # This function creates and closes the database session.
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)] #This tells FastAPI:

#“Whenever you see db: db_dependency in a route, call get_db() and inject the database session here.”


@app.get("/view_question/{question_id}")
async def view_question(question_id: int, db: db_dependency):
    result = db.query(models.Question).filter(models.Question.id == question_id).first()
    if not result :
        raise HTTPException(status_code=404, detail="Question not found")   
    return result

@app.get("/view_choice/{question_id}")
async def view_choice(question_id: int , db: db_dependency):
    result = db.query(models.Choice).filter(models.Question.id == question_id).all()
    if not result:
        raise HTTPException(status_code=404, detail="Choice not found")
    return result

@app.post("/questions/")
async def create_questions(question: QuestionBase, db: db_dependency):
    db_question = models.Question(question_text=question.question_text)
    db.add(db_question)
    db.commit()
    db.refresh(db_question)

    # Add all the choices for this question
    for choice in question.choices:
        db_choice = models.Choice(
            choice_text=choice.choice_text,
            is_correct=choice.is_correct,
            question_id=db_question.id,
        )
        db.add(db_choice)

    db.commit()  # ✅ Commit all choices
    db.refresh(db_question)

    db_question.choices = db.query(models.Choice).filter(models.Choice.question_id == db_question.id).all()
    return db_question
    


    #return {"message": "Question created successfully", "question_id": db_question.id}


'''# now making get endpoint
@app.get("/view_question/" , response_model = List[QuestionResponse]) # tells fastapi to automatically format the output using pydentic
async def view_question(db: db_dependency): # before calling this function first call get_db() to open session of database
    questions = db.query(models.Question).all() # this will get all the questions from the database
    return questions # fastapi automatically converts the sqlalchemy objects -> python dict -> Json response'''

