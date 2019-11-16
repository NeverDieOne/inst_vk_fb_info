import datetime
import requests


def check_comment_date(publish_date, period_days=90):
    today = datetime.datetime.today().timestamp()
    # Разница между сегодня и датай публикации < 90 дней в секундах
    if today - publish_date < period_days * 24 * 60 * 60:
        return True
    return False


# TODO придумать новое имя функции
def pagination(base_url, url_for_request, params: dict, obj_per_page):
    obj = []
    response = requests.get(f"{base_url}/{url_for_request}", params=params).json()['response']
    obj += response['items']
    pages_number = response['count']

    while params['offset'] < pages_number:
        params['offset'] += obj_per_page
        page_response = requests.get(f"{base_url}/{url_for_request}", params=params)
        page_response.raise_for_status()

        obj += page_response.json()['response']['items']

    return obj
