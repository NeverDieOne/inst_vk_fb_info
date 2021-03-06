import requests
import os
from dotenv import load_dotenv
from contextlib import suppress
from utils import check_comment_date, get_objects_from_vk_request


BASE_URL = 'https://api.vk.com/method/'


def get_group_id_by_name(access_token, group_name):
    """
    Возвращает ID группы по её имени
    """
    params = {
        'access_token': access_token,
        'v': 5.103,
        'group_id': group_name
    }

    response = requests.get(f"{BASE_URL}/groups.getById", params=params).json()['response']
    return response[0]['id']


def get_user_posts(access_token, owner_id, post_per_page=100, max_count=None):
    """
    Возвращает список постов owner_id. Есть возможность вернуть ограниченное число постов с помощью max_count
    """
    params = {
        'access_token': access_token,
        'v': 5.103,
        'owner_id': -owner_id,
    }

    posts = get_objects_from_vk_request(BASE_URL, 'wall.get', params, post_per_page, max_count)
    return posts


def get_post_comments(access_token, owner_id, post_id, comments_per_page=100, max_count=None):
    """
    Возвращает список комментов post_id. Есть возможость вернуть ограниченное число комметов с помощью max_count.
    """
    params = {
        'access_token': access_token,
        'v': 5.103,
        'owner_id': -owner_id,
        'post_id': post_id
    }

    comments = get_objects_from_vk_request(BASE_URL, 'wall.getComments', params, comments_per_page, max_count)
    return comments


def get_post_likers(access_token ,owner_id, post_id, likers_per_page=100, max_count=None):
    """
    Возвращает список людей, которые лайкнули пост post_id. Есть возможность вернуть ограниченное число лайкнувших
    с помощью max_count.
    """
    params = {
        'access_token': access_token,
        'v': 5.103,
        'type': 'post',
        'owner_id': -owner_id,
        'post_id': post_id
    }

    likers = get_objects_from_vk_request(BASE_URL, 'likes.getList', params, likers_per_page, max_count)
    return likers


def get_commenters(access_token, group_id, posts) -> set:
    """
    Возвращает множество комментаторов из списка постов posts.
    """
    users = set()
    for post in posts:
        comments = get_post_comments(access_token, group_id, post['id'])

        for comment in comments:
            with suppress(KeyError):  # Может не быть from_id, т.к. будет deleted: True
                if check_comment_date(comment['date'], period_days=14) and comment['from_id'] != -16297716:
                    users.add(comment['from_id'])

    return users


def get_likers(access_token, group_id, posts):
    """
    Возвращает множество лайкнувших из списка постов posts.
    """
    return (set(get_post_likers(access_token, group_id, post['id'])) for post in posts)


def get_vk_statistic(access_token, group_name):
    group_id = get_group_id_by_name(access_token, group_name)

    posts = get_user_posts(access_token, group_id)

    commenters = get_commenters(access_token, group_id, posts)
    likers = get_likers(access_token, group_id, posts)

    return commenters.intersection(likers)


if __name__ == '__main__':
    load_dotenv()

    access_token = os.getenv('SERVICE_VK_TOKEN')

    group_name = 'cocacola'
    print(get_vk_statistic(access_token, group_name))
