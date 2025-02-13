import openai

# ✅ Utilisation correcte du client OpenAI
client = openai.OpenAI(api_key="sk-proj-YxQAVMW44xcXQ4VrTylfT3BlbkFJZVgFdpjsDcW8JjRjoPDj")

response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Quels sont les muscles du bras ?"}],
    max_tokens=100
)

print(response.choices[0].message.content)
