import PySimpleGUI as sg
from src.kinopoisk import kinopoisk_search
from time import time
from src.dontplayfb import get_players
from src.allohalive import get_movie_details, get_movie_streams,\
                           get_file_content, get_raw_content
from src.utils import sanitize_filename
from json import loads
from threading import Thread


layout = [[sg.T('Movie name:'), sg.In('', key='Movie-search', enable_events=True)],
          [sg.Listbox([], size=(56, 16), key='movies-list', enable_events=True)],
          [sg.T('', key='status'), sg.Push(), sg.B('Download', disabled=True, key='download-button')]]

window = sg.Window('GetFilm', layout)

latest_search = ''
latest_result = []
latest_movie_list = []
latest_search_time = 0
latest_selected_movie = ''
selected_movie_id = 0


def download_movie(segment_files, movie_filename):
    for i, x in enumerate(segment_files):
        window['status'].update(f'Downloading: {i+1} / {len(segment_files)}')
        content = None
        while content == None:
            content = get_raw_content(best_quality_master_link.replace('master.m3u8', x))
        open(movie_filename, 'ab').write(content)

while True:
    event, values = window.read(timeout = 33)
    if event == sg.WIN_CLOSED:
        break
    if values['Movie-search'] != '' and values['Movie-search'] != latest_search and \
        time()-latest_search_time > 1 and values['Movie-search'] != latest_search:
        latest_search_time = time()
        latest_search = values['Movie-search']
        latest_result = kinopoisk_search(latest_search)
        latest_movie_list = [f'{x[1]} ({x[0]})' for x in latest_result.values()]
        window['movies-list'].update(latest_movie_list)
    if event == 'movies-list':
        if values['movies-list'][0] != '' and values['movies-list'][0] != latest_selected_movie:
            latest_selected_movie = values['movies-list'][0]
            index = latest_movie_list.index(latest_selected_movie)
            selected_movie_id = list(latest_result.keys())[index]
            window['status'].update(f'Selected: {latest_result[selected_movie_id][1]}')
            window['download-button'].update(disabled=False)
    if event == 'download-button' and selected_movie_id != 0:
        window['status'].update('Looking for players...')
        players = get_players(str(selected_movie_id))
        alloha_iframe_url = ''
        for player in players:
            if player['type'] == 'ALLOHA':
                alloha_iframe_url = player['iframeUrl']
                break
        if alloha_iframe_url != '':
            window['status'].update('Found alloha iframe url')
        else:
            window['status'].update('No alloha iframe url found')
        if alloha_iframe_url != '':
            content = get_movie_details(alloha_iframe_url)
            content = content.decode('utf-8-sig', errors='ignore')
            config = loads(content.split('fileList = JSON.parse(\'')[-1].split('\');')[0])
            if config['type'] == 'movie':
                allohalive_id = config['active']['id']
                streams = get_movie_streams(alloha_iframe_url, allohalive_id)
                # TODO New window to select audio and video quality
                stream = streams[0]
                best_quality_master_link = list(stream['quality'].values())[0].split(' or ')[0]
                master_m3u8 = get_file_content(best_quality_master_link).split('\n')
                index_m3u8 = get_file_content(best_quality_master_link.replace('master.m3u8', master_m3u8[2])).split('\n')
                segment_files = []
                for x in index_m3u8:
                    if 'seg-' in x:
                        segment_files.append(x)
                if '.m4s' in segment_files[0]:
                    init_file = ''
                    for x in index_m3u8:
                        if '#EXT-X-MAP:URI="' in x:
                            init_file = x.split('#EXT-X-MAP:URI="')[-1].split('"')[0]
                            init_file = best_quality_master_link.replace('master.m3u8', init_file)
                            break
                    movie_filename = f'downloads/{sanitize_filename(latest_result[selected_movie_id][1])}.mp4'
                    if init_file == '':
                        init_file = best_quality_master_link.replace('master.m3u8', 'init-c1-f1-v1-a1.mp4')
                    open(movie_filename, 'ab').write(get_raw_content(init_file))
                    Thread(target=download_movie, args=(segment_files, movie_filename)).start()
                elif '.ts' in segment_files[0]:
                    movie_filename = f'downloads/{sanitize_filename(latest_result[selected_movie_id][1])}.ts'
                    open(movie_filename, 'ab').write(b'')
                    Thread(target=download_movie, args=(segment_files, movie_filename)).start()
                    # TODO Download .ts files
                else:
                    print(index_m3u8)
            else:
                print(config)



window.close()