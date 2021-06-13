import datetime, time
import requests
from bs4 import BeautifulSoup

def get_flyers ():
    dt_now = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100'
    headers = {'User-Agent': ua}
    leaflet_links = []

    # チラシページURLを取得
    tokubai_url = 'https://tokubai.co.jp'
    load_url = tokubai_url + '/%E6%A5%AD%E5%8B%99%E3%82%B9%E3%83%BC%E3%83%91%E3%83%BC/169887'
    res = requests.get (load_url, headers=headers)
    html = BeautifulSoup (res.content, 'html.parser')
    if html.findAll(class_='leaflet_component') == []:
        # チラシがなかった
        ret = {'updated_at':dt_now, 'flyers':leaflet_links}
        return ret
    else:
        leaflet_page_url = tokubai_url + html.findAll(class_='leaflet_component')[0].find(class_='image_element').get('href')

    res = requests.get (leaflet_page_url, headers=headers)
    html = BeautifulSoup (res.content, 'html.parser')
    leaflet_page_link = html.find_all (class_='other_leaflet_link')

    # チラシページリンクのチラシページリンクURL（複数）を取得
    leaflet_page_links = []
    for l in leaflet_page_link:
        leaflet_page_links.append (tokubai_url + l.get('href').split('?')[0])

    # 各チラシページリンクURLを開いて、チラシの画像ファイルURLを取得
    for url in leaflet_page_links:
        res = requests.get (url, headers=headers)
        html = BeautifulSoup (res.content, 'html.parser')
        leaflet_links.append (html.find(class_='leaflet').get('src').split('?')[0])

    ret = {'updated_at':dt_now, 'flyers':leaflet_links}
    return ret
