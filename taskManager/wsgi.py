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

def notify(when):
    requests.get("https://tasks-day-scheduler.herokuapp.com/notify/"+when)

def night():
    schedule.every().day.at("12:10").do(notify, "night")
    while True:
        schedule.run_pending()
        time.sleep(10)

def morning():
    schedule.every().day.at("12:15").do(notify, "morning")
    while True:
        schedule.run_pending()
        time.sleep(10)

def afternoon():
    schedule.every().day.at("12:20").do(notify, "afternoon")
    while True:
        schedule.run_pending()
        time.sleep(10)

def minutely():
    schedule.every(1).minutes.do(notify, "a")
    while True:
        schedule.run_pending()
        time.sleep(60)

t = threading.Thread(target=night)
t.start()
s = threading.Thread(target=morning)
s.start()
u = threading.Thread(target=minutely)
u.start()
