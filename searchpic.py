import requests
import json
from bs4 import BeautifulSoup

def load_img(blob:bytes):
    '''Загрузка изображения в форму.

    blob-принимает байты необходимого изображения.'''
    files = {'upfile': ('blob', blob, 'image/jpeg')} # Форма загрузки картинки
    search_params = {
        'rpt': 'imageview', 
        'format': 'json', 
        'request': '{"blocks":[{"block":"b-page_type_search-by-image__link"}]}'
    }
    response = requests.post(
        'https://yandex.ru/images/search', 
        params=search_params, 
        files=files,
    )
    
    query_string = json.loads(response.content)['blocks'][0]['params']['url']
    params = json.loads(response.content)['blocks'][0]['params']

    return params

def search_img(params):
    '''Совершает поиск на основе параметров загруженной картинки.

    params-json параметров картинки.'''
    rpt = 'imageview'
    from_ = 'tabbar'
    http_url = f"https://yandex.ru/images/search?rpt={rpt}&url={params['originalImageUrl']}&cbir_id={params['cbirId']}&from={from_}"
    r = requests.get(http_url)

    soup = BeautifulSoup(r.text, 'lxml')
    parent_block = soup.find('div', 
        class_='cbir-search-by-image-page__section cbir-search-by-image-page__section_name_tags'
    ) # Родительский блок поиска
    if parent_block: 
        tags = parent_block.find('div', 
            class_='Root Theme Theme_color_yandex-default Theme_root_default'
        )['data-state']
        tags_json = json.loads(tags)
    else:
        return 'Ничего не найдено'

    return [tag['text'] for tag in tags_json['tags']] # Вывод всех найденных вещей изображенных на картинке.