from xml.dom.minidom import NamedNodeMap

from investment.serializers import (
    AssetGroupModelSerializer,
    StockModelSerializer,
    InvestmentModelSerializer,
    BankModelSerializer,
    InvestmentStockModelSerializer
)

from investment.models import (
    AssetGroup as AssetGroupModel,
    Stock as StockModel,
    Investment as InvestmentModel,
    Bank as BankModel,
    InvestmentStock as InvestmentStockModel
)


def create_asset_group(name):
    """자산그룹 생성 함수

    Args:
        name (str): 자산그룹명

    Returns:
        AssetGroupModel: 생성된 자산그룹 오브젝트
    """

    data = {
        "name" : name
    }

    serializer = AssetGroupModelSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return serializer.instance


def get_asset_group(name):
    """자산그룹명으로 자산그룹 오브젝트 반환 함수
       해당 오브젝트가 없을시 생성 후 반환

    Args:
        name (str): 자산그룹명

    Returns:
        AssetGroupModel: 해당 자산그룹 오브젝트
    """

    try:
        ag_obj = AssetGroupModel.objects.get(name=name)
    except:
        return create_asset_group(name)
    
    return ag_obj


def create_stock(isin, name, asset_group_name):
    """종목 생성 함수

    Args:
        name (str): 종목명
        isin (str): ISIN
        asset_group_name (str): 자산그룹명

    Returns:
        StockModel: 생성한 종목 오브젝트
    """

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
    """종목 업데이트 함수

    Args:
        stock_obj (StockModel): 수정할 종목 오브젝트
        update_info (dict): 수정할 정보

    Returns:
        StockModel: 수정된 종목 오브젝트
    """

    serializer = StockModelSerializer(stock_obj, data=update_info, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return serializer.instance


def set_stock(isin, name=None, asset_group_name=None):
    """종목 셋팅 함수
       ISIN을 기준으로 해당 종목이 없으면 생성
       있으면 수정 여부 확인후 수정

    Args:
        name (str): 종목명 
        isin (str): ISIN
        asset_group_name (str): 자산그룹명

    Returns:
        StockModel: 종목 오브젝트
    """

    print(isin, name, asset_group_name)
    try:
        stock_obj = StockModel.objects.get(isin=isin)
    except:
        return create_stock(isin, name, asset_group_name)

    if bool(name and name != stock_obj.name) or bool(asset_group_name and asset_group_name != stock_obj.asset_group.name):
        update_info = {
            "name": name,
            "asset_group": get_asset_group(asset_group_name).id
        }
        return update_stock(stock_obj, update_info)
    
    return stock_obj


def create_bank(name):
    data = {
        "name": name
    }
    
    serializer = BankModelSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return serializer.instance


def get_bank(name):
    try:
        bank_obj = BankModel.objects.get(name=name)
    except:
        return create_bank(name)
    
    return bank_obj


def create_investment(user_obj, account_name, account_num, bank_name):
    bank_obj = get_bank(bank_name)

    data = {
        "user": user_obj.id,
        "bank": bank_obj.id,
        "account_name": account_name,
        "account_num": str(account_num)
    }

    serializer = InvestmentModelSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return serializer.instance


def get_investment(user_obj, account_name, account_num, bank_name):
    try:
        investment_obj = InvestmentModel.objects.get(account_num=account_num)
    except:
        return create_investment(user_obj, account_name, account_num, bank_name)

    if investment_obj.user != user_obj or account_name != investment_obj.account_name or bank_name != investment_obj.bank.name:
        return
    
    return investment_obj


def create_investment_stock(investment_obj, stock_obj, current_price, order):
    data = {
        "investment": investment_obj.id,
        "stock": stock_obj.id,
        "current_price": current_price,
        "order": order
    }

    serializer = InvestmentStockModelSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return serializer.instance


def update_investment_stock(investment_stock_obj, update_info):
    serializer = InvestmentStockModelSerializer(investment_stock_obj, data=update_info, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return serializer.instance


def set_investment_stock(investment_obj, stock_obj, current_price, order):
    try:
        investment_stock_obj = InvestmentStockModel.objects.get(investment=investment_obj, stock=stock_obj)
    except:
        return create_investment_stock(investment_obj, stock_obj, current_price, order)

    if current_price != investment_stock_obj.current_price or order != investment_stock_obj.order:
        update_info = {
            "current_price": current_price,
            "order": order
        }
        
        return update_investment_stock(investment_stock_obj, update_info)

    return investment_stock_obj