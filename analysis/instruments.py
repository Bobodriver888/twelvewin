# coding=utf8

"""
股票代码相关函数
"""

__author__ = 'Administrator'

import numpy as np
import tushare as ts
from sqlalchemy import and_, cast, Integer
from models import Instrument, Session


# 字符串转换为浮点
def value_2_float(value):
    if np.isnan(value):
        return None
    else:
        return float(value)

# nan转换为None
def nan_2_none(value):
    if value != value:
        return None
    else:
        return value


def get_instrument_list():
    """
    获取所有股票列表并保存到数据库
    """
    try:
        # 下载数据
        df = ts.get_stock_basics()

        # 按照代码排序
        df.sort_index(inplace=True)

        session = Session()

        codes = [item[0] for item in session.query(Instrument.code).all()]

        for index, row in df.iterrows():
            if index in codes:
                continue

            item = Instrument(index, name=row['name'], industry=nan_2_none(row['industry']), area=nan_2_none(row['area']),
                              pe=value_2_float(row['pe']), outstanding=value_2_float(row['outstanding']),
                              totals=value_2_float(row['totals']), total_assets=value_2_float(row['totalAssets']),
                              liquid_assets=value_2_float(row['liquidAssets']),
                              fixed_assets=value_2_float(row['fixedAssets']), reserved=value_2_float(row['reserved']),
                              reserved_per_share=value_2_float(row['reservedPerShare']), esp=value_2_float(row['esp']),
                              bvps=value_2_float(row['bvps']), pb=value_2_float(row['pb']),
                              time_2_market=value_2_float(row['timeToMarket']), undp=value_2_float(row['undp']),
                              perundp=value_2_float(row['perundp']), rev=value_2_float(row['rev']),
                              profit=value_2_float(row['profit']), gpr=value_2_float(row['gpr']),
                              npr=value_2_float(row['npr']), holders=value_2_float(row['holders']))

            session.add(item)

        session.commit()

        session.close()
    except Exception as e:
        print('Exception: {}'.format(repr(e)))

        # 发送异常通知
        #text.send_text("处理股票代码数据失败")

    return df


def get_all_instrument_codes():
    """
    获取所有股票的代码
    """
    session = Session()

    codes = [item[0] for item in session.query(Instrument.code).all()]

    session.close()

    return codes


def get_all_instrument_codes_before(timeToMarket):
    """
    获取所有股票的代码
    """
    session = Session()

    codes = [item[0] for item in session.query(Instrument.code).filter(
        and_(cast(Instrument.time_2_market, Integer) < timeToMarket, Instrument.time_2_market != '0',
             Instrument.time_2_market != None)).all()]

    session.close()

    return codes


if __name__ == '__main__':
    get_instrument_list()