from django.urls import path
from .views import ProductList
#ProductDetail #LaptopList, PhoneList

app_name = 'store_api'

urlpatterns = [
    #path('get-all-products/<str:pk>', ProductList.as_view(), name = 'listcreate'),
    #path('products/<str:pk>/', ProductDetail.as_view(), name = 'detailcreate')
    path('products/', ProductList.as_view(), name = "ProductList")
    # path('get-phone', PhoneList.as_view(), name='listcreate'),
    # path('get-laptop', LaptopList.as_view(), name='listcreate'),
]