from store.models import Product, Configuration, Feature, Promotion, Errors
from django.db.models import Q
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

def check(data):
    return (data['ProductID'] != '' and data['ProductName'] != '' and data['SalePrice'] != '' and data['NormalPrice'] != '')

def process_item(item):
    __product = {
        'ProductID': item['ProductID'], 
        'ProductName': item['ProductName'], 
        'BrandName': item['BrandName'],
        'ShopName': item['ShopName'],
        'ImageLink': item['ImageLink'],
        'ProductLink': item['ProductLink'],
        'SalePrice': item['SalePrice'],
        'NormalPrice': item['NormalPrice'],
        'Type': item['Type']
    }
    
    product = ''
    product_created = False
    
    if item['ProductID'] is not None and check(item):
        try:
            product, product_created = Product.objects.filter(
                Q(ProductLink = item['ProductLink'])
            ).get_or_create(__product) 
        except IntegrityError as e:
            Errors.objects.create(
                ProdInfo = item['ProductLink'],
                ErrorDetail = e
            )
            
    if product_created == True:
        print('created ',item['ProductID'], ' from ', item['ShopName'])
        for key, value in item['ConfigDetail'].items():
            Configuration.objects.create(
                ProdID = product,
                ConfigName = key,
                Detail = value
            )

        if item['PromotionDetail'] is not None:
            Promotion.objects.create(
                ProdID = product,
                Detail = item['PromotionDetail']
            )
    
def feature_process(link, feature):
    temp = Product.objects.filter(ProductLink = link)
    if len(temp):
        try:
            feature, feature_created = Feature.objects.filter(
                Q(ProdID = temp[0], FeatureName = feature)
            ).get_or_create(ProdID = temp[0], FeatureName = feature)
        except IntegrityError as e:
            Errors.objects.create(
                ProdInfo = link,
                ErrorDetail = e
        )