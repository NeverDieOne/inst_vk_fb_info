from dotenv import load_dotenv
import requests
import os
from utils import check_comment_date
import datetime
from pprint import pprint

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
        comments = get_post_comments(post_id)
        for comment in comments:
            commenters.add(comment['from']['id'])
    return commenters


def get_post_reaction(post_id):
    params = {
        'access_token': os.getenv('FB_ACCESS_TOKEN')
    }
    response = requests.get(f"{BASE_URL}/{post_id}/reactions", params=params)
    response.raise_for_status()

    return response.json()['data']


def get_reactions_list(posts_ids):
    reactions = dict()
    for post_id in posts_ids:
        post_reactions = get_post_reaction(post_id)
        print(post_reactions)
        # for reaction in post_reactions:
        #     print(reaction)

    return reactions


def get_facebook_statistic(group_id):
    posts_ids = get_group_posts(group_id)

    # commenters_list = get_commenters_list(posts_ids)
    reactions_list = get_reactions_list(posts_ids)

    return reactions_list


if __name__ == '__main__':
    load_dotenv()

    group_id = get_group_id()
    print(get_facebook_statistic(group_id))










