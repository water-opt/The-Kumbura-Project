import os
from django.conf import settings
import random
import string
import numpy as np
import warnings
import nltk
from rest_framework.decorators import api_view
from rest_framework.response import Response
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.stem import WordNetLemmatizer

nltk.download('punkt', quiet=True)
nltk.download('wordnet', quiet=True)

warnings.filterwarnings('ignore')

lemmatizer = WordNetLemmatizer()

greeting_user = ['hi', 'hello', 'hey', 'greetings']
greeting_response = ['hi there', 'hello there', 'hey', 'hello user!']

punct = str.maketrans('', '', string.punctuation)

def _tokenize():
    path_corpus = os.path.join(settings.BASE_DIR, 'chatbot', 'corpus.txt')
    with open(path_corpus, 'r', errors='ignore') as file:
        corpus_data = file.read()
    sent_tokens = nltk.sent_tokenize(corpus_data)
    return sent_tokens

def _lemmatize(tokens):
    return [lemmatizer.lemmatize(i) for i in tokens]

def _lemmatize_text_without_punct(text):
    without_punc_word_tokens = nltk.word_tokenize(text.lower().translate(punct))
    return _lemmatize(without_punc_word_tokens)

def _greeting_response(user_input):
    for token in user_input.split():
        if token.lower() in greeting_user:
            return random.choice(greeting_response)
    return None

def _generate_response(user_query, sent_tokens):
    sent_tokens.append(user_query)
    
    Tfidf_vectors_object = TfidfVectorizer(tokenizer=_lemmatize_text_without_punct, stop_words='english')
    Tfidf_vectors = Tfidf_vectors_object.fit_transform(sent_tokens)

    cosine_similarity_values = cosine_similarity(Tfidf_vectors[-1], Tfidf_vectors) # type: ignore

    index_response = cosine_similarity_values.argsort()[0][-2]
    required_tfidf = cosine_similarity_values.flatten()[index_response]

    if required_tfidf < 0.1: 
        return "I'm sorry, I don't have enough information on that."
    else:
        return sent_tokens[index_response]

# print('Bot -> Greetings!')

conversation_history = []

@api_view(['POST'])
def _user_query(request):
    data = request.data
    query = str(data.get('query')).strip()
    response = _greeting_response(query)

    if response is None:
        sent_tokens = _tokenize()
        response = _generate_response(query, sent_tokens)
    
    conversation_history.append({"user": query, "bot": response})

    return Response({'reply': response})

