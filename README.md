ESunnyAPI是一款基于的易盛信息官方封装开源库。
如果你在开发易盛信息程序的时候遇到了奇奇怪怪的问题，请使用Quote.exe，其中打包了详尽的错误处理，可以快速定位问题。

Windows、Linux都可以使用哦！！

不限语言哦！！！

# 免费获取外盘行情

可以从demo中获取部分行情，如果想获取所有行情，欢迎沟通sino5000@outlook.com
----------------------------------------------------------------------------

10s内上手EsunnyAPI2.0？

实例在Quote.py
--------------------
- **三行代码搞定登录与订阅**
```
api = BaseAPI(quote_callback)
auth = 'B112F916FE7D27BCE7B97EB620206457946CED32E26C1EAC946CED32E26C1EAC946CED32E26C1EAC946CED32E26C1EAC5211AF9FEE541DDE9D6F622F72E25D5DEF7F47AA93A738EF5A51B81D8526AB6A9D19E65B41F59D6A946CED32E26C1EACCAF8D4C61E28E2B1ABD9B8F170E14F8847D3EA0BF4E191F5DCB1B791E63DC196D1576DEAF5EC563CA3E560313C0C3411B45076795F550EB050A62C4F74D5892D2D14892E812723FAC858DEBD8D4AF9410729FB849D5D8D6EA48A1B8DC67E037381A279CE9426070929D5DA085659772E24A6F5EA52CF92A4D403F9E46083F27B19A88AD99812DADA44100324759F9FD1964EBD4F2F0FB50B51CD31C0B02BB437'
api.login(auth=auth, ip='61.163.243.173', port=7171, username='ES', password='123456')
api.subscribe(0, 'COMEX', 'F', 'GC', '2106')  # 可以订阅多个
```
--------------------
- **自定义行情接受、处理函数**
```
@on_msg
def quote_callback(msg, timestamp, name, func_name):
    # 展现所有的回调信息
    # msg，信息主体;timestamp，行情的北京时间，name，交易所+商品+合约;func_name回调函数名字，可以是行情回调，也可以是查询回调
    print(msg, timestamp, name, func_name)
```
--------------------
- **完整代码**
```
import time

from Code.PyES import BaseAPI, on_msg


@on_msg
def quote_callback(msg, timestamp, name, func_name):
    # 展现所有的回调信息
    # msg，信息主体;timestamp，行情的北京时间，name，交易所+商品+合约;func_name回调函数名字，可以是行情回调，也可以是查询回调
    print(msg, timestamp, name, func_name)


def test_api():
    # 登录并订阅
    api = BaseAPI(quote_callback)
    auth = 'B112F916FE7D27BCE7B97EB620206457946CED32E26C1EAC946CED32E26C1EAC946CED32E26C1EAC946CED32E26C1EAC5211AF9FEE541DDE9D6F622F72E25D5DEF7F47AA93A738EF5A51B81D8526AB6A9D19E65B41F59D6A946CED32E26C1EACCAF8D4C61E28E2B1ABD9B8F170E14F8847D3EA0BF4E191F5DCB1B791E63DC196D1576DEAF5EC563CA3E560313C0C3411B45076795F550EB050A62C4F74D5892D2D14892E812723FAC858DEBD8D4AF9410729FB849D5D8D6EA48A1B8DC67E037381A279CE9426070929D5DA085659772E24A6F5EA52CF92A4D403F9E46083F27B19A88AD99812DADA44100324759F9FD1964EBD4F2F0FB50B51CD31C0B02BB437'
    api.login(auth=auth,
              ip='61.163.243.173',
              port=7171,
              username='ES',
              password='123456')
    # 订阅行情
    api.subscribe(exchange_no='COMEX', commodity_type='F', commodity_no='GC', contact_no1='2108')
    api.subscribe(exchange_no='COMEX', commodity_type='F', commodity_no='GC', contact_no1='2110')

    # 查询交易合约
    # time.sleep(2) # 如果登录之后立马查询，需要等待2s
    # api.qry_commodity()
    # api.qry_contract(exchange_no='COMEX', commodity_type='F', commodity_no='SI')

    # 检测是否断线
    time.sleep(10)
    while api.qry_status() == 1:
        time.sleep(5)
    api.disconnect()  # 销毁api


if __name__ == '__main__':
    test_api()

```
--------------------
# 运行
  - 慵懒版:直接运行Quote.exe（Windows系统）或者Quote（linux系统）
  - 勤劳版:运行Quote.py（不限系统）

安装第三方库
--------------------

    pip install -r requirements.txt(使用python3.7)
    或者
    conda env create -f environment.yml



