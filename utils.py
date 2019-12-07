import datetime
import requests


def check_comment_date_fb(publish_date, period_days=30):
    time = publish_date.split('T')[0]
    year, month, day = time.split('-')

    pub_date = datetime.datetime(year=int(year), month=int(month), day=int(day)).timestamp()

    return check_comment_date(pub_date, period_days)


def check_comment_date(publish_date, period_days=90):
    today = datetime.datetime.today().timestamp()
    # Разница между сегодня и датай публикации < 90 дней в секундах
    if today - publish_date < period_days * 24 * 60 * 60:
        return True
    return False


def get_objects(base_url, url_for_request, params: dict, obj_per_page, max_count=None):
    obj = []
    response = requests.get(f"{base_url}/{url_for_request}", params=params).json()['response']
    objcects_count = response['count']

    for page in get_pagination(objcects_count, obj_per_page=obj_per_page, max_count=max_count):
        params['offset'] = page[0]
        params['count'] = page[1]

        response = requests.get(f"{base_url}/{url_for_request}", params=params)
        response.raise_for_status()

        obj += response.json()['response']['items']
    return obj


def get_pagination(obj_count, obj_per_page=100, max_count=None):
    """
    Возвращает генератор, на каждой итерации которого возвращается список, первым аргументом которого
    является текущее смещение, а вторым - количество объектов для запроса
    """
    current_offset = 0

    if max_count:
        obj_count = max_count
        if obj_count < obj_per_page:
            obj_per_page = obj_count

    while obj_count > 0:
        if obj_per_page > obj_count:
            obj_per_page = obj_count

        yield [current_offset, obj_per_page]

        obj_count -= obj_per_page
        current_offset += obj_per_page
