from sqlalchemy import create_engine #this import the function to create a connection between python and your database
from sqlalchemy.orm import sessionmaker #creates a session which is like an active connection that allows you to [ add data, read data, update data , delete data ]
from sqlalchemy.ext.declarative import declarative_base # this is used to define models[basically database tables] using python classes


# databse connection url
URL_DATABASE = 'postgresql://postgres:admin@localhost:5432/QuizApplicationYT'

#creates the connection engine that knows how to talk with postgreSQL
engine = create_engine(URL_DATABASE)

# a function that gives you database session
# parameter info: autocommit = false we can manually controll when data get saved
Sessionlocal = sessionmaker(autocommit= False , autoflush= False , bind=engine )

Base = declarative_base()# this creates base class that we will use to create models

