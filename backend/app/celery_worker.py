from celery import Celery


def make_celery(app_name=__name__):
    return Celery(app_name, broker='redis://localhost:6379/0')


celery = make_celery()
