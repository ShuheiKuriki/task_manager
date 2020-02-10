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
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'taskManager.settings.prod')

application = get_wsgi_application()

def notify(msg):
    requests.get("http://tasks-day-scheduler.herokuapp.com/notify")

def daily():
    schedule.every().day.at("23:30").do(notify)
    while True:
        schedule.run_pending()
        time.sleep(60)

def secondly():
    schedule.every(1).seconds.do(notify)
    while True:
        schedule.run_pending()
        time.sleep(1)

t = threading.Thread(target=secondly)
t.start()
