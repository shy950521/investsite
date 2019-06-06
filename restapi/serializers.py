from rest_framework import serializers
from . import models


# stock serializer
class StockSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'name',
            'ticker',
            'price',
        )
        model = models.Stock


# stock join invest serializer
class InvestSerializer(serializers.ModelSerializer):
    ticker = StockSerializer(many=False, read_only=True)

    class Meta:
        fields = (
            'pk',
            'ticker',
            'user',
            'time',
            'share',
        )
        model = models.Invest


# invest serializer
class InvestSerializerCreate(serializers.ModelSerializer):

    class Meta:
        fields = (
            'pk',
            'ticker',
            'user',
            'time',
            'share',
        )
        model = models.Invest


# user input serializer
class ReceiveSerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
            'user',
            'first',
            'second',
            'third',
            'fourth',
            'fifth',
            'val',
        )
        model = models.Receive
