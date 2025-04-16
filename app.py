import nltk
import os
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import string
import streamlit as st




nltk_data_dir = os.path.join(os.path.expanduser("~"), "nltk_data")
nltk.download('punkt', download_dir=nltk_data_dir)
nltk.download('stopwords', download_dir=nltk_data_dir)
nltk.download('wordnet', download_dir=nltk_data_dir)
nltk.download('punkt_tab')

nltk.data.path.append(nltk_data_dir)

with open("chatbot.txt", 'r', encoding='utf-8') as f:
    data = f.read().splitlines()

qa_pairs = {}
for line in data:
    if ',' in line:
        question, answer = line.split(',', 1)  
        qa_pairs[question.strip()] = answer.strip()

def preprocess(text):
   
    words = word_tokenize(text)
    
    words = [word.lower() for word in words if word.lower() not in stopwords.words('french') and word not in string.punctuation]
    
    lemmatizer = WordNetLemmatizer()
    words = [lemmatizer.lemmatize(word) for word in words]
    return words

# Définir une fonction pour trouver la réponse la plus pertinente
def get_most_relevant_answer(query):
    
    query = preprocess(query)
    max_similarity = 0
    most_relevant_question = ""
    most_relevant_answer = "Je ne trouve pas de réponse à votre question. Pour plus d'informations, contactez-nous au 77 400 10 10."

   
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
   
    answer = get_most_relevant_answer(question)
   
    return answer

def main():
    st.title("RentaCar")
    st.write("Bonjour! Je suis Rentabot, votre assistant virtuel. Je suis là pour répondre à toutes vos questions concernant l'entreprise de location/vente de voiture RentaCar. Comment puis-je vous aider aujourd'hui ?")

    continue_chatting = True
    iteration = 0

    while continue_chatting:
        # Obtenir la question de l'utilisateur
        question = st.text_input("Vous:", key=f"question_{iteration}")

        if question:
            st.write(f"Vous: {question}")

            response = chatbot(question)
            st.write(f"Rentabot: {response}")

        continue_chatting = st.checkbox("Continuer à discuter?", key=f"checkbox_{iteration}")

        iteration += 1

if __name__ == "__main__":
    main()
