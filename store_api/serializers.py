from rest_framework import serializers
from store.models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('ProductID', 'ProductName', 'BrandName', 'ShopName', 'ImageLink', 'ProductLink', 'SalePrice', 'NormalPrice', 'Type')
        model = Product

        