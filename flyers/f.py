import traceback
import json
import pathlib
import configparser
import requests
import urllib.request
import git
from bs4 import BeautifulSoup
from selenium import webdriver
from PIL import Image

def testf ():
    print ("testf")
    return 0

def iw (webhook_url:str, message:str):
    """
    SlackチャンネルへIncomingWebhookを使ってメッセージをポストする
    """
    data = json.dumps({
    'text' : message
    })
    res = requests.post(webhook_url, data=data)
    return res

