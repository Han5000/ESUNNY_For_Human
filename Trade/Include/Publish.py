import socket

import redis
from Bin.Config import es_publish_way
from Include.Log import log
from Include.Path import Path
from pickle import dump


class Publish:
    def __init__(self):
        self.way = '0'
        self.tool = None

    def __config_tool(self):
        # self.way = Path('Bin/Config/Publish.txt').text().strip()
        self.way = es_publish_way
        if self.way == '1':  # redis
            tool = self.__get_redis()

            def send(msg):
                chanel = ''.join(msg[:3])
                tool.publish(chanel, ','.join(msg))

        elif self.way == '2':  # socket
            tool = self.__get_socket()

            def send(msg):
                tool.send(bytes(','.join(msg), encoding='gbk'))

        elif self.way == '4':  # file_json
            tail = []
            for i in range(1, 21):
                for j in ['QBidPrice', 'QBidQty', 'QAskPrice', 'QAskQty']:
                    tail.append(f'{j}{i}')
            # names = ['ExchangeNo', 'CommodityNo', 'Contract.ContractNo1', 'DateTimeStamp', 'QPreClosingPrice',
            #          'QPreSettlePrice', 'QPrePositionQty', 'QOpeningPrice', 'QLastPrice', 'QHighPrice', 'QLowPrice',
            #          'QHisHighPrice', 'QHisLowPrice', 'QLimitUpPrice', 'QLimitDownPrice', 'QTotalQty', 'QTotalTurnover',
            #          'QPositionQty', 'QAveragePrice', 'QClosingPrice', 'QSettlePrice', 'QLastQty', 'QImpliedBidPrice',
            #          'QImpliedBidQty', 'QImpliedAskPrice', 'QImpliedAskQty', 'QPreDelta', 'QCurrDelta', 'QInsideQty',
            #          'QOutsideQty', 'QTurnoverRate', 'Q5DAvgQty', 'QPERatio', 'QTotalValue', 'QNegotiableValue',
            #          'QPositionTrend', 'QChangeSpeed', 'QChangeRate', 'QChangeValue', 'QSwing', 'QTotalBidQty',
            #          'QTotalAskQty'] + tail
            # 20200709增加期权字段
            names = ['ExchangeNo', 'CommodityNo', 'CommodityType', 'ContractNo1', 'StrikePrice1',
                     'CallOrPutFlag1', 'ContractNo2', 'StrikePrice2', 'CallOrPutFlag2',
                     'DateTimeStamp', 'QPreClosingPrice', 'QPreSettlePrice', 'QPrePositionQty', 'QOpeningPrice',
                     'QLastPrice', 'QHighPrice', 'QLowPrice', 'QHisHighPrice', 'QHisLowPrice',
                     'QLimitUpPrice', 'QLimitDownPrice', 'QTotalQty', 'QTotalTurnover', 'QPositionQty',
                     'QAveragePrice', 'QClosingPrice', 'QSettlePrice', 'QLastQty', 'QImpliedBidPrice',
                     'QImpliedBidQty', 'QImpliedAskPrice', 'QImpliedAskQty', 'QPreDelta', 'QCurrDelta',
                     'QInsideQty', 'QOutsideQty', 'QTurnoverRate', 'Q5DAvgQty', 'QPERatio',
                     'QTotalValue', 'QNegotiableValue', 'QPositionTrend', 'QChangeSpeed', 'QChangeRate',
                     'QChangeValue', 'QSwing', 'QTotalBidQty', 'QTotalAskQty'] + tail

            def send(msg):
                content = {_name: _values for _name, _values in zip(names, msg)}
                with open(f"Bin\\ESData\\{''.join(msg[:9])}.lc", 'wb') as f:
                    dump(content, f)

                # name = f"Bin\\ESData\\{''.join(msg[:3])}.txt"
                # content = {_name: _values for _name, _values in zip(names, msg)}
                # Path(name).write_text(str(content).replace("'", '"'))

        else:  # 文本
            def send(msg):
                name = f"Bin\\ESData\\{''.join(msg[:3])}.txt"
                Path(name).write_text(','.join(msg))

        self.tool = send

    @staticmethod
    def __get_redis():
        redis_conf = {'socket_timeout': 3}
        for line in Path('Bin/Config/Redis.txt').lines():
            if ':' in line:
                _key, value = [j.strip() for j in line.split(':')]
                redis_conf[_key] = value if value != 'None' else None

        pool = redis.ConnectionPool(**redis_conf)
        r = redis.Redis(connection_pool=pool)
        log('start Redis->' + ','.join(redis_conf))

        return r

    @staticmethod
    def __get_socket():
        hostname, port = [i.strip() for i in Path('Bin/Config/Socket.txt').lines() if i.strip()]
        port = int(port)

        srv = socket.socket()  # 创建一个socket
        srv.bind(('', port))
        srv.listen(5)

        log(f"socket等待{hostname}:{port}的链接")

        connect_socket, addr = srv.accept()
        print('链接IP', addr)
        log(f"socket链接成功")
        return connect_socket

    def get_tool(self):
        self.__config_tool()
        return self.tool
