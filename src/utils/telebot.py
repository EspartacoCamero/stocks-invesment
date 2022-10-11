import requests

class Tabot:
    def __init__(self, chat_token, chat_id):
        BOT_URL = 'https://api.telegram.org/bot'

        self.chat_token = chat_token
        self.chat_id = chat_id

    def __str__(self):
        return "Tabot with chat token: {token} and chat_id {chat_id}".format(token=self.chat_token, chat_id=self.chat_id)