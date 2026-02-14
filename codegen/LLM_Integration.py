import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def call_llm(prompt):
    completion = client.chat.completions.create(
        model="openai/gpt-oss-120b",  # fast + strong
        messages=[
            {"role": "system", "content": "You are a senior backend architect. Follow clean layered architecture."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    return completion.choices[0].message.content

