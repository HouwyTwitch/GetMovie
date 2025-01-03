import requests
from .kinopoisk import LATEST_USERAGENT

headers = {
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.9,ru;q=0.8,zh-CN;q=0.7,zh;q=0.6,ko;q=0.5',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Origin': 'https://flicksbar.mom',
    'Pragma': 'no-cache',
    'Referer': 'https://flicksbar.mom/',
    'User-Agent': LATEST_USERAGENT
}

def get_players(kinopoisk_id: str):
    params = {'kinopoisk': kinopoisk_id}
    try:
        response = requests.get('https://dontplayfb.top/kinobox/index.php', params=params, headers=headers)
        return response.json()['data']
    except:
        return []