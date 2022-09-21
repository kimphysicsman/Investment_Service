from xml.dom.minidom import NamedNodeMap
from investment.serializers import (
    AssetGroupModelSerializer,
    StockModelSerializer,
)

from investment.models import (
    AssetGroup as AssetGroupModel,
    Stock as StockModel
)


def create_asset_group(name):
    data = {
        "name" : name
    }

    serializer = AssetGroupModelSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return serializer.instance


def get_asset_group(name):
    try:
        ag_obj = AssetGroupModel.objects.get(name=name)
    except:
        return create_asset_group(name)
    
    return ag_obj

def create_stock(name, isin, asset_group_name):
    ag_obj = get_asset_group(asset_group_name)
    
    data = {
        "name": name,
        "isin": isin,
        "asset_group": ag_obj.id 
    }

    serializer = StockModelSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return serializer.instance


def update_stock(stock_obj, update_info):

    serializer = StockModelSerializer(stock_obj, data=update_info)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return serializer.instance


def set_stock(name, isin, asset_group_name):
    print("run - set_stcok")

    try:
        stock_obj = StockModel.objects.get(isin=isin)
    except:
        create_stock(name, isin, asset_group_name)

    if name != stock_obj.name or asset_group_name != stock_obj.asset_group.name:
            update_info = {
                "name": name,
                "asset_group": get_asset_group(asset_group_name).id
            }
            update_stock(stock_obj, update_info)