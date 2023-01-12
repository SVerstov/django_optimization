import time
from datetime import datetime

from celery import shared_task
from django.conf import settings
from django.core.cache import cache
from django.db import transaction
from django.db.models import F
from celery_singleton import Singleton


@shared_task(base=Singleton)
def calculate_price(subscription_id):
    """ calculate and save price to DB for subscription"""

    time.sleep(5)  # work simulate

    from service.models import Subscription

    with transaction.atomic():
        subscription = Subscription.objects.filter(id=subscription_id).annotate(
            annotated_price=F('service__full_price') * (1 - F('plan__discount_percent') / 100.00)).first()

        subscription.price = subscription.annotated_price

        subscription.save()
    cache.delete(settings.PRICE_CACHE_NAME)


@shared_task(base=Singleton)
def add_comment(subscription_id):
    """ calculate and save price to DB for subscription"""
    from service.models import Subscription

    time.sleep(5)  # work simulate

    with transaction.atomic():
        subscription = Subscription.objects.filter(id=subscription_id).first()
        subscription.comment = str(datetime.now())
        subscription.save()
