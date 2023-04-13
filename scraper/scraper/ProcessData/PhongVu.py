# -*- coding: utf-8 -*- 
import re

ConfigPattern = ["CPU", "RAM", "Lưu trữ", "Màn hình", "Hệ điều hành", "Đồ hoạ", "Pin", "Khối lượng"]
def PVConfigFixed(data):
    dict = {}
    if len(data) != 0:
        for item in data:
            for i in ConfigPattern:
                if re.search(i,item):
                    if i == 'Lưu trữ' and item.endswith('/ '):
                        item = item.replace('/ ','')
                    elif item == "- Pin liền":
                        item = item.replace(" liền",": ")
                    elif item.endswith(" Pin liền"):
                        item = item.replace(" Pin liền","")
                        item = item.replace("- ","Pin: ")
                    elif item.endswith(" Pin rời"):
                        item = item.replace(" Pin rời","")
                        item = item.replace("- ","Pin: ")
                    dict[i] = item.split(': ')[1].rstrip()
                    if i == "Màn hình":
                        dict[i] = dict[i].replace('\"','inch')
    return dict