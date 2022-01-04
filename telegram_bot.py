from telethon import TelegramClient, sync
import time
import config as config

client = TelegramClient('session_name', config.API_ID, config.API_HASH).start()

from pancake_bot import buy_token


def get_message():
    last_message = ""
    message =client.get_messages(config.GROUP_NAME, 1)
    token = ""

    for chat in message:
        if last_message == "":
            last_message = chat.message

        expected_message = "Insider info received for possible CMC listing. Coin not listed anywhere yet (listing in 15 minutes aprox.) Buy now to be the first (first pump)."
        if(expected_message in chat.message):
            message = chat.message
            
            token_start_position = message.find("Address:")
            token_finish_position = message.find("Liquidity:")
            token = message[token_start_position:token_finish_position]
            token = token.replace(" ", "").replace("Address:", "").replace("\n", "")
            
            return(token)

def main():
    last_message = ""
    new_last_message = ""
    while(True):
        new_last_message = get_message()        

        if not last_message:
            last_message = new_last_message
        elif last_message != new_last_message:
            start = time.time()
            last_message = new_last_message
            print('buying token: ', last_message)
            buy_token(last_message)
            end = time.time()
            print('Tempo demorado para comprar -> ', end - start)
            break


main()
