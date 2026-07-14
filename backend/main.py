from retriever import retrieve_context
from fastapi import FastAPI
from fastapi import HTTPException
from pydantic import BaseModel
from config import APP_NAME, LOG_FILE
from llm_client import ask_llm
from auth import register_user, authenticate
import requests
import logging

#configuring logging
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")

app = FastAPI(title=APP_NAME, description="An API for University Student Support Assistant using LLM", version="1.0.0")

class QuestionRequest(BaseModel):
    question: str

@app.get("/")
def home():
    return {"message": APP_NAME}

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "app": APP_NAME
        }

@app.post("/ask")
def submit_question(request: QuestionRequest):
    try:
        logging.info(f"Received question: {request.question}")
        answer = ask_llm(request.question)
        
        if answer is None:
            logging.error("LLM returned no response.")
            raise HTTPException(status_code=504,detail="LLM failed to respond. Please try again later.")
            
        logging.info(f"Generated answer: {answer}")
        return {"answer": answer}
    except Exception as e:
        logging.error(f"Error occurred while processing question: {str(e)}")
        print(e)
        raise HTTPException(status_code=500, detail="Internal server error")


class RegisterRequest(BaseModel):
    username: str
    password: str
    
    
class LoginRequest(BaseModel):
    username:str
    password:str
    
    
@app.post("/register")
def register(user: RegisterRequest):
    success = register_user(user.username, user.password)

    if not success:
        raise HTTPException(status_code=400, detail="This username already exists")

    logging.info(f"New user registered: {user.username}")
    
    return {"message": "Registration was successful! Welcome!"}
    

@app.post("/login")
def login(request:LoginRequest):
    success = authenticate(request.username, request.password)

    if not success:
        logging.warning(f"Failed attempted login: {request.username}")

        raise HTTPException(status_code=401,detail="Invalid credentials")

    logging.info(f"Successful login! Welcome, {request.username}")

    return {
        "message":"Login successful",
        "authenticated":True
    }
    
    
class Feedback(BaseModel):
    username:str
    question:str
    rating:str
    

@app.post("/feedback")
def feedback(data:Feedback):
    with open("feedback.txt","a") as file:
        file.write(f"""
            User:
            {data.username}

            Question:
            {data.question}

            Rating:
            {data.rating}

            ================

            """)

    return {"message":"Feedback recorded"}