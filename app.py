import nltk
import os
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import string
import streamlit as st




# Téléchargement des ressources NLTK si elles ne sont pas déjà là
nltk_data_dir = os.path.join(os.path.expanduser("~"), "nltk_data")
nltk.download('punkt', download_dir=nltk_data_dir)
nltk.download('stopwords', download_dir=nltk_data_dir)
nltk.download('wordnet', download_dir=nltk_data_dir)
nltk.download('punkt_tab')

# Dire à nltk où chercher les données
nltk.data.path.append(nltk_data_dir)

# Charger le fichier texte et séparer les questions et réponses
with open("chatbot.txt", 'r', encoding='utf-8') as f:
    data = f.read().splitlines()

# Créer un dictionnaire pour stocker les questions et réponses
qa_pairs = {}
for line in data:
    if ',' in line:
        question, answer = line.split(',', 1)  # Séparer en question et réponse
        qa_pairs[question.strip()] = answer.strip()

# Définir une fonction pour prétraiter le texte
def preprocess(text):
    # Tokeniser le texte en mots
    words = word_tokenize(text)
    # Supprimer les stopwords et la ponctuation
    words = [word.lower() for word in words if word.lower() not in stopwords.words('french') and word not in string.punctuation]
    # Lemmatiser les mots
    lemmatizer = WordNetLemmatizer()
    words = [lemmatizer.lemmatize(word) for word in words]
    return words

# Définir une fonction pour trouver la réponse la plus pertinente
def get_most_relevant_answer(query):
    # Prétraiter la requête
    query = preprocess(query)
    max_similarity = 0
    most_relevant_question = ""
    most_relevant_answer = "Je ne trouve pas de réponse à votre question. Pour plus d'informations, contactez-nous au 77 400 10 10."

    # Comparer la requête avec chaque question dans le dictionnaire
    for question in qa_pairs:
        processed_question = preprocess(question)
        similarity = len(set(query).intersection(processed_question)) / float(len(set(query).union(processed_question)))
        if similarity > max_similarity:
            max_similarity = similarity
            most_relevant_question = question
            most_relevant_answer = qa_pairs[question]
    if max_similarity == 0:
         most_relevant_answer = "Désolé, je ne comprends pas bien votre question."
    return most_relevant_answer

# Définir la fonction du chatbot
def chatbot(question):
    # Trouver la réponse la plus pertinente
    answer = get_most_relevant_answer(question)
    # Retourner la réponse
    return answer

# Créer une application Streamlit
def main():
    st.title("Renta Car")
    st.write("Bonjour et bienvenue ! Je suis Rentabot, votre assistant virtuel. Je suis là pour répondre à toutes vos questions concernant l'entreprise Rentabot. Comment puis-je vous aider aujourd'hui ?")

    # Initialiser la variable de boucle
    continue_chatting = True
    iteration = 0

    while continue_chatting:
        # Obtenir la question de l'utilisateur
        question = st.text_input("Vous:", key=f"question_{iteration}")

        # Afficher la question de l'utilisateur
        if question:
            st.write(f"Vous: {question}")

            # Appeler la fonction du chatbot avec la question et afficher la réponse
            response = chatbot(question)
            st.write(f"Rentabot: {response}")

        # Demander à l'utilisateur s'il souhaite continuer
        continue_chatting = st.checkbox("Continuer à discuter?", key=f"checkbox_{iteration}")

        # Incrémenter le compteur d'itération
        iteration += 1

if __name__ == "__main__":
    main()
