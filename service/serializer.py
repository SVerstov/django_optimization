from rest_framework import serializers

from service.models import Subscription, Plan


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ('__all__')


class SubscriptionSerializer(serializers.ModelSerializer):
    plan = PlanSerializer()
    price = serializers.SerializerMethodField()
    client_name = serializers.CharField(source='client.company_name')
    email = serializers.CharField(source='client.user.email')

    def get_price(self, instance): # instance будем представлять подпуску
        return instance.service.full_price * (1 - instance.plan.discount_percent/100)


    class Meta:
        model = Subscription
        fields = ('id', 'plan_id', 'client_name', 'email', 'plan', 'price')
