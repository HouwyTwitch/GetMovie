from .utils import get_latest_chrome_useragent
import requests
from functools import lru_cache


LATEST_USERAGENT = get_latest_chrome_useragent()

cookies = {
    'mobile': 'no',
    'disable_server_sso_redirect': '1'
}

headers = {
    'accept': '*/*',
    'accept-language': 'ru,en;q=0.9',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    'origin': 'https://www.kinopoisk.ru',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://www.kinopoisk.ru/',
    'service-id': '25',
    'user-agent': LATEST_USERAGENT,
}

params = {
    'operationName': 'SuggestSearch',
}

query = 'query SuggestSearch($keyword: String!, $yandexCityId: Int, $limit: Int) { suggest(keyword: $keyword) { top(yandexCityId: $yandexCityId, limit: $limit) { topResult { global { ...SuggestMovieItem ...SuggestPersonItem ...SuggestCinemaItem ...SuggestMovieListItem __typename } __typename } movies { movie { ...SuggestMovieItem __typename } __typename } persons { person { ...SuggestPersonItem __typename } __typename } cinemas { cinema { ...SuggestCinemaItem __typename } __typename } movieLists { movieList { ...SuggestMovieListItem __typename } __typename } __typename } __typename } } fragment SuggestMovieItem on Movie { id contentId title { russian original __typename } rating { kinopoisk { isActive value __typename } __typename } poster { avatarsUrl fallbackUrl __typename } viewOption { buttonText isAvailableOnline: isWatchable(filter: {anyDevice: false, anyRegion: false}) purchasabilityStatus contentPackageToBuy { billingFeatureName __typename } type availabilityAnnounce { groupPeriodType announcePromise availabilityDate type __typename } __typename } ... on Film { type productionYear __typename } ... on TvSeries { releaseYears { end start __typename } __typename } ... on TvShow { releaseYears { end start __typename } __typename } ... on MiniSeries { releaseYears { end start __typename } __typename } __typename } fragment SuggestPersonItem on Person { id name originalName birthDate poster { avatarsUrl fallbackUrl __typename } __typename } fragment SuggestCinemaItem on Cinema { id ctitle: title city { id name geoId __typename } __typename } fragment SuggestMovieListItem on MovieListMeta { id cover { avatarsUrl __typename } coverBackground { avatarsUrl __typename } name url description movies(limit: 0) { total __typename } __typename } '

@lru_cache(256)
def kinopoisk_search(keyword):
    json_data = {
        'operationName': 'SuggestSearch',
        'variables': {
            'keyword': keyword,
            'yandexCityId': 192,
            'limit': 3,
        },
        'query': query,
    }

    try:
        response = requests.post('https://graphql.kinopoisk.ru/graphql/', params=params, cookies=cookies, headers=headers, json=json_data)
        content = response.json()
        movies = [content['data']['suggest']['top']['topResult']['global']] + [x['movie'] for x in content['data']['suggest']['top']['movies']]
        return {x['id']: (x['title']['russian'],
                          x['title']['original']) for x in movies}
    except:
        return {}

