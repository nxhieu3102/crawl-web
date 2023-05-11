from time import sleep
from celery import shared_task

from store.crawl.fptshop import FPTShopUpdateProduct
from store.crawl.cellphones import CellPhoneSUpdateProduct
from store.crawl.phongvu import PhongVuUpdateProduct
from store.crawl.tgdd import TGDDUpdateProduct

    
@shared_task()
def fpt():
    FPTShopUpdateProduct()

@shared_task()
def tgdd():
    TGDDUpdateProduct()
    
@shared_task()
def phongvu():
    PhongVuUpdateProduct()
    
@shared_task()
def cps():
    CellPhoneSUpdateProduct()