--------------------
    行情字段如下
        ExchangeNo
        CommodityNo
        Contract.ContractNo1
        DateTimeStamp
        QPreClosingPrice
        QPreSettlePrice
        QPrePositionQty
        QOpeningPrice
        QLastPrice
        QHighPrice
        QLowPrice
        QHisHighPrice
        QHisLowPrice
        QLimitUpPrice
        QLimitDownPrice
        QTotalQty
        QTotalTurnover
        QPositionQty
        QAveragePrice
        QClosingPrice
        QSettlePrice
        QLastQty
        QImpliedBidPrice
        QImpliedBidQty
        QImpliedAskPrice
        QImpliedAskQty
        QPreDelta
        QCurrDelta
        QInsideQty
        QOutsideQty
        QTurnoverRate
        Q5DAvgQty
        QPERatio
        QTotalValue
        QNegotiableValue
        QPositionTrend
        QChangeSpeed
        QChangeRate
        QChangeValue
        QSwing
        QTotalBidQty
        QTotalAskQty
        QBidPrice、QBidQty、QAskPrice、 QAskQty共计20档

字段释义如下

      //! 行情全文
      - struct TapAPIQuoteWhole
      - {
      	TapAPIContract				Contract;						///< 合约
      	TAPISTR_10					CurrencyNo;						///< 币种编号
      	TAPICHAR					TradingState;					///< 交易状态。1,集合竞价;2,集合竞价撮合;3,连续交易;4,交易暂停;5,闭市
      	TAPIDTSTAMP					DateTimeStamp;					///< 时间戳
      	TAPIQPRICE					QPreClosingPrice;				///< 昨收盘价
      	TAPIQPRICE					QPreSettlePrice;				///< 昨结算价
      	TAPIQVOLUME					QPrePositionQty;				///< 昨持仓量
      	TAPIQPRICE					QOpeningPrice;					///< 开盘价
      	TAPIQPRICE					QLastPrice;						///< 最新价
      	TAPIQPRICE					QHighPrice;						///< 最高价
      	TAPIQPRICE					QLowPrice;						///< 最低价
      	TAPIQPRICE					QHisHighPrice;					///< 历史最高价
      	TAPIQPRICE					QHisLowPrice;					///< 历史最低价
      	TAPIQPRICE					QLimitUpPrice;					///< 涨停价
      	TAPIQPRICE					QLimitDownPrice;				///< 跌停价
      	TAPIQVOLUME					QTotalQty;						///< 当日总成交量
      	TAPIQPRICE					QTotalTurnover;					///< 当日成交金额
      	TAPIQVOLUME					QPositionQty;					///< 持仓量
      	TAPIQPRICE					QAveragePrice;					///< 均价
      	TAPIQPRICE					QClosingPrice;					///< 收盘价
      	TAPIQPRICE					QSettlePrice;					///< 结算价
      	TAPIQVOLUME					QLastQty;						///< 最新成交量
      	TAPIQPRICE					QBidPrice[20];					///< 买价1-20档
      	TAPIQVOLUME					QBidQty[20];					///< 买量1-20档
      	TAPIQPRICE					QAskPrice[20];					///< 卖价1-20档
      	TAPIQVOLUME					QAskQty[20];					///< 卖量1-20档
      	TAPIQPRICE					QImpliedBidPrice;				///< 隐含买价
      	TAPIQVOLUME					QImpliedBidQty;					///< 隐含买量
      	TAPIQPRICE					QImpliedAskPrice;				///< 隐含卖价
      	TAPIQVOLUME					QImpliedAskQty;					///< 隐含卖量
      	TAPIQPRICE					QPreDelta;						///< 昨虚实度
      	TAPIQPRICE					QCurrDelta;						///< 今虚实度
      	TAPIQVOLUME					QInsideQty;						///< 内盘量
      	TAPIQVOLUME					QOutsideQty;					///< 外盘量
      	TAPIQPRICE					QTurnoverRate;					///< 换手率
      	TAPIQVOLUME					Q5DAvgQty;						///< 五日均量
      	TAPIQPRICE					QPERatio;						///< 市盈率
      	TAPIQPRICE					QTotalValue;					///< 总市值
      	TAPIQPRICE					QNegotiableValue;				///< 流通市值
      	TAPIQDIFF					QPositionTrend;					///< 持仓走势
      	TAPIQPRICE					QChangeSpeed;					///< 涨速
      	TAPIQPRICE					QChangeRate;					///< 涨幅
      	TAPIQPRICE					QChangeValue;					///< 涨跌值
      	TAPIQPRICE					QSwing;							///< 振幅
      	TAPIQVOLUME					QTotalBidQty;					///< 委买总量
      	TAPIQVOLUME					QTotalAskQty;					///< 委卖总量
      	TapAPIContract				UnderlyContract;				///< 虚拟合约对应的真实合约
      };
