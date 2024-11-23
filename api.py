from fastapi import FastAPI
from pydantic import BaseModel
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage


os.environ["GOOGLE_API_KEY"] = "AIzaSyDi0e42aTdXnhvHEzdQYh-zvfGnk_jcmQw"


app = FastAPI()

# Modèle de la requête avec Pydantic
class Message(BaseModel):
    subject: str  # Champ pour le sujet de la blague

# Modèle pour la réponse avec Pydantic
class JokeResponse(BaseModel):
    joke: str  # Le texte de la blague

def send_message(subject : str):

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "Give me a joke in this subject: {subject} ",
            ),
            MessagesPlaceholder(variable_name="subject"),
        ]
    )
    
    model = ChatGoogleGenerativeAI(
        model="gemini-1.5-pro",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
    )

    chain = prompt | model

    return chain.invoke({"subject": [HumanMessage(content = subject)]})

@app.post("/joke/")
async def stream_chat(message: Message):
    joke = send_message(message.subject)

    return JokeResponse(joke=joke.content) #Quand une route dans FastAPI retourne une instance de modèle Pydantic comme réponse, FastAPI utilise automatiquement Pydantic pour convertir cet objet en JSON