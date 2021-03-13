import datetime
import requests
from bs4 import BeautifulSoup

def yorktest ():
    print ("yorkmart!")
    return 0

def get_flyers () -> dict:
    """
    ヨークマートのチラシ情報
    """
    dt_now = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

    # 最新のチラシのファイル名を取得
    york_url = 'https://www.york-inc.com'
    load_url = york_url + '/store/%e5%a4%a7%e5%ae%ae%e5%8d%97%e4%b8%ad%e9%87%8e%e5%ba%97.html'
    res = requests.get (load_url)
    html = BeautifulSoup (res.content, 'html.parser')
    leaflet = html.find_all (class_='leaflet pc')
    yorkmart_flyers = []
    for l in leaflet:
        for l2 in list (l.findAll('img')[0].get('data-set').split(',')):
            if 'ul-files' in l2:
                yorkmart_flyers.append (york_url + l2)

    ret = {'updated_at':dt_now, 'flyers':yorkmart_flyers}
    return ret

