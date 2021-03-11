import sys, os
import datetime, time
import pathlib
import configparser
from . import f

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

    f.testf ()
    message = "testdayo"
    f.iw(webhook_dev,message)


if __name__ == '__main__':
    main ()
