from threading import Thread
from newsapi import NewsApiClient
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv('API_KEY')

newsapi = NewsApiClient(api_key=API_KEY)


class Subscription(Thread):
    def __init__(self, name, country_choice, category_choice):
        super().__init__()

        self.name = name
        self.country_choice = country_choice
        self.category_choice = category_choice

    def get_new_headlines(self):
        # new_headlines = newsapi.get_top_headlines(q='bitcoin',
        #                                           sources='bbc-news,the-verge',
        #                                           category='business',
        #                                           language='en',
        #                                           country='us')
        print("Pobieranie nowych headline'ów!")
