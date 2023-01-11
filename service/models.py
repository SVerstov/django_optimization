from django.core.validators import MaxValueValidator
from django.db import models

from clients.models import Client
from service.tasks import calculate_price


# Create your models here.
class Service(models.Model):
    name = models.CharField(max_length=50)
    full_price = models.PositiveIntegerField()

    def __str__(self):
        return self.name

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__full_price = self.full_price

    def save(self, *args, **kwargs):
        if self.__full_price != self.full_price:
            for subscription in self.subscriptions.all():
                calculate_price.delay(subscription.id)

        self.__full_price = self.full_price
        return super().save(*args, **kwargs)


class Plan(models.Model):
    PLAN_TYPES = (
        ('full', 'Full'),
        ('student', 'Student'),
        ('discount', 'Discount')
    )

    plan_types = models.CharField(choices=PLAN_TYPES, max_length=10)
    discount_percent = models.PositiveIntegerField(default=0,
                                                   validators=[
                                                       MaxValueValidator(100)
                                                   ])

    def __str__(self):
        return f'{self.plan_types} - {self.discount_percent}%'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__discount_percent = self.discount_percent

    def save(self, *args, **kwargs):
        if self.__discount_percent != self.discount_percent:
            for subscription in self.subscriptions.all():
                calculate_price.delay(subscription.id)

        self.__discount_percent = self.discount_percent
        return super().save(*args, **kwargs)


class Subscription(models.Model):
    client = models.ForeignKey(Client, related_name='subscriptions', on_delete=models.PROTECT)
    service = models.ForeignKey(Service, related_name='subscriptions', on_delete=models.PROTECT)
    plan = models.ForeignKey(Plan, related_name='subscriptions', on_delete=models.PROTECT)
    price = models.FloatField(default=0)

    def __str__(self):
        return f'{self.client.user.username} - {self.service.name} - {self.plan}'
