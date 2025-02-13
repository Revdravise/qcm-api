import logging
import sys
from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os
import json
from dotenv import load_dotenv

# Charger la clé API OpenAI
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Vérifier si la clé API est bien chargée
if not OPENAI_API_KEY:
    raise ValueError("❌ Erreur : La clé API OpenAI n'est pas trouvée.")

# Initialisation de l'application Flask
app = Flask(__name__)
CORS(app)

# Configuration des logs
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("qcm_debug.log", mode="w", encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)

@app.route("/")
def home():
    return jsonify({"message": "✅ API Flask QCM opérationnelle !"})

@app.route("/generate-qcm", methods=["POST"])
def generate_qcm():
    """
    Endpoint pour générer un QCM basé sur un sujet donné.
    """
    subject = request.args.get("subject", "").strip()
    if not subject:
        return jsonify({"error": "Sujet manquant"}), 400

    logging.info(f"🔹 Génération du QCM pour : {subject}")

    try:
        client = openai.OpenAI(api_key=OPENAI_API_KEY)

        # Construire la requête pour OpenAI
        prompt = f"""
        Génère un QCM sur "{subject}" avec **exactement 5 questions**. 
        Réponds en JSON strict sous ce format :

        {{
            "qcm": [
                {{
                    "question": "Texte de la question",
                    "options": {{
                        "A": "Option A",
                        "B": "Option B",
                        "C": "Option C",
                        "D": "Option D",
                        "E": "Option E"
                    }},
                    "correct_answers": ["A", "C"],
                    "explanation": "Explication détaillée."
                }}
            ]
        }}

        Ne retourne que du JSON strict, sans texte additionnel.
        """

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "system", "content": "Tu es un assistant qui génère des QCM médicaux en JSON strict."},
                      {"role": "user", "content": prompt}],
            max_tokens=800,
            temperature=0.3,
        )

        # Récupérer la réponse brute de l'API OpenAI
        qcm_text = response.choices[0].message.content.strip()

        # DEBUG : Afficher immédiatement dans le terminal et les logs
        print(f"🔎 Réponse brute OpenAI : {qcm_text}")
        logging.info(f"✅ Réponse brute de l'API OpenAI : {qcm_text}")

        # Vérifier et convertir la réponse en JSON
        try:
            qcm_json = json.loads(qcm_text)

            # Vérifier si la structure est correcte
            if isinstance(qcm_json, dict) and "qcm" in qcm_json and isinstance(qcm_json["qcm"], list):
                logging.info("✅ Format JSON valide reçu.")
                return jsonify(qcm_json)
            else:
                logging.error("❌ Format JSON incorrect.")
                return jsonify({"error": "Format JSON incorrect"}), 500

        except json.JSONDecodeError:
            logging.error("❌ OpenAI a retourné un JSON invalide.")
            return jsonify({"error": "L'API OpenAI a retourné un JSON invalide."}), 500

    except Exception as e:
        logging.error(f"❌ Erreur QCM : {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8002, debug=True)
