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
    
    ConfigDetail = scrapy.Field()
    FeatureDetail = scrapy.Field()
    PromotionDetail = scrapy.Field()
