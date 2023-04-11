# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from store.models import Product, Configuration, Feature, Promotion, Errors
from scraper.ProcessData import ConfigFixed
from django.db.models import Q
from django.db import IntegrityError

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
        product_created = ''
        
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
            for key, value in ConfigFixed(item['ConfigDetail']).items():
                Configuration.objects.create(
                    #ProdID = item['ProductID'],
                    ProdID = product,
                    ConfigName = key,
                    Detail = value
                )
        
            Promotion.objects.create(
                #ProdID = item['ProductID'],
                ProdID = product,
                Detail = item['PromotionDetail']
            )
        else:
            if item['ProductName'] != '':
                #print("hello")
                product = Product.objects.filter(ProductLink = item["ProductLink"])
                product.update(SalePrice = item["SalePrice"])
                product.update(NormalPrice = item["NormalPrice"])
            else:
                temp = Product.objects.filter(ProductLink = __product["ProductLink"])
                Feature.objects.create(
                    #ProdID = temp.get('ProductID'),
                    ProdID = temp,
                    Detail = item['FeatureDetail']
                )

        return item
    
    def close_spider(self, spider):
        logging.warning("Items recorded to database by pipeline")