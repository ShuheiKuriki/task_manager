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

def daily():
    schedule.every().day.at("09:00").do(notify, "morning")
    schedule.every().day.at("16:00").do(notify, "afternoon")
    schedule.every().day.at("22:30").do(notify, "night")
    # schedule.every(2).minutes.do(notify, "a")
    while True:
        schedule.run_pending()
        logger.error("pending")
        time.sleep(120)
        requests.get("https://tasks-day-scheduler.herokuapp.com/")
        logger.error("sleep_done")

def test():
    logger.error("test")

t = threading.Thread(target=daily)
t.start()
