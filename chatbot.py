import numpy as np
import nltk
from tensorflow.keras.models import load_model
import json
import os

# Download NLTK data if not already present
nltk.download('punkt')

# Load the trained model and other necessary data
model = load_model("model.h5")

# Load the JSON file containing the intents
intents_file_path = "intents.json"
with open(intents_file_path, 'r') as f:
    intents = json.load(f)

# Initialize the stemmer
stemmer = nltk.stem.LancasterStemmer()

# Extract words and labels from the training data
words = sorted(set(stemmer.stem(w.lower()) for w in nltk.word_tokenize(" ".join([pattern for intent in intents["intents"] for pattern in intent["patterns"]])) if w not in "?"))
labels = sorted(set(intent["tag"] for intent in intents["intents"]))

# Function to convert user input into a bag of words
def bag_of_words(s, words):
    bag = [0] * len(words)
    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1

    return np.array(bag)

# Function to handle user input and return chatbot response
def chat_with_bot(user_input):
    results = model.predict(np.array([bag_of_words(user_input, words)]))
    results_index = np.argmax(results)
    tag = labels[results_index]

    response = "Sorry, I don't understand that."
    for intent in intents["intents"]:
        if intent['tag'] == tag:
            responses = intent['responses']
            response = responses[0]
            break
    
    return response
