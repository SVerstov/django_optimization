from celery import shared_task
from django.db.models import F


@shared_task
def calculate_price(subscription_id):
    """ calculate and save price to DB for subscription"""
    from service.models import Subscription

    subscription = Subscription.objects.filter(id=subscription_id).annotate(
        annotated_price=F('service__full_price') * (1 - F('plan__discount_percent') / 100.00)).first()

    subscription.price = subscription.annotated_price
    subscription.save()
