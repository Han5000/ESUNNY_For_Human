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
