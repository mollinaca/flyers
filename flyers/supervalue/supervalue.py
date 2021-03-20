import sys,os
import datetime, time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from .. import f
""" サンプルページ
店舗   https://www.supervalue.jp/shop/detail/10
チラシ https://www.supervalue.jp/leaflet/uploads/20210314102302LJYz/
"""

def get_flyer_page_url () -> list:
    """
    supervalue のチラシ
    OpenSeadragon のページからチラシの取得の仕方がわからないのでURLだけで諦める
    """
    dt_now = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100'
    headers = {'User-Agent': ua}

    # 店舗ページへアクセスし掲載されているチラシへのリンクを取得する
    supervalue_url = 'https://www.supervalue.jp'
    store_url = supervalue_url + '/shop/detail/10'
    res = requests.get (store_url, headers=headers)
    html = BeautifulSoup (res.content, 'html.parser')
    leaflet_btn_url = html.findAll(class_="leaflet-btn")[0].get('href')
    leaflet_page_url = supervalue_url + leaflet_btn_url
    flyer_page_list = [leaflet_page_url]

    return flyer_page_list
