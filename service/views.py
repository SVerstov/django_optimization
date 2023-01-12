from django.conf import settings
from django.db.models import Prefetch, F, Sum
from django.shortcuts import render
from rest_framework.viewsets import ReadOnlyModelViewSet
from django.core.cache import cache

from clients.models import Client
from service.models import Subscription
from service.serializer import SubscriptionSerializer


class SubscriptionView(ReadOnlyModelViewSet):
    queryset = Subscription.objects.all().prefetch_related('plan',
                                                           Prefetch('client',
                                                                    queryset=Client.objects.all().select_related(
                                                                        'user').only('company_name', 'user__email'))
                                                            )
    serializer_class = SubscriptionSerializer

    def list(self, request, *args, **kwargs):
        # queryset = self.filter_queryset(self.get_queryset())
        queryset = self.get_queryset()

        total_amount = cache.get(settings.PRICE_CACHE_NAME)
        if not total_amount:
            total_amount = queryset.aggregate(total=Sum('price')).get('total')
            cache.set(settings.PRICE_CACHE_NAME, total_amount, 60 * 60)

        response = super().list(request, *args, **kwargs)
        response_data = {'result': response.data, 'total_amount': total_amount}
        response.data = response_data
        return response
