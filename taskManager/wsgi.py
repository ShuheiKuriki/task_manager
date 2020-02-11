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
import logging

logger = logging.getLogger(__name__)
# logger.setLevel(10)
pid = os.getpid()
thread_name = threading.current_thread().getName()
logger.error("pid:{}".format(pid))
logger.error("thread_name:{}".format(thread_name))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'taskManager.settings.prod')

application = get_wsgi_application()

def notify(when):
    requests.get("https://tasks-day-scheduler.herokuapp.com/notify/"+when)

def night():
    schedule.every().day.at("14:38").do(notify, "night")
    while True:
        schedule.run_pending()
        time.sleep(60)

def morning():
    schedule.every().day.at("14:41").do(notify, "morning")
    while True:
        schedule.run_pending()
        time.sleep(60)

def afternoon():
    schedule.every().day.at("14:44").do(notify, "afternoon")
    while True:
        schedule.run_pending()
        time.sleep(60)

def minutely():
    # schedule.every(2).minutes.do(notify, "a")
    notify("a")
    logger.error("notify")
    # while True:
    #     schedule.run_pending()
    #     logger.error("I'm going to bed")
    #     time.sleep(60)
    #     logger.error("I'm awake")
def test():
    logger.error("test")

t = threading.Thread(target=night)
s = threading.Thread(target=morning)
u = threading.Thread(target=afternoon)
logger.error("start")
s.start()
t.start()
u.start()
