"""
WSGI config for taskManager project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os
import time
import schedule
import threading
import requests
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'taskManager.settings.prod')

application = get_wsgi_application()

def notify():
    requests.get("https://tasks-day-scheduler.herokuapp.com/notify")

def daily():
    schedule.every().day.at("17:20").do(notify)
    while True:
        schedule.run_pending()
        time.sleep(60)

def minutely():
    schedule.every(1).minutes.do(notify)
    while True:
        schedule.run_pending()
        time.sleep(1)

t = threading.Thread(target=daily)
t.start()
