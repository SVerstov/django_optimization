from django.core.cache import cache
from django.db.models.signals import pre_delete, post_save
from django.dispatch import receiver
from service.models import Subscription
from django.conf import settings
from service.tasks import calculate_price


@receiver(post_save, sender=Subscription)
def recalculate_price(sender, instance, **kwargs):
    calculate_price.delay(instance.id)


@receiver(pre_delete, sender=Subscription)
def delete_price_cache(sender, instance, **kwargs):
    cache.delete(settings.PRICE_CACHE_NAME)
