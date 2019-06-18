from instabot import Bot
import os
from dotenv import load_dotenv
import datetime

if __name__ == '__main__':
    load_dotenv()

    bot = Bot()
    bot.login(username=os.getenv('INST_LOGIN'), password=os.getenv('INST_PASSWORD'))

    user_id = bot.get_user_id_from_username('cocacolarus')
    user_medias = bot.get_total_user_medias(user_id)

    for media_id in user_medias:
        comments = bot.get_media_comments_all(media_id)
        for comment in comments:
            print(comment['text'])
            comment_date = datetime.datetime.fromtimestamp(comment['created_at'])
            print(comment_date)
            print()
