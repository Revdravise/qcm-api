import openai
import os
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = openai.OpenAI(api_key=OPENAI_API_KEY)

prompt = """
Génère un QCM sur le sujet suivant : "le système nerveux".
Le QCM doit contenir **exactement 5 questions**.
Réponds uniquement avec un JSON strict sous ce format :

{
    "qcm": [
        {
            "question": "Texte de la question",
            "options": {
                "A": "Option A",
                "B": "Option B",
                "C": "Option C",
                "D": "Option D",
                "E": "Option E"
            },
            "correct_answers": ["A", "C"],
            "explanation": "Explication détaillée de la réponse."
        }
    ]
}

Ne retourne **que du JSON valide**, sans texte supplémentaire avant ou après.
"""

response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "system", "content": "Tu es un assistant pédagogique qui génère des QCM médicaux en JSON strict."},
              {"role": "user", "content": prompt}],
    max_tokens=800,
    temperature=0.3,
)

print("🔎 Réponse brute OpenAI :")
print(response.choices[0].message.content.strip())
