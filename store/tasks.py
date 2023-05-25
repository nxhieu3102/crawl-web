from time import sleep
from celery import shared_task

from store.crawl.fptshop import FPTShopUpdateProduct, FPTShopUpdateLink
from store.crawl.cellphones import CellPhoneSUpdateProduct, CellPhoneSUpdateLink
from store.crawl.phongvu import PhongVuUpdateProduct, PhongVuUpdateLink
from store.crawl.tgdd import TGDDUpdateProduct, TGDDUpdateLink

    
@shared_task()
def fpt():
    FPTShopUpdateProduct()
    
@shared_task()
def tgdd():
    TGDDUpdateProduct()

@shared_task()
def cellphones():
    CellPhoneSUpdateProduct()
    
@shared_task()
def phongvu():
    PhongVuUpdateProduct()
    
