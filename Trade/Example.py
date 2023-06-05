import threading

from Bin.Config import *
from Code.Operation import Example

if __name__ == '__main__':
    trade = Example()
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

    # 登录成功，开始策略
    # 下一个空单
    print('初始化')
    trade.insert_order(account='account', exchange_no='COMEX', commodity_type='F', commodity_no='GC', order_type='1',
                       contract_no='2010', order_side='B', order_qty='1')
    pre_side = 'B'
    while 1:
        # 每成交一单，就下一个相反的单子
        if trade.insert_success:
            pre_side = 'S' if pre_side == 'B' else 'B'
            trade.insert_order(account='account', exchange_no='COMEX', commodity_type='F', commodity_no='GC',
                               order_type='1',
                               contract_no='2012', order_side=pre_side, order_qty='1')
            trade.insert_success = False
            print('换方向', pre_side)

    reading_result.join()  # 阻塞线程使用
