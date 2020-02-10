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

def night():
    schedule.every().day.at("22:30").do(notify, "night")
    while True:
        schedule.run_pending()
        time.sleep(300)

def morning():
    schedule.every().day.at("07:00").do(notify, "morning")
    while True:
        schedule.run_pending()
        time.sleep(300)

def afternoon():
    schedule.every().day.at("14:00").do(notify, "afternoon")
    while True:
        schedule.run_pending()
        time.sleep(300)

def minutely():
    schedule.every(1).minutes.do(notify, "")
    while True:
        schedule.run_pending()
        time.sleep(1)

t = threading.Thread(target=night)
t.start()
s = threading.Thread(target=morning)
s.start()
u = threading.Thread(target=afternoon)
u.start()
