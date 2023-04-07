# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
import pathlib

class ProductItem(scrapy.Item):
    ProductID = scrapy.Field()
    ProductName = scrapy.Field() 
    
    BrandName = scrapy.Field() 
    ShopName = scrapy.Field() 
    
    ImageLink = scrapy.Field()
    ProductLink = scrapy.Field()
    
    SalePrice = scrapy.Field()
    NormalPrice = scrapy.Field()
    
    Type = scrapy.Field()
    

class ConfigItem(scrapy.Item):
    ProdID = scrapy.Field()
    ConfigName = scrapy.Field()
    Detail = scrapy.Field()
    

class FeatureItem(scrapy.Item):
    ProdID = scrapy.Field()
    FeatureName = scrapy.Field()
  
  
class PromotionItem(scrapy.Item):
    ProdID = scrapy.Field()
    Detail = scrapy.Field()
