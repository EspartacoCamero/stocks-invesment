import requests

class Tabot:
    BOT_URL = 'https://api.telegram.org/bot'

    def __init__(self, chat_token, chat_id):
        self.chat_token = chat_token
        self.chat_id = chat_id

    def __str__(self):
        return "Tabot with chat token: {token} and chat_id {chat_id}".format(token=self.chat_token, chat_id=self.chat_id)

    def get_chat_id(self):
        url = Tabot.BOT_URL + str(self.chat_token) + '/getUpdates'
        #response = requests.get('https://api.telegram.org/bot5675115970:AAFxftIMTUwBrJtOMRfPZjI3e3_3kFy0YKU/getUpdates')
        response = requests.get(url)
        print(url)

        return response.json()['result'][0]['message']['chat']['id']