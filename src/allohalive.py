import requests
from .kinopoisk import LATEST_USERAGENT

headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9,ru;q=0.8,zh-CN;q=0.7,zh;q=0.6,ko;q=0.5',
    'cache-control': 'no-cache',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'origin': 'https://thesaurus.allohalive.com',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://thesaurus.allohalive.com',
    'user-agent': LATEST_USERAGENT,
    'x-requested-with': 'XMLHttpRequest',
}

def get_movie_details(iframe_url: str):
    try:
        response = requests.get(iframe_url, headers=headers)
        return response.content
    except:
        return None

def get_movie_streams(iframe_url: str, allohalive_id):
    token = iframe_url.split('token=')[-1]
    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9,ru;q=0.8,zh-CN;q=0.7,zh;q=0.6,ko;q=0.5',
        'cache-control': 'no-cache',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://thesaurus.allohalive.com',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': f'{iframe_url}&null=',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

    data = {
        'token': token,
        'av1': 'true',
        'autoplay': '0',
        'audio': '',
        'subtitle': '',
    }

    try:
        response = requests.post(f'https://thesaurus.allohalive.com/movie/{allohalive_id}', headers=headers, data=data)
        return response.json()['hlsSource']
    except:
        return []

def get_file_content(link: str):
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9,ru;q=0.8,zh-CN;q=0.7,zh;q=0.6,ko;q=0.5',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Origin': 'https://thesaurus.allohalive.com',
        'Pragma': 'no-cache',
        'Referer': 'https://thesaurus.allohalive.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'User-Agent': LATEST_USERAGENT,
    }

    try:
        response = requests.get(link, headers=headers)
        content = response.content.decode('utf-8-sig', errors='ignore')
        return content
    except:
        return ''

def get_raw_content(link: str):
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9,ru;q=0.8,zh-CN;q=0.7,zh;q=0.6,ko;q=0.5',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Origin': 'https://thesaurus.allohalive.com',
        'Pragma': 'no-cache',
        'Referer': 'https://thesaurus.allohalive.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'User-Agent': LATEST_USERAGENT,
    }

    try:
        response = requests.get(link, headers=headers)
        return response.content
    except Exception as e:
        print(str(e))
        return None