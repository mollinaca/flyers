import datetime, time
import requests
import urllib.request
from bs4 import BeautifulSoup

def get_flyers () -> dict:
    """
    ミートミートのチラシ情報
    """
    dt_now = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100'
    headers = {'User-Agent': ua}

    # チラシページURLを取得
    tokubai_url = 'https://tokubai.co.jp'
    load_url = tokubai_url + '/MEATMeet%E9%A3%9F%E8%82%89%E5%8D%B8%E5%A3%B2%E3%82%BB%E3%83%B3%E3%82%BF%E3%83%BC/174289'

    res = requests.get (load_url, headers=headers)
    html = BeautifulSoup (res.content, 'html.parser')
    leaflet_page_url = tokubai_url + html.findAll(class_='leaflet_component')[0].find(class_='image_element').get('href')

    time.sleep(2) # be gentle
    res = requests.get (leaflet_page_url, headers=headers)
    html = BeautifulSoup (res.content, 'html.parser')
    leaflet_page_link = html.find_all(class_='other_leaflet_link')

    # チラシページリンクのチラシページリンクURL（複数）を取得
    leaflet_page_links = []
    for l in leaflet_page_link:
        leaflet_page_links.append(tokubai_url + l.get('href').split('?')[0])

    # 各チラシページリンクURLを開いて、チラシの画像ファイルURLを取得
    leaflet_links = []
    for url in leaflet_page_links:
        time.sleep(2) # be gentle
        res = requests.get (url, headers=headers)
        html = BeautifulSoup(res.content, 'html.parser')
        leaflet_links.append(html.find(class_='leaflet').get('src').split('?')[0])

    ret = {'updated_at':dt_now, 'flyers':leaflet_links}
    return ret
