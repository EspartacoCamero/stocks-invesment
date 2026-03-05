stocks-invesment
==============================

This ETL project will tell you where to invest your money according to your preferred stocks right away in your Telegram app.
The process is divided in three simple steps:

![ETL](https://github.com/EspartacoCamero/stocks-invesment/blob/master/etl-stocks.jpg?)

We get the data from yahoo, transformed with Pandas and delivered to Telegram. Everything was built using Python.


Regarding the strategy about what stocks are sent, recommendations are based on the following indicators:
- **Trend:** MA or EMA
- **Momentum:** RSI
- **Volatility:** Bollinger Bands
- **Strength:** ADX (Not implemented yet)


####  Flow:
- Load which ticks you want to analyze.
- Create your strategy, for example, having a RSI <= 30, and/or a EMA12 < EMA26, etc.
- Receive which stocks satisfy those conditions in a daily (weekly?, monthly?) Telegram message.



#### Steps:
1. A CSV file with your own tick selections and your strategy.
2. You need a Telegram account where the alerts will be sent. Check details below.
3. Create a cron process in your computer. Check details below.





**Step 1: Ticks and strategy**


**Step 2: Telegram setup:**

Within your Telegram account, look for *BotFather* contact and open a chat with him.
Now, write him the following messages:
```
/start
/newbot
```

And then assign a name and a nickname for your bot. Check and save the token generated for your bot. You will use it later.
Now, create a Telegram group and add your new bot to the chat by the name you gave him. 
To make sure the bot is active and to create a chat_id for this Telegram group, follow the next steps:
1. Copy the token you received when creating the bot.
2. Open this link in your browser with your token on it https://api.telegram.org/bot/<your_bot_token>/getupdates
3. Go back to Telegram and chat with your bot.
4. Refresh the page from point 2 and look for your chat id



Done! You already have a group where you will receive your notifications. You can invite anyone to this group


**Step 3: Cron setup:**
