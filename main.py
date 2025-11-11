from fastapi import FastAPI, Depends
from pydantic import BaseModel
from typing import List, Annotated
import models
from database import engine, Sessionlocal
from sqlalchemy.orm import  Session

app = FastAPI()
models.Base.metadata.create_all(bind=engine)  # tells SQLAlchemy to create all tables in the database if they don’t exist.


class ChoiceBase(BaseModel):  # Pydantic Schemas: These define how incoming JSON data should look when a user sends a request.
    choice_text: str
    is_correct: bool


class QuestionBase(BaseModel):
    question_text: str
    choices: List[ChoiceBase]


def get_db():  # This function creates and closes the database session.
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)] #This tells FastAPI:

#“Whenever you see db: db_dependency in a route, call get_db() and inject the database session here.”


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

    return {"message": "Question created successfully", "question_id": db_question.id}
