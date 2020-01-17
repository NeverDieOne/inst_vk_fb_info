from dotenv import load_dotenv
import requests
import os
from utils import check_comment_date_fb
import collections

BASE_URL = 'https://graph.facebook.com'


def get_group_id(access_token):
    """
    Возвращает group_id, где пользователь является создателем.
    """
    params = {
        'access_token': access_token
    }

    response = requests.get(f"{BASE_URL}/me/groups", params=params)
    response.raise_for_status()

    return response.json()['data'][0]['id']


def get_group_posts(access_token, group_id):
    """
    Возвращает список постов в группе group_id.
    """
    params = {
        'access_token': access_token
    }
    response = requests.get(f"{BASE_URL}/{group_id}/feed", params=params)
    response.raise_for_status()

    return [post['id'] for post in response.json()['data']]


def get_post_comments(access_token, post_id):
    """
    Возвращает список комментариев под постом post_id.
    """
    params = {
        'access_token': access_token
    }
    response = requests.get(f"{BASE_URL}/{post_id}/comments", params=params)
    response.raise_for_status()

    return response.json()['data']


def get_commenters_list(access_token, posts_ids):
    """
    Возвращает список комментаторов под списком постов posts_ids.
    """
    commenters = set()
    for post_id in posts_ids:
        comments = get_post_comments(access_token, post_id)
        commenters += (comment['from']['id'] for comment in comments if check_comment_date_fb(comment['created_time']))

    return commenters


def get_post_reaction(access_token, post_id):
    """
    Возвращает список реакций на пост post_id.
    """
    params = {
        'access_token': access_token
    }
    response = requests.get(f"{BASE_URL}/{post_id}/reactions", params=params)
    response.raise_for_status()

    return response.json()['data']


def get_reactions_list(access_token, posts_ids):
    """
    Возвращает словарь в котором ключами являются user_id, а значения - словари с подсчетом реакций пользователя.
    """
    reactions = collections.defaultdict(collections.Counter)
    for post_id in posts_ids:

        post_reactions = get_post_reaction(access_token, post_id)

        for reaction in post_reactions:
            reaction_type = reaction['type']
            user_id = reaction['id']

            reactions[user_id] += collections.Counter([reaction_type])

    return reactions


def get_facebook_statistic(access_token):
    group_id = get_group_id(access_token)

    posts_ids = get_group_posts(access_token, group_id)

    return get_reactions_list(access_token, posts_ids)

    # commenters_list = get_commenters_list(access_token, posts_ids)
    # reactions_list = get_reactions_list(access_token, posts_ids)
    #
    # return commenters_list, reactions_list


if __name__ == '__main__':
    load_dotenv()

    access_token = os.getenv('FB_ACCESS_TOKEN')

    print(get_facebook_statistic(access_token))
