# University Student Support Assistant using Large Language Models (LLMs)

## Overview

**University Student Support Assistant** is an AI-powered web app designed to help university students obtain information about student support services through natural language conversations. The system integrates a *Streamlit frontend*, *FastAPI backend*, and a locally hosted *Large Language Model (LLM)* using *Ollama*. Students can register then login, submit questions, receive AI generated responses and provide feedback on the quality of those responses. 

The aim of this project was mainly to demonstrate the integration of Artificial Intelligence with modern web application technologies so as to understand the complete pipeline for deploying an LLM-based system.


# Features

## Core features
* Student login and authentication
* AI-powered answering
* FastAPI
* Streamlit web interface
* Local LLM inference using Ollama
* Request validation using Pydantic
* Application logging
* Error handling

## Bonus features
* User authentication (to register and to login)
* Response evaluation (Good/Average/Poor)
* Storage of feedback
* API documentation using Swagger UI


# Technologies used
| Technology          | Purpose              |
| ------------------- | -------------------- |
| Python 3.12         | Programming language |
| Streamlit           | Frontend interface   |
| FastAPI             | Backend API          |
| Ollama              | Local LLM runtime    |
| Llama 3             | Language model       |
| Requests            | HTTP communication   |
| Pydantic            | Data validation      |
| Uvicorn             | ASGI server          |
| Logging             | System monitoring    |


# Project structure
student_support_llm/
│
├── backend/
│   ├── auth.py
│   ├── config.py
│   ├── llm_client.py
│   ├── main.py
│   ├── users.json
│   ├── feedback.txt
│   ├── log/
│   │   └── app.log
│
├── docs/
|   ├──screenshots
|
├── frontend/
│   └── app.py
│
├──tests/
|   └──test_api.py
|
├── venv/
│
├── requirements.txt
└── README.md


# System architecture
                 Student
                     │
            Streamlit frontend
                     │
                     │ HTTP Request
             FastAPI backend
                     │
      ┌──────────────┼──────────────┐
      │              │              │
 authentication   logging      Input validation
                     │
                Ollama LLM
                     │
            AI generated answer
                     │
             Response evaluation
                     │
               feedback.txt


# Installation

## 1. Clone the repository

```bash
git clone <repository-url>
cd student_support_llm

## 2. Creating virtual environment
```bash
python -m venv venv
venv\Scripts\activate

## 3. Install dependencies
pip install -r requirements.txt

## 4. Install Ollama

Download and install Ollama. After installation, verify:
ollama --version

## 5. Pull the language model
ollama pull llama3


# Running the Project

## Step 1
Start Ollama
ollama serve

## Step 2
Start the FastAPI backend
cd backend
uvicorn main:app --reload

Backend will run on http://127.0.0.1:8000

Swagger Documentation http://127.0.0.1:8000/docs

## Step 3

Activate the virtual environment on another terminal then navigate to the frontend.
cd frontend
python -m streamlit run app.py

Frontend will run on http://localhost:8501


# Authentication
New users can create an account through the Register page and also existing users can log in using their username and password. Only authenticated users are allowed to access the AI assistant.


#Asking questions
After login:
1. Enter a question.
2. Click **Submit** button.
3. The frontend sends the question to the FastAPI backend.
4. FastAPI forwards the request to Ollama.
5. The LLM generates a response.
6. The answer is displayed on the frontend.


#Response evaluation
After every generated answer, users can rate the response as:
* Good
* Average
* Poor
The feedback is then stored in **feedback.txt** for future analysis.


# Logging
Application events are recorded in:
backend/log/app.log

Examples of logged events include:

* Application startup
* User registration
* Login attempts
* Successful authentication
* Submitted questions
* AI response generation
* Feedback submissions


# API endpoints
| Method | Endpoint    | Description                           |
| ------ | ----------- | ------------------------------------- |
| POST   | `/register` | Register a new user                   |
| POST   | `/login`    | Authenticate user                     |
| POST   | `/submit`   | Submit a question to the AI assistant |
| POST   | `/feedback` | Save user feedback                    |


# Possible future improvements
Potential enhancements include:
* Password hashing using bcrypt
* JWT-based authentication
* Chat history
* Database integration (MySQL/PostgreSQL)
* Retrieval-Augmented Generation (RAG)
* University document search
* Multi-language support
* Speech-to-text and text-to-speech
* Cloud deployment


# Authors
**Group Members**
1. Catherine Mwita
2. Jolyine Ringo
3. Belva Kitaja
4. Rebecca Lengesia
5. Edgar Mainda


This project was developed for academic purposes as part of a university coursework assignment.
