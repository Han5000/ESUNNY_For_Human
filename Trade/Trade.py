import threading

from Bin.Config import *
from Code.Operation import Trade

if __name__ == '__main__':
    trade = Trade()
    # 启动回执线程
    # 这个线程自动读取回执
    # 一来读取rtn
    # 而来读取rsqry
    reading_result = threading.Thread(target=trade.read_result)
    reading_result.start()
    # 登录测试
    trade.login(ip=es_ip,
                port=es_port,
                username=es_account,
                password=es_password,
                auth_code=es_auth_code)
    while 'login Finished' not in trade.detail:  # 确定登录成功
        pass
    # 下单测试
    trade.insert_order(account='account', exchange_no='COMEX', commodity_type='F', commodity_no='GC', order_type='1',
                       contract_no='2010', order_side='B', order_qty='1')
    # trade.insert_order(account='account', exchange_no='HKEX', commodity_type='S', commodity_no='HSI', order_type='2',
    #                    contract_no='2009', contract_no2='2010', order_side='B', order_qty='1', order_price='2')
    # trade.insert_order(account='account',
    #                    exchange_no='HKEX', commodity_type='O', commodity_no='HHI', order_type='2',
    #                    contract_no='2009', order_side='B', order_qty='1', strike_price='9400', call_or_put_flag='P')
    # 改单测试
    # trade.modify(order_no='OA202008260000000057', account='account', order_price='1379')
    # 查询持仓测试
    # trade.qry_position(account='account')
    # 查询fund测试
    # trade.qry_fund(account='account')
    # 取消单子测试
    # trade.cancel_order(order_no='OA202008260000000057')
    # qry_fill测试
    # trade.qry_fill()
    # qry_order测试
    trade.qry_order()
    # 关闭程序
    # trade.kill()

    print(trade.detail)
    reading_result.join()  # 阻塞线程使用
