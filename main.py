from instabot import Bot
import os
from dotenv import load_dotenv
import datetime
import collections


def get_post_statistic(post_id, days=90) -> collections.Counter:
    counter = collections.Counter()
    comments = bot.get_media_comments_all(post_id)
    today = datetime.datetime.now()
    for comment in comments:
        user_id = comment['user_id']
        comment_text = comment['text']
        comment_date = datetime.datetime.fromtimestamp(comment['created_at'])
        time_delta = today - comment_date
        if time_delta.days <= days:
            counter[user_id] += 1

    return counter


if __name__ == '__main__':
    load_dotenv()

    bot = Bot()
    bot.login(username=os.getenv('INST_LOGIN'), password=os.getenv('INST_PASSWORD'))

    user_id = bot.get_user_id_from_username('cocacolarus')
    user_medias = bot.get_total_user_medias(user_id)  # ID всех постов

    posts_statistic = sum([get_post_statistic(post_id) for post_id in user_medias])
