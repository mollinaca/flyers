import sys, os
import datetime, time
import pathlib
import configparser
from . import f
from .yorkmart import yorkmart

def main ():
    dt_now = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    p = pathlib.Path(__file__).resolve().parent
    config = configparser.ConfigParser()
    config.read(str(p)+'/.settings.ini')
    token = config['flyers']['token']
    webhook = config['flyers']['webhook']
    webhook_dev = config['flyers']['webhook_dev']
    channel = config['flyers']['channel']
    channel_dev = config['flyers']['channel_dev']
    updated = False

    stores = ['yorkmart']
    pf = f.prev_flyer ()

    for store in stores:
        if store == 'yorkmart': # ヨークマート
            york_flyers = yorkmart.get_flayers ()
            if store not in pf['detail'] or not (set(york_flyers['flyers']) == set(pf['detail'][store]['flyers'])):
                # pf に存在しないスーパー or pf にあるデータと一致しないURLを取得した → チラシに更新があった
                # 新しいチラシを取得してPOSTする
                updated = True
                for flyer_url in york_flyers['flyers']:
                    filename = f.dl (flyer_url)
                    if not filename == 'Fail':
                        f.files_upload (token, channel_dev, filename, flyer_url)
                        os.remove (filename)
                    else:
                        message = 'チラシファイルのダウンロードに失敗しました。URL: ' + flyer_url
                        f.iw (webhook_dev, message)
            else:
                text = '[debug] ' + store + ' has no changed.'
                print (text)

        else:
            pass

    if updated: # チラシに更新があった
        pass

if __name__ == '__main__':
    main ()
