import sys
import os

sys.path.insert(0,
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

from fastapi.testclient import TestClient
from backend.main import app

#creating a test client for the FastAPI app
client = TestClient(app)

def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "University Student Support Assistant API"}
    
    
def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_submit_question():
    response = client.post("/ask", json={"question": "How to apply for student accommodation?"})
    assert response.status_code == 200
    
    data = response.json()
    
    assert "answer" in data
    assert len(data["answer"]) > 0  #the answer should not be empty
    

def test_submit_question_invalid():
    response = client.post("/ask", json={"question": ""})  # sending an empty question
    assert response.status_code == 422  # Unprocessable Entity due to validation error