from instabot import Bot
import os
from dotenv import load_dotenv
import collections
from utils import check_comment_date


def get_comments_top(bot, posts):
    """Топ по количеству комментариев.

    Возвращает топ людей по колличеству оставленных комментариев под всеми постами.

    Args:
        bot: instance класса Bot
        posts (list): список постов, по которым требуется посчитать комментарии

    Returns:
        dict: {user_id: comments_count}
    """
    users = []
    for post_id in posts:
        users += [comment['user_id'] for comment in bot.get_media_comments_all(post_id) if
                  check_comment_date(comment['created_at'])]

    return dict(collections.Counter(users))


def get_posts_top(bot, posts):
    """Топ по количеству постов.

    Возвращает топ людей по количеству прокоммментированных постов.

    Args:
        bot: instance класса Bot
        posts (list): список постов, по которым необходимо составить топ

    Returns:
        dict: {user_id: posts_count}
    """
    posts_top = collections.Counter()
    for post_id in posts:
        users = (comment['user_id'] for comment in bot.get_media_comments_all(post_id) if
                 check_comment_date(comment['created_at']))

        posts_top += collections.Counter(users)

    return dict(posts_top)


def get_inst_statistic(bot, user_name):
    user_id = bot.get_user_id_from_username(user_name)
    user_posts = bot.get_total_user_medias(user_id)

    comments_top = get_comments_top(bot, user_posts)
    posts_top = get_posts_top(bot, user_posts)

    return comments_top, posts_top


if __name__ == '__main__':
    load_dotenv()

    bot = Bot(base_path='./inst')
    bot.login(username=os.getenv('INST_LOGIN'), password=os.getenv('INST_PASSWORD'))

    user_name_inst = 'cocacolarus'
    print(get_inst_statistic(bot, user_name_inst))
