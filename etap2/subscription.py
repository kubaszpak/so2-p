import threading
from newsapi import NewsApiClient
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv('API_KEY')

newsapi = NewsApiClient(api_key=API_KEY)

THREAD_INTERVAL_IN_SECONDS = 20


class Subscription(threading.Thread):
    def __init__(self, name, country_choice=None, category_choice=None):
        super().__init__()

        self.name = name
        self.country_choice = country_choice
        self.category_choice = category_choice

        self.__stopped = threading.Event()
        self.__running = threading.Event()
        self.__running.set()

    def run(self):
        self.get_new_headlines()
        while self.__running.isSet():
            while not self.__stopped.wait(THREAD_INTERVAL_IN_SECONDS):
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
        print(f"Request for {self.name}")
