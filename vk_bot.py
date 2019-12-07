import requests
import os
from dotenv import load_dotenv
from contextlib import suppress
from utils import check_comment_date, get_objects


BASE_URL = 'https://api.vk.com/method/'


def get_group_id_by_name(group_name):
    """
    Возвращает ID группы по её имени
    """
    params = {
        'access_token': os.getenv('SERVICE_VK_TOKEN'),
        'v': 5.103,
        'group_id': group_name
    }

    response = requests.get(f"{BASE_URL}/groups.getById", params=params).json()['response']
    return response[0]['id']


def get_user_posts(owner_id, post_per_page=100, max_count=None):
    """
    Возвращает список постов owner_id. Есть возможность вернуть ограниченное число постов с помощью max_count
    """
    params = {
        'access_token': os.getenv('SERVICE_VK_TOKEN'),
        'v': 5.103,
        'owner_id': -owner_id,
    }

    posts = get_objects(BASE_URL, 'wall.get', params, post_per_page, max_count)
    return posts


def get_post_comments(owner_id, post_id, comments_per_page=100, max_count=None):
    """
    Возвращает список комментов post_id. Есть возможость вернуть ограниченное число комметов с помощью max_count.
    """
    params = {
        'access_token': os.getenv('SERVICE_VK_TOKEN'),
        'v': 5.103,
        'owner_id': -owner_id,
        'post_id': post_id
    }

    comments = get_objects(BASE_URL, 'wall.getComments', params, comments_per_page, max_count)
    return comments


def get_post_likers(owner_id, post_id, likers_per_page=100, max_count=None):
    """
    Возвращает список людей, которые лайкнули пост post_id. Есть возможность вернуть ограниченное число лайкнувших
    с помощью max_count.
    """
    params = {
        'access_token': os.getenv('SERVICE_VK_TOKEN'),
        'v': 5.103,
        'type': 'post',
        'owner_id': -owner_id,
        'post_id': post_id
    }

    likers = get_objects(BASE_URL, 'likes.getList', params, likers_per_page, max_count)
    return likers


def get_commenters(group_id, posts) -> set:
    """
    Возвращает множество комментаторов из списка постов posts.
    """
    users = set()
    for post in posts:
        print(post)
        post_id = post['id']
        comments = get_post_comments(group_id, post_id)

        for comment in comments:
            with suppress(KeyError):  # Может не быть from_id, т.к. будет deleted: True
                if check_comment_date(comment['date'], period_days=14) and comment['from_id'] != -16297716:
                    users.add(comment['from_id'])

    return users


def get_likers(group_id, posts) -> set:
    """
    Возвращает множество лайкнувших из списка постов posts.
    """
    users = set()
    for post in posts:
        post_id = post['id']
        likers = set(get_post_likers(group_id, post_id))
        users.union(likers)

    return users


def get_vk_statistic(group_name):
    group_id = get_group_id_by_name(group_name)

    posts = get_user_posts(group_id)

    commenters = get_commenters(group_id, posts)
    likers = get_likers(group_id, posts)

    return commenters.intersection(likers)


if __name__ == '__main__':
    load_dotenv()

    group_name = 'cocacola'
    print(get_vk_statistic(group_name))
