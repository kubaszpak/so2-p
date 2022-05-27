import threading
from dotenv import load_dotenv
import os
from tkinter import ttk
import requests
import webbrowser

from news_api_exception import NewsAPIException

load_dotenv()

API_KEY = os.getenv('API_KEY')

TOP_HEADLINES_ENDPOINT = "https://newsapi.org/v2/top-headlines"


class Subscription(threading.Thread):
    def __init__(self, name, frame, interval, country_choice=None, category_choice=None):
        super().__init__()
        self.headlines = {}
        self.name = name
        self.interval = interval
        self.country_choice = country_choice
        self.category_choice = category_choice
        self.frame = frame

        self.__stopped = threading.Event()
        self.__running = threading.Event()
        self.__running.set()

    def run(self):
        self.get_new_headlines()
        while self.__running.isSet():
            while not self.__stopped.wait(self.interval):
                self.get_new_headlines()

    def pause(self):
        self.__stopped.set()

    def resume(self):
        self.__stopped.clear()

    def stop(self):
        self.__stopped.set()
        self.__running.clear()
        self.join()

    def get_new_headlines(self):
        payload = {}
        payload['apiKey'] = API_KEY
        if self.category_choice:
            payload['category'] = self.category_choice
        if self.country_choice:
            payload['country'] = self.country_choice

        print(f"Checking for new headlines on subscription: {self.name}!")
        res = requests.get(
            TOP_HEADLINES_ENDPOINT, timeout=10, params=payload)

        if res.status_code != requests.codes.ok:
            raise NewsAPIException(res.json())

        newHeadlineFound = False
        new_headlines = res.json()
        for headline in new_headlines["articles"]:
            if headline["title"] not in self.headlines:
                newHeadlineFound = True
                self.add_new_headline(headline)

        if not newHeadlineFound:
            print("No new headlines found!")

    def add_new_headline(self, headline):
        self.headlines[headline["title"]] = headline
        print(f"New headline: {headline['title']}")
        label_title = ttk.Label(
            self.frame, text=f'{self.name}\t{headline["publishedAt"]}\t{headline["source"]["name"]}\n{headline["title"]}\t', anchor="w")
        label_title.pack(fill="x")
        button_open_url = ttk.Button(self.frame,
                                     text="More...", command=lambda: webbrowser.open_new(headline["url"]))
        button_open_url.pack()
        sep = ttk.Separator(self.frame, orient="horizontal")
        sep.pack(fill='x')

    def is_thread_running(self):
        return not self.__stopped.isSet()
