from store.models import Product, Configuration, Feature, Promotion, Errors
from django.db.models import Q
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist


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
    
    if item['ProductID'] is not None:
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
    else:
        if item['ProductID'] is not None:
            try:
                product = Product.objects.get(ProductLink = item['ProductLink'])
                tmp = ''
                if item['SalePrice'] != '' and item['NormalPrice'] != '':
                    product.SalePrice = item['SalePrice']
                    product.NormalPrice = item['NormalPrice']
                    #product.save()
                    #print('update price', item['ProductID'])
                    tmp += item['ProductID'] + ': update price '
                if product.ProductName == '' and item['ProductName'] != '':
                    product.ProductName = item['ProductName']
                    #print('update productname')
                    tmp += 'productname '
                if product.ShopName == '' and item['ShopName'] != '':
                    product.ShopName = item['ShopName']
                    #print('update shopname')
                    tmp += 'shopname '
                if product.BrandName == '' and item['BrandName'] != '':
                    product.BrandName = item['BrandName']
                    #print('update brandname')
                    tmp += 'brandname '
                if product.ImageLink == '' and item['ImageLink'] != '':
                    product.ImageLink = item['ImageLink']
                    #print('update imagelink')
                    tmp += 'imagelink'
                if tmp != '':
                    print(tmp)
                product.save()
            except ObjectDoesNotExist:
                pass
        elif item['FeatureDetail'] is not None:
            temp = Product.objects.filter(ProductLink = item["ProductLink"])
            if len(temp):
                try:
                    feature, feature_created = Feature.objects.filter(
                        Q(ProdID = temp[0], FeatureName = item['FeatureDetail'])
                    ).get_or_create(ProdID = temp[0], FeatureName = item['FeatureDetail'])
                except IntegrityError as e:
                    Errors.objects.create(
                        ProdInfo = item['ProductLink'],
                        ErrorDetail = e
                )
                if feature:
                    print('create')
                else: print('exist')
    
    return item