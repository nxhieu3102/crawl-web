# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from store.models import Product, Configuration, Feature, Promotion, Errors
from scraper.ProcessData.PhongVu import PVConfigFixed
#from scraper.ProcessData.FPTShop import FPTConfigFixed
from django.db.models import Q
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist


import logging, coloredlogs
logger = logging.getLogger(__name__)
coloredlogs.install(level="WARN", logger=logger)

class ScraperPipeline:
    def process_item(self, item, spider):
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
            if item['ShopName'] == 'PhongVu':
                for key, value in PVConfigFixed(item['ConfigDetail']).items():
                    Configuration.objects.create(
                        ProdID = product,
                        ConfigName = key,
                        Detail = value
                    )
            else:
                for key, value in item['ConfigDetail'].items():
                    Configuration.objects.create(
                        ProdID = product,
                        ConfigName = key,
                        Detail = value
                    )
        
            Promotion.objects.create(
                ProdID = product,
                Detail = item['PromotionDetail']
            )
        else:
            if item['ProductID'] is not None:
                try:
                    product = Product.objects.get(ProductLink = item['ProductLink'])
                    product.SalePrice = item['SalePrice']
                    product.NormalPrice = item['NormalPrice']
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
        return item
    
    def close_spider(self, spider):
        logging.warning("Items recorded to database by pipeline")
