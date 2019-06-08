import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "client-secret.json"

#Establishing mongo db connection
from pymongo import MongoClient

client1=MongoClient("mongodb+srv://mybot:mybot@cluster0-8cpfq.mongodb.net/test?retryWrites=true&w=majority")


#My Movie Api
from tmdbv3api import TMDb
tmdb = TMDb()
tmdb.api_key = '2fca495abe778601602ef9aea59dc10e'
from tmdbv3api import Movie

import dialogflow_v2 as dialogflow
dialogflow_session_client = dialogflow.SessionsClient()
PROJECT_ID = "newsbot-cnthyu"

from gnewsclient import gnewsclient

client = gnewsclient.NewsClient(max_results=3)
def get_news(parameters):
    client.topic = parameters.get('news_type')
    client.language = parameters.get('language')
    client.location = parameters.get('geo-country')
    return client.get_news()


def detect_intent_from_text(text, session_id, language_code='en'):
    session = dialogflow_session_client.session_path(PROJECT_ID, session_id)
    text_input = dialogflow.types.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.types.QueryInput(text=text_input)
    response = dialogflow_session_client.detect_intent(session=session, query_input=query_input)
    return response.query_result

def fetch_reply(msg,session_id):
    response = detect_intent_from_text(msg,session_id)
    #storing user news searching details in th database
    db=client1.get_database('news_db')
    record_news=db.news_search
    
    #Getting news details
    img=' '
    if response.intent.display_name =='get_news':
        news =  get_news(dict(response.parameters))
        news_str = 'Here is your news'

        for row in news:
            news_str += '\n\n{}\n\n{}\n\n'.format(row['title'],row['link'])
        
        #sending news search preferences to database
        record_news.insert_one(dict(response.parameters))
               
        return news_str,img
    
    elif response.intent.display_name == 'movie':
        
        #inserting user searching details 
        db=client1.get_database('movies_db')
        records=db.movies

        #retrieving movies details
        movie = Movie()
        movie_name=response.parameters['movie']
        search =movie.search(movie_name)
        result = '\n\nId: {}\n\nTitle: {}\n\nOverview: {}\n\nRatings: {}\n\n'.format(search[0].id,search[0].title,search[0].overview,search[0].vote_average)
        img=search[0].poster_path

        #inserting records to database
        records.insert_one(dict(response.parameters))
        
        return result,img

    else:
        return response.fulfillment_text,img