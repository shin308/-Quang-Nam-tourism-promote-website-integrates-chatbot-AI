# -*- coding: utf-8 -*-
"""
Created on Sat May  9 22:59:57 2020

@author: Madhan Kumar Selvaraj
"""
import nltk
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import pickle
import numpy as np
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()
import keras
from tensorflow.keras.models import load_model
import sys

session = tf.Session()
graph = tf.get_default_graph()

tf.keras.backend.set_session(session)

model = load_model(r'chatbot_model_v2.h5')
model._make_predict_function()
import json
import random
intents = json.loads(open(r'intents2.json', encoding="utf-8").read())
words = pickle.load(open(r'words.pkl','rb'))
classes = pickle.load(open(r'classes.pkl','rb'))


def clean_up_sentence(sentence):
    # tokenize the pattern - split words into array
    sentence_words = nltk.word_tokenize(sentence)
    # stem each word - create short form for word
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words
# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence
def bow(sentence, words, show_details=True):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words - matrix of N words, vocabulary matrix
    bag = [0]*len(words) 
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s: 
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)
    return(np.array(bag))

def predict_class(sentence, model):
    # filter out predictions below a threshold
    global graph
    global session

    p = bow(sentence, words,show_details=False)
    with graph.as_default():
        tf.keras.backend.set_session(session)
        res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

def getResponse(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    results = []
    for i in list_of_intents:
        if(i['tag'] == tag):
            results = i['responses'] 
            #results.append(i['responses'])
            break
    return results
def chatbot_response(text):
    ints = predict_class(text, model)
    res = getResponse(ints, intents)
    return res

# def destination_details(request, tour_id):
#     # dest = Detailed_desc.objects.get(dest_name=city_name)
#     dest = get_object_or_404(Detailed_desc, dest_id=tour_id)

#     price = dest.price
#     city_name = dest.dest_name

#     request.session['price'] = price
#     request.session['city'] = city_name

#     tour = Detailed_desc.objects.get(dest_id=tour_id)
#     #tours = get_object_or_404(Detailed_desc, dest_id=tour_id)

#     if request.method == "POST":
#         # For rating
#         if not request.user.is_authenticated:
#             return redirect('login')
#         else:
#             rate = request.POST['rating']
#             if Myrating.objects.all().values().filter(tour_id=tour_id,user=request.user.get_user):
#                 Myrating.objects.all().values().filter(tour_id=tour_id,user=request.user).update(rating=rate)
#             else:
#                 q=Myrating(user=request.user,tour_id=tour,rating=rate)
#                 q.save()

#             messages.success(request, "Rating has been submitted!")

#         return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
#     out = list(Myrating.objects.filter(user_id=request.user.id).values())

#     # To display ratings in the movie detail page
#     tour_rating = 0
#     rate_flag = False
#     for each in out:
#         if each['tour_id'] == tour_id:
#             tour_rating = each['rating']
#             rate_flag = True
#             break

#     context = {'dest':dest,'tour_rating':tour_rating,'rate_flag':rate_flag}

#     return render(request,'destination_details.html', context)