
from rest_framework import serializers
from app.models import Goods, FoodType


class GoodsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Goods
        fields = ['id', 'productlongname', 'categoryid', 'price', 'marketprice']

