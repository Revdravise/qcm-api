import json
from fastapi import FastAPI, Query
import openai
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permet à tout le monde d'accéder temporairement (remplace "*" par ton domaine en production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Récupérer la clé API OpenAI
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("⚠️ ERREUR : Aucune clé API OpenAI trouvée ! Vérifie ton fichier `.env`.")

# Initialisation du client OpenAI
client = openai.OpenAI(api_key=api_key)

# --------------------------------------------------------------
# ✅ 1️⃣ Endpoint `/ask` → Pose une question libre sur un sujet médical
# --------------------------------------------------------------
@app.post("/ask")
def ask_question(question: str = Query(..., description="Pose une question médicale")):
    """
    Répond à une question médicale posée par l'utilisateur.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Tu es un assistant médical qui répond de manière claire et concise."},
                {"role": "user", "content": question}
            ],
            max_tokens=500,
            temperature=0.7
        )
        return {"answer": response.choices[0].message.content.strip()}
    
    except Exception as e:
        return {"error": str(e)}

# --------------------------------------------------------------
# ✅ 2️⃣ Endpoint `/generate-qcm` → Génère un QCM interactif basé sur un sujet médical
# --------------------------------------------------------------
@app.post("/generate-qcm")
def generate_qcm(subject: str = Query(..., description="Le sujet du QCM")):
    """
    Génère un QCM médical avec 5 questions, 5 choix (A-E), et plusieurs bonnes réponses possibles.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Tu es un expert en pédagogie médicale. "
                                              "Génère un QCM de 5 questions sur un sujet donné. "
                                              "Chaque question doit contenir 5 propositions (A, B, C, D, E). "
                                              "La réponse E doit toujours être 'Toutes les propositions sont fausses'. "
                                              "Plusieurs réponses correctes sont possibles. "
                                              "Retourne une liste des réponses correctes et une explication. "
                                              "Réponds en JSON au format : "
                                              "{'qcm': [{'question': '...', 'options': {'A': '...', 'B': '...', 'C': '...', 'D': '...', 'E': 'Toutes les propositions sont fausses'}, 'correct_answers': ['A', 'C'], 'explanation': '...'}]}"},
                {"role": "user", "content": f"Génère un QCM médical sur : {subject}"}
            ],
            max_tokens=800,
            temperature=0.5
        )
        
        # ✅ Convertir la réponse en vrai JSON
        qcm_data = json.loads(response.choices[0].message.content.strip())
        return qcm_data  # ✅ Maintenant, c'est un vrai JSON et pas une string !

    except json.JSONDecodeError:
        return {"error": "⚠️ Erreur de format JSON - OpenAI a retourné un texte incorrect."}
    
    except Exception as e:
        return {"error": str(e)}
