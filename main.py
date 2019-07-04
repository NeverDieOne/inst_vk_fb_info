from instabot import Bot
import os
from dotenv import load_dotenv
import datetime
import collections
import requests
from pprint import pprint


def get_post_statistic(bot, post_id, days=90) -> collections.Counter:
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


def get_inst_info():
    bot = Bot()
    bot.login(username=os.getenv('INST_LOGIN'), password=os.getenv('INST_PASSWORD'))

    user_id = bot.get_user_id_from_username('cocacolarus')
    user_medias = bot.get_total_user_medias(user_id)  # ID всех постов

    # Получаем счетчик user_id: количество коментариев
    comments_top = collections.Counter()
    comments_statistic = [get_post_statistic(bot, post_id) for post_id in user_medias]
    for comment in comments_statistic:
        comments_top += comment

    # Получаем счетчик user_id: количество откоментированных постов
    posts_top = collections.Counter()
    for post_id in user_medias:
        commenters = set(bot.get_media_commenters(post_id))
        for commenter in commenters:
            if int(commenter) in comments_top:
                posts_top[commenter] += 1


def get_vk_info():
    page = 0
    pages_number = 1

    result = []

    # while page < pages_number:
    base_url = 'https://api.vk.com/method/wall.get'
    base_params = {
        'access_token': os.getenv('SERVICE_VK_TOKEN'),
        'v': '5.95',
        'domain': 'cocacola',
        'count': 100,
    }

    response = requests.get(base_url, params=base_params)
    result += response.json()['response']['items']

    pprint(response.json())


if __name__ == '__main__':
    load_dotenv()

    get_vk_info()
