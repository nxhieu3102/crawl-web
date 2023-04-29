from rest_framework import serializers
from store.models import Product, Configuration, Promotion


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        #fields = ('ProductID', 'ProductName', 'BrandName', 'ShopName', 'ImageLink', 'ProductLink', 'SalePrice', 'NormalPrice', 'Type')
        model = Product
        fields = "__all__"
        
class ConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('ProdID', 'ConfigName', 'Detail',)
        model = Configuration
        
class PromotionSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('ProdID', 'Detail',)
        model = Promotion
    
class ProductDetailSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    config = ConfigurationSerializer(many = True, read_only = True)
    promo = PromotionSerializer()
    
    class Meta:
        model = Product
        fields = ('ProductID', 'ProductName', 'BrandName', 'ShopName', 'ImageLink', 'ProductLink', 'SalePrice', 'NormalPrice', 'Type', 'config', 'promo')
    
    
    # class Meta:
    #     fields = ('ProductName', 'BrandName', 'ShopName', 'ImageLink', 'ProductLink', 'SalePrice', 'NormalPrice', 'Type', 'Promotion')

        