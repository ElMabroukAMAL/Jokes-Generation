import streamlit as st
import requests

# Titre de l'application
st.title("Joke Generator")

# Zone de texte pour entrer le sujet de la blague
subject = st.text_input("Enter a subject of the joke ")

# Si un sujet est fourni, faites la requête POST à l'API FastAPI
if subject:
    # Requête POST pour envoyer le sujet et récupérer la blague
    response = requests.post("http://127.0.0.1:8000/joke/", json={"subject": subject})
    
    # Vérifiez si la réponse est OK
    if response.status_code == 200:
        joke = response.json()
        st.subheader("The joke :")
        st.write(joke["joke"])  
    else:
        st.error("Error.")
