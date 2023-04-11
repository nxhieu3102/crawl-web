from django.db import models

# Create your models here.
class Product(models.Model):
    ProductID = models.CharField(max_length = 20, primary_key = True, blank = False) #PVLAP1
    ProductName = models.CharField(max_length = 255) #Macbook Pro M2
    
    BrandName = models.CharField(max_length = 25) #APPLE
    ShopName = models.CharField(max_length = 20) #PhongVu
    
    ImageLink = models.URLField(max_length = 255) #https://...
    ProductLink = models.URLField(max_length = 255, unique = True) #https://...
    
    SalePrice = models.CharField(max_length = 12) #31000000
    NormalPrice = models.CharField(max_length = 12) #35000000
    
    Type = models.CharField(max_length = 25) #May tinh ca nhan
    
    def __str__(self):
        return self.ProductName
    
    def isSale(self):
        return self.SalePrice < self.NormalPrice
    
class Configuration(models.Model):
    ProdID = models.ForeignKey(Product, on_delete = models.CASCADE) #PVLAP1
    ConfigName = models.CharField(max_length = 50) #ROM
    Detail = models.CharField(max_length = 100) #512GB
    
class Feature(models.Model):
    ProdID = models.ForeignKey(Product, on_delete = models.CASCADE) #PVLAP1
    FeatureName = models.CharField(max_length = 50) #Sinh viên, văn phòng

class Promotion(models.Model):
    ProdID = models.ForeignKey(Product, on_delete = models.CASCADE) #PVLAP1
    Detail = models.CharField(max_length = 255) #Khuyến mãi khi mua kèm tai nghe, điện thoại ...

#This class is used for tracking bug in database
class Errors(models.Model):
    ProdInfo = models.CharField(max_length = 255) #https://phongvu.vn/....
    ErrorDetail = models.CharField(max_length = 255) #Primary Key invalid ... 
    