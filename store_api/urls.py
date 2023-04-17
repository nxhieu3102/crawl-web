from django.urls import path
from .views import ProductList, LaptopList, PhoneList

app_name = 'store_api'

urlpatterns = [
    path('get-all-products', ProductList.as_view(), name = 'listcreate'),
    path('get-phone', PhoneList.as_view(), name='listcreate'),
    path('get-laptop', LaptopList.as_view(), name='listcreate'),
]