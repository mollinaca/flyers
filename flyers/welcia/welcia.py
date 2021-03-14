import sys,os
import datetime, time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from .. import f

""" サンプルページ
チラシ1枚ページ http://s-cmn.shufoo.net/chirashi/298280/37174623802166/?
チラシ2枚ページ http://s-cmn.shufoo.net/chirashi/298280/97116123867838/?
"""


def get_flyer_page_list () -> list:
    """
    ウエルシアのチラシ
    shufoo のチラシ取得はちょっと難しい
    この機能は、アクセスしたページに "必ずチラシが1枚以上存在する" ことを前提としている。もし表示できるチラシがなかったらのパターンは想定できていない。
    """
    dt_now = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100'
    headers = {'User-Agent': ua}

    # チラシURL抜きのページへアクセスし、この店舗のチラシページが複数存在するか確認する
    # 1ページのみ "以下 cf 要素が空" ならそのページのみを処理
    # 複数ページある場合は各ページを処理する
    shufoo_url = 'http://s-cmn.shufoo.net' 
    load_url = shufoo_url + '/chirashi/298280/'
    res = requests.get (load_url, headers=headers)
    html = BeautifulSoup (res.content, 'html.parser')
    cf = html.findAll(class_="list_ui list_ui_B")[0].findAll(class_='cF')
    flyer_page_list = []
    if not cf:
        # チラシが1枚で当該ページのみだった場合
        flyer_page_list.append (load_url)
    else:
        # チラシが複数ページにまたがって存在する → まずページのURLをすべて取得する
        for l in cf:
            cf_url = l.get('href')
            cf_url = shufoo_url + cf_url
            flyer_page_list.append (cf_url)

        res = requests.get (flyer_page_list[0], headers=headers)
        html = BeautifulSoup (res.content, 'html.parser')
        cf = html.findAll(class_="list_ui list_ui_B")[0].findAll(class_='cF')
        for l in cf:
            cf_url = l.get('href')
            cf_url = shufoo_url + cf_url
            if not cf_url in flyer_page_list:
                flyer_page_list.append (cf_url)

    return flyer_page_list

def get_flyers_pics (page_url:str) -> list:
    """
    ページURLから画像を取得してファイル名を返す
    1つのURLから1枚取れるパターンと2枚取れるパターンがあるためリストで返す
    """
    # 各ページに画像が1枚なのか複数枚なのかを、ページ毎に確認する
    pics = []
    driver = webdriver.PhantomJS(executable_path='/usr/local/bin/phantomjs', service_log_path=os.path.devnull)
    driver.get(page_url)
    body = driver.page_source
    html = BeautifulSoup (body, 'html.parser')
    n = int(html.find('div', {'class':'cv_pager_number'}).get_text().split('/')[1].strip())

    p = page_url.split('/')[-2]
    filename = 'welcia_' + p + '.jpg'
    sliceimg_url_list = []
    L = html.findAll(class_='cv_panel')[0].select('img')
    for l in L:
        sliceimg_url_list.append(l.get('src'))

    images = []
    for img_url in sliceimg_url_list:
        title = img_url.split('/')[-1]
        images.append(title)
        f.dl (img_url)
    images_left = []
    images_right = []
    for i,img in enumerate(images):
        if i%2 == 0:
            images_left.append(img)
        else:
            images_right.append(img)
    f.concat_v (images_left).save('left.jpg')
    f.concat_v (images_right).save('right.jpg')
    f.concat_h (['left.jpg','right.jpg']).save(filename)
    pics.append (filename)

    for img in images:
        os.remove(img)
    os.remove('right.jpg')
    os.remove('left.jpg')

    if n == 2: # 裏表で２枚あるページ
        # 2枚目のファイル名は 1枚目の image1 が image2 に変わっただけなのでそのままURLをいじって取得する
        # この部分が変更されたら追従が必要
        filename = 'welcia_' + p + '_2' + '.jpg'
        images = []
        for img_url in sliceimg_url_list:
            img_url = img_url.replace('image1','image2')
            title = img_url.split('/')[-1]
            images.append(title)
            f.dl (img_url)
        images_left = []
        images_right = []
        for i,img in enumerate(images):
            if i%2 == 0:
                images_left.append(img)
            else:
                images_right.append(img)
        f.concat_v (images_left).save('left.jpg')
        f.concat_v (images_right).save('right.jpg')
        f.concat_h (['left.jpg','right.jpg']).save(filename)
        pics.append (filename)

        for img in images:
            os.remove(img)
        os.remove('right.jpg')
        os.remove('left.jpg')

    return pics
