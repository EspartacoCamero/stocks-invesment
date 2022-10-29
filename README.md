stocks-invesment
==============================

This ETL project will tell you where to invest your money according to your prefered stocks right away in your Telegram APP.
The process is divided in three simple steps:

![ETL](https://github.com/EspartacoCamero/stocks-invesment/blob/master/etl-stocks.jpg?)

We get the data from yahoo, transformed with Pandas and delivered to Telegram. Everything was built using Python.


Regarding the strategy about what stocks are sent, recommendations is based on the following indicators:
- **Trend:** MA or EMA
- **Momemtun:** RSI
- **Volatility:** Bollinger Bands
- **Strength:** ADX (Not implemented yet)


####  Flow:
- Load which ticks you want to analyze.
- Create your strategy, for example, having a RSI <= 30, and/or a EMA12 < EMA26, etc.
- Recieve which stocks satisfied tose condition in a daily (weekly?, monthly?) based Telegram message.



#### Steps:
1. A CSV file  your own tick selections and you strategy.
2. You need a Telegram account where the alerts will be send. Check details bellow
3. Create a cron process in you computer. Check details bellow.





**Step 1: Ticks and strategy**


**Step 2: Telegram setup:**

Within your Telegram account, look for *BotFather* contact and open a chat with him.
Now, write him the following messages:
```
/start
/newbot
```

And then asigne a name and a nickname for you bot. Check and save the token generated for your bot. You will use it later.
Now, create a Telegram group and add your new bot to the chat by the name you gave him. 
To make sure the bot is active and to create a chat_id for this Telegram group, write the following message.

```
/my_id @<bot name>
```

Done! You already have a group where you will receive your notifications. You can invite anyone to this group


**Step 3: Cron setup:**
