# discord-blackjack
 A rusty and unorganized discord bot you can play blackjack with
 
## Usage
#### To enable the bot on your server: 
Invite the bot using the [invitation link](https://discord.com/oauth2/authorize?client_id=676422935933878282&scope=bot), which also can be found by sending a message containing word 'invite' on a server that this bot is a part of.

#### To use your own Discord bot application
Set up the environment:
```
python -m venv venv
.\venv\Scripts\activate
python -m pip install -r requirements.txt
```
> This creates a virtual environment, activates it and downloads the requirements to it.

Save your discord application token in the "token.tkn" file. This should work.
> This can be found at [https://discord.com/developers/applications/{YOUR-BOT-CLIENT-ID}/bot]()
