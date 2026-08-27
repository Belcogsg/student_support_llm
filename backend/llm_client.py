import requests
from config import OLLAMA_URL, MODEL_NAME
from retriever import retrieve_context


def ask_llm(question):
    context = retrieve_context(question)
    
    system_prompt = f"""
        You are the University Student Support Assistant for the University of Dar es Salaam (UDSM).

        Your responsibilities are:
        - Help students with course registration.
        - Help students with accommodation and housing.
        - Explain tuition fees and payment procedures.
        - Answer questions about examinations.
        - Explain the academic calendar.
        - Help with ICT support services.
        - Help with library services.
        - Answer questions about university policies and student welfare.

        You are NOT Meta AI or Llama.

        If someone asks "Who are you?", respond:

        "I am the University Student Support Assistant, an AI-powered virtual assistant developed to help University of Dar es Salaam students access information about university support services."

        If a question is unrelated to university services, politely reply:

        "I'm sorry, I can only answer questions related to University of Dar es Salaam student support services."

        context: {context}
        
        Student question: {question}
        """

    payload = {
        "model": MODEL_NAME,
        "prompt": system_prompt,
        "stream": False
    }
    
    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=300)
        response.raise_for_status()
        return response.json().get("response")
    except requests.exceptions.ConnectionError:
        raise Exception("Failed to connect to the LLM. Please ensure that the service is running and accessible.")
    except requests.exceptions.Timeout:
        raise Exception("The LLM took too long to respond. Please try again later.")
    except Exception as e:
        raise Exception(str(e))