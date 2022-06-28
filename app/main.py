from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models 
from .database import engine 
from .routers import posts, users , auth , votes
#from .config import settings

models.Base.metadata.create_all(bind=engine)  # If you use alembic you don't 
                                              # need this line

app = FastAPI() 

origins = ["*"]     # This means it is a puclic API. 
                    #  Any domain can access the application
                    #  if we would want to restrict the origin to google 
                    #  we would set it to google.com


app.add_middleware(         
    CORSMiddleware,
    allow_origins=origins,   # we define which domains can "talk" to our app
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(votes.router)

@app.get("/")
def root():
    return {"message": "Hello World"}


    
# Check documentation http://localhost:8000/docs