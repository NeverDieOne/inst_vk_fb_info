from dotenv import load_dotenv
import requests
import os
from utils import check_comment_date
import datetime

BASE_URL = 'https://graph.facebook.com'


def get_group_id():
    params = {
        'access_token': os.getenv('FB_ACCESS_TOKEN')
    }

    response = requests.get(f"{BASE_URL}/me/groups", params=params)
    response.raise_for_status()

    return response.json()['data'][0]['id']


def get_group_posts(group_id):
    params = {
        'access_token': os.getenv('FB_ACCESS_TOKEN')
    }
    response = requests.get(f"{BASE_URL}/{group_id}/feed", params=params)
    response.raise_for_status()

    return [post['id'] for post in response.json()['data']]


def get_post_comments(post_id):
    params = {
        'access_token': os.getenv('FB_ACCESS_TOKEN')
    }
    response = requests.get(f"{BASE_URL}/{post_id}/comments", params=params)
    response.raise_for_status()

    return response.json()['data']


def get_commenters_list(posts_ids):
    commenters = set()
    for post_id in posts_ids:
        print(post_id)
        # comments = get_post_comments(post_id)
        # print(comments)
        # for comment in comments:
        #     commenters.add(comment['data']['from']['id'])
        #     print(comment)

    return commenters


def get_comment_reaction(comment_id):
    params = {
        'access_token': os.getenv('FB_ACCESS_TOKEN')
    }
    response = requests.get(f"{BASE_URL}/{comment_id}/reactions", params=params)
    response.raise_for_status()

    return response.json()


def get_facebook_statistic(group_id):
    posts_ids = get_group_posts(group_id)

    commenters_list = get_commenters_list(posts_ids)

    return commenters_list


if __name__ == '__main__':
    load_dotenv()

    group_id = get_group_id()
    print(get_facebook_statistic(group_id))










