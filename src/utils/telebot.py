import requests

class Tabot:
    BOT_URL = 'https://api.telegram.org/bot'

    def __init__(self, chat_token, chat_id = None):
        self.chat_token = chat_token
        self.chat_id = chat_id

    def __str__(self):
        return "Tabot with chat token: {token} and chat_id {chat_id}".format(token=self.chat_token, chat_id=self.chat_id)

    def get_chat_id(self):
        try:
            url = Tabot.BOT_URL + str(self.chat_token) + '/getUpdates'
            response = requests.get(url)
            self.chat_id = response.json()['result'][0]['message']['chat']['id']
        except IndexError as ex1:
            print("Error " + str(ex1))
            print("Check if chat group at Telegram was created with Tabot in it. Also make sure to send a message to activate the chat")


    def check_bot(self):
        url = Tabot.BOT_URL + str(self.chat_token) + '/getUpdates'
        print(requests.get(url))

    def send_message(self, text):
        if self.chat_id is None:
            raise Exception("Chat id is missing. Run 'get_chat_id' method or provide the chat id when creating the object")
        
        if not isinstance(text, str):
            raise Exception('Message needs to be a string')

        url = Tabot.BOT_URL + str(self.chat_token) + '/sendMessage?chat_id=' + str(self.chat_id) +'&text=' + text 
        requests.get(url)