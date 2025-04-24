import random
import json
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import load_model

lemmatizer = WordNetLemmatizer()

intents = json.loads(open('intents.json').read())
words = json.load(open('words.json'))
classes = json.load(open('classes.json'))
model = load_model('chatbot_model.h5')

def clean_up(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

def bag_of_words(sentence, words):
    sentence_words = clean_up(sentence)
    bag = [0] * len(words)
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                bag[i] = 1
    return np.array(bag)

def predict_intent(sentence):
    bow = bag_of_words(sentence, words)
    result = model.predict(np.array([bow]))[0]
    threshold = 0.6
    result_indices = [[i, r] for i, r in enumerate(result) if r > threshold]
    result_indices.sort(key=lambda x: x[1], reverse=True)
    return [{"intent": classes[r[0]], "probability": str(r[1])} for r in result_indices]

def get_response(intents_list):
    if intents_list:
        tag = intents_list[0]['intent']
        for i in intents['intents']:
            if i['tag'] == tag:
                return random.choice(i['responses'])
    return "I'm not sure I understand that."

def chatbot_reply(text):
    intents_list = predict_intent(text)
    return get_response(intents_list)
