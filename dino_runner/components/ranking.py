import requests

from dino_runner.utils.constants import API_URL

class Ranking:

    def get(self):
        response = requests.get(API_URL)
        return response

    def save(self,name, score):
        data = {
            "name": name,
            "score":score
        }
        response = requests.post(API_URL, data)
        return response
    