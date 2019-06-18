from instabot import Bot
import os
from dotenv import load_dotenv
from pprint import pprint


if __name__ == '__main__':
    load_dotenv()

    bot = Bot()
    bot.login(username=os.getenv('INST_LOGIN'), password=os.getenv('INST_PASSWORD'))

    user_id = bot.get_user_id_from_username('neverdieone')
    user_info = bot.get_user_info(user_id)

    pprint(user_info)
