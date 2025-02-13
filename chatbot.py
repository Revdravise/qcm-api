from fastapi import FastAPI, Query
import openai
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
import logging

# Charger les variables d'environnement
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialiser FastAPI
app = FastAPI()

# Activer CORS pour autoriser le frontend à communiquer avec l'API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Logger pour voir les requêtes dans la console
logging.basicConfig(level=logging.INFO)

@app.get("/")
def read_root():
    return {"message": "Chatbot médical opérationnel !"}

@app.post("/ask")
def ask_question(question: str = Query(...)):
    """
    Endpoint pour poser une question à GPT-4.
    """
    logging.info(f"Question reçue : {question}")
    try:
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Tu es un assistant médical. Réponds de manière claire et bien structurée, en séparant les points clés par des sauts de ligne."},
                {"role": "user", "content": question}
            ],
            max_tokens=800,  # ✅ Augmenté pour éviter les coupures
            temperature=0.7
        )
        answer = response.choices[0].message.content.strip()
        logging.info(f"Réponse envoyée : {answer}")
        return {"answer": answer}
    except Exception as e:
        logging.error(f"Erreur API : {e}")
        return {"error": str(e)}
