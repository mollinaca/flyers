import sys, os
import traceback
import json
import datetime
import pathlib
import configparser
import git
from . import f
from .yorkmart import yorkmart
from .meatmeet import meatmeet
from .gyoumusuper import gyoumusuper
from .welcia import welcia
from .supervalue import supervalue

def main ():
    debug = True
    dt_now = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    p = pathlib.Path(__file__).resolve().parent
    conf_file_path = str(p) + '/.settings.ini'
    config = configparser.ConfigParser()
    config.read(conf_file_path)
    token = config['flyers']['token']
    webhook = config['flyers']['webhook']
    webhook_dev = config['flyers']['webhook_dev']
    channel = config['flyers']['channel']
    channel_dev = config['flyers']['channel_dev']
    updated = False
    stores = ['yorkmart', 'meatmeet', 'gyoumusuper', 'welcia', 'supervalue']
    pf = f.prev_flyer ()

    try:
        if debug:
            text = '[debug] script start'
            print (text)
            f.iw (webhook_dev, text)

        for store in stores:
            if store == 'yorkmart': # ヨークマート
                york_flyers = yorkmart.get_flyers ()
                if store not in pf['stores'] or not (set(york_flyers['flyers']) == set(pf['detail'][store]['flyers'])):
                    updated = True
                    for flyer_url in york_flyers['flyers']:
                        if not flyer_url in pf['detail'][store]['flyers']:
                            filename = f.dl (flyer_url)
                            if not filename == 'Fail':
                                f.files_upload (token, channel, filename, flyer_url)
                                if debug:
                                    f.files_upload (token, channel_dev, filename, flyer_url)
                                os.remove (filename)
                            else:
                                message = 'チラシファイルのダウンロードに失敗しました。URL: ' + flyer_url
                                f.iw (webhook_dev, message)
                        else:
                            if debug:
                                text = flyer_url + ' has already posted in previous'
                                f.iw (webhook_dev, text)
                    if store not in pf['stores']:
                        pf['stores'].append(store)
                    pf['detail'][store] = york_flyers

                else:
                    if debug:
                        text = '[debug] ' + store + ' has no changed.'
                        print (text)
                        f.iw (webhook_dev, text)

            elif store == 'meatmeet': # ミートミート
                mm_flyers = meatmeet.get_flyers()
                if store not in pf['stores'] or not (set(mm_flyers['flyers']) == set(pf['detail'][store]['flyers'])):
                    updated = True
                    for flyer_url in mm_flyers['flyers']:
                        if not flyer_url in pf['detail'][store]['flyers']:
                            filename = f.dl (flyer_url)
                            if not filename == 'Fail':
                                f.files_upload (token, channel, filename, flyer_url)
                                if debug:
                                    f.files_upload (token, channel_dev, filename, flyer_url)
                                os.remove (filename)
                            else:
                                message = 'チラシファイルのダウンロードに失敗しました。URL: ' + flyer_url
                                f.iw (webhook_dev, message)
                        else:
                            if debug:
                                text = flyer_url + ' has already posted in previous'
                                f.iw (webhook_dev, text)
                    if store not in pf['stores']:
                        pf['stores'].append(store)
                    pf['detail'][store] = mm_flyers

                else:
                    if debug:
                        text = '[debug] ' + store + ' has no changed.'
                        print (text)
                        f.iw (webhook_dev, text)

            elif store == "gyoumusuper": # 業務スーパー
                gs_flyers = gyoumusuper.get_flyers()
                if store not in pf['stores'] or not (set(gs_flyers['flyers']) == set(pf['detail'][store]['flyers'])):
                    updated = True
                    for flyer_url in gs_flyers['flyers']:
                        if not flyer_url in pf['detail'][store]['flyers']:
                            filename = f.dl (flyer_url)
                            if not filename == 'Fail':
                                f.files_upload (token, channel, filename, flyer_url)
                                if debug:
                                    f.files_upload (token, channel_dev, filename, flyer_url)
                                os.remove (filename)
                            else:
                                message = 'チラシファイルのダウンロードに失敗しました。URL: ' + flyer_url
                                f.iw (webhook_dev, message)
                        else:
                            if debug:
                                text = flyer_url + ' has already posted in previous'
                                f.iw (webhook_dev, text)
                    if store not in pf['stores']:
                        pf['stores'].append(store)
                    pf['detail'][store] = gs_flyers

                else:
                    if debug:
                        text = '[debug] ' + store + ' has no changed.'
                        print (text)
                        f.iw (webhook_dev, text)

            elif store == "welcia": # ウエルシア
                pass # いったんパス
                wl_flyers = welcia.get_flyer_page_list ()
                wl_flyers_page_list = wl_flyers['flyers']
                if store not in pf['stores'] or not (set(wl_flyers_page_list) == set(pf['detail'][store]['flyers'])):
                    updated = True
                    for p in wl_flyers_page_list:
                        if not p in pf['detail'][store]['flyers']:
                            pics = welcia.get_flyers_pics (p)
                            for pic in pics:
                                f.files_upload (token, channel, pic, p)
                                if debug:
                                    f.files_upload (token, channel_dev, pic, p)
                                os.remove (pic)
                        else:
                            if debug:
                                text = p + ' has already posted in previous'
                                f.iw (webhook_dev, text)
                    if store not in pf['stores']:
                        pf['stores'].append(store)
                    pf['detail'][store] = wl_flyers
                else:
                    if debug:
                        text = '[debug] ' + store + ' has no changed.'
                        print (text)
                        f.iw (webhook_dev, text)

            elif store == "supervalue": # スーパーバリュー
                sv_flyers_page_list = supervalue.get_flyer_page_url ()
                if store not in pf['stores'] or not (set(sv_flyers_page_list) == set(pf['detail'][store]['flyers'])):
                    updated = True
                    for flyer_url in sv_flyers_page_list:
                        if not flyer_url in pf['detail'][store]['flyers']:
                            f.iw (webhook, flyer_url)
                            if debug:
                                f.iw (webhook_dev, flyer_url)
                        else:
                            if debug:
                                text = p + ' has already posted in previous'
                                f.iw (webhook_dev, text)
                    if store not in pf['stores']:
                        pf['stores'].append(store)
                    sv_flyers = {"updated_at":dt_now, "flyers": sv_flyers_page_list}
                    pf['detail'][store] = sv_flyers
                else:
                    if debug:
                        text = '[debug] ' + store + ' has no changed.'
                        print (text)
                        f.iw (webhook_dev, text)
            else:
                pass

        if updated:
            # ファイルを更新
            pf['updated_at'] = dt_now
            SCRIPT_DIR = pathlib.Path(__file__).resolve().parent.parent
            OUTPUT_DIR = pathlib.Path(str(SCRIPT_DIR) + '/docs/')
            OUTPUT_FILE_NAME = 'latest.json'
            OUTPUT_FILE = pathlib.Path(str(OUTPUT_DIR) + '/' + OUTPUT_FILE_NAME)
            with open(OUTPUT_FILE, mode='w') as fl:
                fl.write(json.dumps(pf, indent=4))

            # git push
            git_repo= git.Repo(SCRIPT_DIR)
            git_repo.index.add(str(OUTPUT_FILE))
            commit_message = '[auto] update ' + str(OUTPUT_FILE_NAME)
            git_repo.index.commit(commit_message)
            git_repo.remotes.origin.push('HEAD')
            if debug:
                text = '[debug] git push'
                print (text)
                f.iw(webhook_dev, text)

        if debug:
            text = '[debug] script finished'
            print (text)
            f.iw (webhook_dev, text)

    except Exception as e:
        err_msg = '```' + '[Exception]\n' + str(e) + '\n' + '[StackTrace]' + '\n' + traceback.format_exc() + '```'
        f.iw (webhook_dev, err_msg)

if __name__ == '__main__':
    main ()
