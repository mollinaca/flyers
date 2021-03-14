import sys,os
import traceback
import time
import shutil
import json
import requests
from selenium import webdriver
from PIL import Image

class ScriptError (Exception):
    pass

def iw (webhook:str, message:str):
    """
    post message to slack channel
    """
    data = json.dumps({
    'text' : message
    })
    res = requests.post(webhook, data=data)
    return res

def files_upload (token:str, channel:str, filename:str, comment:str):
    """
    upload file to slack channel
    """
    url = 'https://slack.com/api/files.upload'
    files = {'file': open(filename, 'rb')}
    data = {
        'token': token,
        'channels': channel,
        'filename': filename,
        'initial_comment': comment,
        'filetype': 'jpg',
        'file': files
    }
    res = requests.post(url, data=data, files=files)
    return res

def dl (url:str) -> str:
    """
    download file from web and save to local
    """
    filename = os.path.basename(url)
    res = requests.get(url, stream=True)
    if not res.status_code == 200:
        time.sleep(60)
        res = requests.get(url, stream=True)
        if not res.status_code == 200:
            return 'Fail'

    with open(filename, 'wb') as file:
        res.raw.decode_content = True
        shutil.copyfileobj(res.raw, file)

    return filename

def concat_h (images:list):
    """
    connect images(list) horizontally
    """
    n = len(images)
    im0 = Image.open(images[0])
    ret = Image.new('RGB',(im0.width*n, im0.height))
    for i,img in enumerate(images):
        im = Image.open(img)
        ret.paste(im, (im0.width*i, 0))
    return ret

def concat_v (images:list):
    """
    concat images(list) vertically
    """
    n = len(images)
    im0 = Image.open(images[0])
    ret = Image.new('RGB',(im0.width, im0.height*n))
    for i,img in enumerate(images):
        im = Image.open(img)
        ret.paste(im, (0, im0.height*i))
    return ret

def prev_flyer () -> dict:
    """
    get previous flyer info from my WebAPI
    """
    url = 'https://mollinaca.github.io/flyers/latest.json'
#   url = 'https://mollinaca.github.io/flyers/latest_test.json'
    res = requests.get(url)
    if res.status_code == 200:
        body = res.text
    else:
        time.sleep(60)
        res = requests.get(url)
        if res.status_code == 200:
            body = res.text
        else:
            raise ScriptError ('Error: get latest.json not 200')
    ret = json.loads(body)
    return ret
