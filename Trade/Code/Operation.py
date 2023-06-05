import arrow as ar

from Bin.Config import es_ver_code
from Code.Sarge import this_time, Sarge
from Include.Log import log


class Base:
    def __init__(self, exe_path='Bin\\Data\\App1\\Trade0822.exe'):
        # sarge
        self.path = exe_path
        sarge = Sarge(exe_path, app_id='1')
        sarge.run()
        self.exe = sarge.exe
        self.error_ = ''  # 记录登录过程中的错误
        self.success = False  # 是否已经登录
        self.result = {
            'task_name': 'login',  # 任务名
            'status': 0,  # 任务状态,0开始，-1失败，1成功
            'content': {},  # 任务内容
            'start_time': this_time(),  # 任务发启时间
            'end_time': this_time(),  # 任务结束时间
        }
        self.json_title = {
            'qry_position': ["AccountNo", "ExchangeNo", "CommodityType", "CommodityNo", "ContractNo", "StrikePrice",
                             "CallOrPutFlag", "MatchSide", "HedgeFlag", "PositionNo", "ServerFlag", "OrderNo",
                             "MatchNo", "UpperNo", "PositionPrice", "PositionQty", "PositionStreamId",
                             "CommodityCurrencyGroup", "CommodityCurrency", "CalculatePrice", "AccountInitialMargin",
                             "AccountMaintenanceMargin", "UpperInitialMargin", "UpperMaintenanceMargin",
                             "PositionProfit", "LMEPositionProfit", "OptionMarketValue", "IsHistory"],
            'qry_fund': ["AccountNo", "CurrencyGroupNo", "CurrencyNo", "TradeRate", "FutureAlg", "OptionAlg",
                         "PreBalance", "PreUnExpProfit", "PreLMEPositionProfit", "PreEquity", "PreAvailable1",
                         "PreMarketEquity", "CashInValue", "CashOutValue", "CashAdjustValue", "CashPledged",
                         "FrozenFee", "FrozenDeposit", "AccountFee", "SwapInValue", "SwapOutValue", "PremiumIncome",
                         "PremiumPay", "CloseProfit", "FrozenFund", "UnExpProfit", "ExpProfit", "PositionProfit",
                         "LmePositionProfit", "OptionMarketValue", "AccountIntialMargin",
                         "AccountMaintenanceMargin", "UpperInitalMargin", "UpperMaintenanceMargin", "Discount",
                         "Balance", "Equity", "Available", "CanDraw", "MarketEquity", "AuthMoney"],
            'qry_order': ["ExchangeNo", "CommodityType", "CommodityNo", "ContractNo", "StrikePrice", "CallOrPutFlag",
                          "ContractNo2", "StrikePrice2", "CallOrPutFlag2", "OrderType", "OrderSource", "TimeInForce",
                          "ExpireTime", "IsRiskOrder", "OrderSide", "PositionEffect", "PositionEffect2", "InquiryNo",
                          "HedgeFlag", "OrderPrice", "OrderPrice2", "StopPrice", "OrderQty", "OrderMinQty", "RefInt",
                          "RefDouble", "RefString", "MinClipSize", "MaxClipSize", "LicenseNo", "ServerFlag", "OrderNo",
                          "ClientOrderNo", "ClientID", "TacticsType", "TriggerCondition", "TriggerPriceType",
                          "AddOneIsValid", "ClientLocalIP", "ClientMac", "ClientIP", "OrderStreamID", "UpperNo",
                          "UpperChannelNo", "OrderLocalNo", "UpperStreamID", "OrderSystemNo", "OrderExchangeSystemNo",
                          "OrderParentSystemNo", "OrderInsertUserNo", "OrderInsertTime", "OrderCommandUserNo",
                          "OrderUpdateUserNo", "OrderUpdateTime", "OrderState", "OrderMatchPrice", "OrderMatchPrice2",
                          "OrderMatchQty", "OrderMatchQty2", "ErrorCode", "ErrorText", "IsBackInput", "IsDeleted",
                          "IsAddOne"],
            'qry_fill': ["ExchangeNo", "CommodityType", "CommodityNo", "ContractNo", "StrikePrice", "CallOrPutFlag",
                         "MatchSource", "MatchSide", "PositionEffect", "ServerFlag", "OrderNo", "OrderSystemNo",
                         "MatchNo", "UpperMatchNo", "ExchangeMatchNo", "MatchDateTime", "UpperMatchDateTime", "UpperNo",
                         "MatchPrice", "MatchQty", "IsDeleted", "IsAddOne", "FeeCurrencyGroup", "FeeCurrency",
                         "FeeValue", "IsManualFee", "ClosePrositionPrice"]
        }  # json的表头

    def flash(self):
        self.exe.stdin.flush()  # 登录完毕

    def init_header(self, task_name):
        self.result['task_name'] = task_name
        self.result['start_time'] = this_time()
        self.result['end_time'] = ''
        self.result['status'] = 0
        self.result['content'] = []

    def write_msg(self, *values):
        for msg in values:
            if msg:
                self.exe.stdin.write(f'{msg}\n'.encode())
            else:
                self.exe.stdin.write('0\n'.encode())
        self.flash()

    def init_ope(self, task_no):
        self.exe.stdin.write(f'{task_no}\n'.encode())
        self.flash()

    def read_result(self):
        while 1:
            self.reading_out()
            if self.result['status']:  # 任务完成
                print(f"任务{self.result['task_name']}{'' if self.result['status'] == 1 else '不'}正常完成")
                break
            if ar.now().timestamp - ar.get(self.result['start_time']).replace(
                    tzinfo=ar.now().tzinfo).timestamp >= 10:  # 任务异常结束
                print(f"任务{self.result['task_name']}超过10s，强制异常停止")
                break
        print(self.result)

    def login(self, ip='', port=123, username='', password='', auth_code=''):
        # 定义任务头
        self.init_header('login')
        # 开始执行任务
        self.write_msg(auth_code, ip, port, username, password)
        # 读取任务结果
        # self.read_result()

    def set_ver_code(self):
        # 输入二次验证验证码
        self.write_msg(es_ver_code)
        ver_code = input('请输入二次验证验证码')
        self.write_msg(ver_code)

    def insert_order(self,
                     account='C5908', exchange_no='COMEX', commodity_type='F', commodity_no='GC',
                     contract_no='2012', strike_price='', call_or_put_flag='N',
                     contract_no2='', strike_price2='', call_or_put_flag2='N',
                     order_type='1',
                     # //const TAPIOrderTypeType			TAPI_ORDER_TYPE_MARKET = '1';
                     # ////! 限价
                     # //const TAPIOrderTypeType			TAPI_ORDER_TYPE_LIMIT = '2';
                     # ////! 市价止损
                     # //const TAPIOrderTypeType			TAPI_ORDER_TYPE_STOP_MARKET = '3';
                     # ////! 限价止损
                     # //const TAPIOrderTypeType			TAPI_ORDER_TYPE_STOP_LIMIT = '4';
                     # ////! 期权行权
                     # //const TAPIOrderTypeType			TAPI_ORDER_TYPE_OPT_EXEC = '5';
                     # ////! 期权弃权
                     # //const TAPIOrderTypeType			TAPI_ORDER_TYPE_OPT_ABANDON = '6';
                     # ////! 询价
                     # //const TAPIOrderTypeType			TAPI_ORDER_TYPE_REQQUOT = '7';
                     # ////! 应价
                     # //const TAPIOrderTypeType			TAPI_ORDER_TYPE_RSPQUOT = '8';
                     # ////! 冰山单
                     # //const TAPIOrderTypeType			TAPI_ORDER_TYPE_ICEBERG = '9';
                     # ////! 影子单
                     # //const TAPIOrderTypeType			TAPI_ORDER_TYPE_GHOST = 'A';
                     # ////港交所竞价单
                     # //const TAPIOrderTypeType			TAPI_ORDER_TYPE_HKEX_AUCTION = 'B';
                     # ////互换
                     # //const TAPIOrderTypeType			TAPI_ORDER_TYPE_SWAP = 'C';
                     # ////证券锁定
                     # //const TAPIOrderTypeType			TAPI_ORDER_TYPE_LOCK = 'D';
                     # ////证券解锁
                     # //const TAPIOrderTypeType			TAPI_ORDER_TYPE_UNLOCK = 'E';
                     # ////增强限价单
                     # //const TAPIOrderTypeType			TAPI_ORDER_TYPE_ENHANCE = 'F';
                     order_source='6', time_in_force='1',  # 取消前有效
                     expire_time='', is_risk_order='N',
                     order_side='B',
                     position_effect='N', position_effect2='N', inquiry_no='', hedge_flag='N',
                     order_price='1913', order_price2='0', stop_price='0',
                     order_qty='1', order_min_qty='1', min_clip_size='0', max_clip_size='0',
                     client_id='', tactics_type='N', trigger_condition='N', trigger_price_type='N',
                     add_one_is_valid='Y'):
        '''
            //! 客户下单请求结构
            TAPISTR_20					AccountNo;						///< 客户资金帐号，必填
            TAPISTR_10					ExchangeNo;						///< 交易所编号，必填
            TAPICommodityType			CommodityType;					///< 品种类型，必填
            TAPISTR_10					CommodityNo;					///< 品种编码类型，必填
            TAPISTR_10					ContractNo;						///< 合约1，必填
            TAPISTR_10					StrikePrice;					///< 执行价格1，期权填写
            TAPICallOrPutFlagType		CallOrPutFlag;					///< 看张看跌1 默认N
            TAPISTR_10					ContractNo2;					///< 合约2，默认空
            TAPISTR_10					StrikePrice2;					///< 执行价格2，默认空
            TAPICallOrPutFlagType		CallOrPutFlag2;					///< 看张看跌2 默认N
            TAPIOrderTypeType			OrderType;						///< 委托类型 必填
            TAPIOrderSourceType			OrderSource;					///< 委托来源，默认程序单。
            TAPITimeInForceType			TimeInForce;					///< 委托有效类型,默认取消前有效
            TAPIDATETIME				ExpireTime;						///< 有效日期(GTD情况下使用)
            TAPIYNFLAG					IsRiskOrder;					///< 是否风险报单，默认非风险保单
            TAPISideType				OrderSide;						///< 买入卖出
            TAPIPositionEffectType		PositionEffect;					///< 开平标志1,默认N
            TAPIPositionEffectType		PositionEffect2;				///< 开平标志2，默认N
            TAPISTR_50					InquiryNo;						///< 询价号
            TAPIHedgeFlagType			HedgeFlag;						///< 投机保值，默认N
            TAPIREAL64					OrderPrice;						///< 委托价格1
            TAPIREAL64					OrderPrice2;					///< 委托价格2，做市商应价使用
            TAPIREAL64					StopPrice;						///< 触发价格
            TAPIUINT32					OrderQty;						///< 委托数量，必填
            TAPIUINT32					OrderMinQty;					///< 最小成交量，默认1
            TAPIUINT32					MinClipSize;					///< 冰山单最小随机量
            TAPIUINT32					MaxClipSize;					///< 冰山单最大随机量
            TAPIINT32					RefInt;							///< 整型参考值,无需输入
            TAPIREAL64					RefDouble;						///< 浮点参考值，无需输入
            TAPISTR_50					RefString;						///< 字符串参考值，无需输入
			TAPIClientIDType			ClientID;						///< 客户子账号，如果存在子账号，则自行上报子账号
            TAPITacticsTypeType			TacticsType;					///< 策略单类型，默认N
            TAPITriggerConditionType	TriggerCondition;				///< 触发条件，默认N
            TAPITriggerPriceTypeType	TriggerPriceType;				///< 触发价格类型，默认N
            TAPIYNFLAG					AddOneIsValid;					///< 是否T+1有效,默认T+1有效。

        '''
        # 不需要的都是设置为N，数字设置为-1
        self.init_ope('1')
        # 定义任务头
        self.init_header('insert_order')
        # 开始执行任务
        self.write_msg(
            account, exchange_no, commodity_type, commodity_no, contract_no, strike_price, call_or_put_flag,
            contract_no2, strike_price2, call_or_put_flag2, order_type, order_source, time_in_force,  # 取消前有效
            is_risk_order, order_side, position_effect, position_effect2, inquiry_no, hedge_flag,
            order_price, order_price2, stop_price, order_qty, order_min_qty, min_clip_size, max_clip_size, client_id,
            tactics_type, trigger_condition, trigger_price_type, add_one_is_valid
        )
        if strike_price:
            self.exe.stdin.write(f'{1}\n'.encode())
            self.exe.stdin.write(f'{strike_price}\n'.encode())
            self.flash()
        else:
            self.exe.stdin.write(f'{0}\n'.encode())
            self.flash()
        if contract_no2:
            self.exe.stdin.write(f'{1}\n'.encode())
            self.exe.stdin.write(f'{contract_no2}\n'.encode())
        else:
            self.exe.stdin.write(f'{0}\n'.encode())
            self.flash()
        if strike_price2:
            self.exe.stdin.write(f'{1}\n'.encode())
            self.exe.stdin.write(f'{strike_price2}\n'.encode())
        else:
            self.exe.stdin.write(f'{0}\n'.encode())
            self.flash()
        # 读取任务结果
        # self.read_result()

    def cancel_order(self, order_no='123456'):
        self.init_ope('2')
        # 定义任务头
        self.init_header('cancel_order')
        # 开始执行任务
        self.write_msg(order_no)
        # 读取任务结果
        # self.read_result()

    def qry_fund(self, account='123456'):
        '''
                    TAPISTR_20					AccountNo;						///< 客户资金账号
                    TAPISTR_10					CurrencyGroupNo;				///< 币种组号
                    TAPISTR_10					CurrencyNo;						///< 币种号(为空表示币种组基币资金)
                    TAPIREAL64					TradeRate;						///< 交易汇率
                    TAPIFutureAlgType			FutureAlg;                      ///< 期货算法
                    TAPIOptionAlgType			OptionAlg;                      ///< 期权算法
                    TAPIREAL64					PreBalance;						///< 上日结存
                    TAPIREAL64					PreUnExpProfit;					///< 上日未到期平盈
                    TAPIREAL64					PreLMEPositionProfit;			///< 上日LME持仓平盈
                    TAPIREAL64					PreEquity;						///< 上日权益
                    TAPIREAL64					PreAvailable1;					///< 上日可用
                    TAPIREAL64					PreMarketEquity;				///< 上日市值权益
                    TAPIREAL64					CashInValue;					///< 入金
                    TAPIREAL64					CashOutValue;					///< 出金
                    TAPIREAL64					CashAdjustValue;				///< 资金调整
                    TAPIREAL64					CashPledged;					///< 质押资金
                    TAPIREAL64					FrozenFee;						///< 冻结手续费
                    TAPIREAL64					FrozenDeposit;					///< 冻结保证金
                    TAPIREAL64					AccountFee;						///< 客户手续费包含交割手续费
                    TAPIREAL64					SwapInValue;					///< 汇入资金
                    TAPIREAL64					SwapOutValue;					///< 汇出资金
                    TAPIREAL64					PremiumIncome;					///< 权利金收取
                    TAPIREAL64					PremiumPay;						///< 权利金支付
                    TAPIREAL64					CloseProfit;					///< 平仓盈亏
                    TAPIREAL64					FrozenFund;						///< 冻结资金
                    TAPIREAL64					UnExpProfit;					///< 未到期平盈
                    TAPIREAL64					ExpProfit;						///< 到期平仓盈亏
                    TAPIREAL64					PositionProfit;					///< 不含LME持仓盈亏
                    TAPIREAL64					LmePositionProfit;				///< LME持仓盈亏
                    TAPIREAL64					OptionMarketValue;				///< 期权市值
                    TAPIREAL64					AccountIntialMargin;			///< 客户初始保证金
                    TAPIREAL64					AccountMaintenanceMargin;		///< 客户维持保证金
                    TAPIREAL64					UpperInitalMargin;				///< 上手初始保证金
                    TAPIREAL64					UpperMaintenanceMargin;			///< 上手维持保证金
                    TAPIREAL64					Discount;						///< LME贴现
                    TAPIREAL64					Balance;						///< 当日结存
                    TAPIREAL64					Equity;							///< 当日权益
                    TAPIREAL64					Available;						///< 当日可用
                    TAPIREAL64					CanDraw;						///< 可提取
                    TAPIREAL64					MarketEquity;					///< 账户市值
                    TAPIREAL64					AuthMoney;                      ///< 授信资金
        '''

        self.init_ope('3')
        # 定义任务头
        self.init_header('qry_fund')
        # 开始执行任务
        self.write_msg(account)
        # 读取任务结果
        # self.read_result()

    def qry_position(self, account='123456'):
        '''
            TAPISTR_20					AccountNo;						///< 客户资金帐号
        	TAPISTR_10					ExchangeNo;						///< 交易所编号
        	TAPICommodityType			CommodityType;					///< 品种类型
        	TAPISTR_10					CommodityNo;					///< 品种编码类型
        	TAPISTR_10					ContractNo;						///< 合约1
        	TAPISTR_10					StrikePrice;					///< 执行价格
        	TAPICallOrPutFlagType		CallOrPutFlag;					///< 看张看跌
        	TAPISideType				MatchSide;						///< 买入卖出
        	TAPIHedgeFlagType			HedgeFlag;						///< 投机保值
        	TAPISTR_70					PositionNo;						///< 本地持仓号，服务器编写
        	TAPICHAR					ServerFlag;						///< 服务器标识
        	TAPISTR_20					OrderNo;						///< 委托编码
        	TAPISTR_20					MatchNo;						///< 本地成交号
        	TAPISTR_10					UpperNo;						///< 上手号
        	TAPIREAL64					PositionPrice;					///< 持仓价
        	TAPIUINT32					PositionQty;					///< 持仓量
        	TAPIUINT32                  PositionStreamId;				///< 持仓流号
        	TAPISTR_10					CommodityCurrencyGroup;			///< 品种币种组
        	TAPISTR_10					CommodityCurrency;				///< 品种币种
        	TAPIREAL64					CalculatePrice;					///< 当前计算价格
        	TAPIREAL64					AccountInitialMargin;			///< 客户初始保证金
        	TAPIREAL64					AccountMaintenanceMargin;		///< 客户维持保证金
        	TAPIREAL64					UpperInitialMargin;				///< 上手初始保证金
        	TAPIREAL64					UpperMaintenanceMargin;			///< 上手维持保证金
        	TAPIREAL64					PositionProfit;					///< 持仓盈亏
        	TAPIREAL64					LMEPositionProfit;				///< LME持仓盈亏
        	TAPIREAL64					OptionMarketValue;				///< 期权市值
        	TAPIYNFLAG					IsHistory;						///< 是否为昨仓
        '''
        self.init_ope('4')
        # 定义任务头
        self.init_header('qry_position')
        # 开始执行任务
        self.write_msg(account)
        # 读取任务结果
        # self.read_result()

    def modify(self, order_no='OA202008260000000057', account='C5908', exchange_no='COMEX', commodity_type='F',
               commodity_no='GC',
               contract_no='2012', strike_price='', call_or_put_flag='N', contract_no2='', strike_price2='',
               call_or_put_flag2='N', order_type='1', order_source='6', time_in_force='1',  # 取消前有效
               expire_time='', is_risk_order='N', order_side='B', position_effect='N', position_effect2='N',
               inquiry_no='', hedge_flag='N', order_price='1913', order_price2='0', stop_price='0', order_qty='1',
               order_min_qty='1',
               min_clip_size='0', max_clip_size='0', client_id='', tactics_type='N', trigger_condition='N',
               trigger_price_type='N', add_one_is_valid='Y'):
        self.init_ope('5')
        # 定义任务头
        self.init_header('modify')
        # 开始执行任务
        self.write_msg(order_no)
        self.write_msg(
            account, exchange_no, commodity_type, commodity_no, contract_no, strike_price, call_or_put_flag,
            contract_no2, strike_price2, call_or_put_flag2, order_type, order_source, time_in_force,  # 取消前有效
            is_risk_order, order_side, position_effect, position_effect2, inquiry_no, hedge_flag,
            order_price, order_price2, stop_price, order_qty, order_min_qty, min_clip_size, max_clip_size, client_id,
            tactics_type, trigger_condition, trigger_price_type, add_one_is_valid
        )
        if strike_price:
            self.exe.stdin.write(f'{1}\n'.encode())
            self.exe.stdin.write(f'{strike_price}\n'.encode())
            self.flash()
        else:
            self.exe.stdin.write(f'{0}\n'.encode())
            self.flash()
        if contract_no2:
            self.exe.stdin.write(f'{1}\n'.encode())
            self.exe.stdin.write(f'{contract_no2}\n'.encode())
        else:
            self.exe.stdin.write(f'{0}\n'.encode())
            self.flash()
        if strike_price2:
            self.exe.stdin.write(f'{1}\n'.encode())
            self.exe.stdin.write(f'{strike_price2}\n'.encode())
        else:
            self.exe.stdin.write(f'{0}\n'.encode())
            self.flash()
        # 读取任务结果
        # self.read_result()

    @property
    def should_loop(self):
        return (not self.error_) and (self.exe.poll() is None)

    # 获取输出
    def reading_out(self):
        lines = self.exe.stdout.readlines(block=not self.success)  # 读入flush_time_of_out s以内所有的数据
        for line in lines:
            self.thread_out(line)

    def thread_out(self, line):  # 并行处理返回的信息
        # 查看是否成功
        line = line.decode('gbk').replace('\r\n', '').strip()  # 清除回车键
        if line:  # 有内容
            print(line)
            task_name = self.result["task_name"]
            if not self.result['status'] and f'OnRsp_{task_name}' in line:  # 开始一个新的任务
                # 构建json
                content = line.split('\t')[1:]
                content = {i: j for i, j in zip(self.json_title[task_name], content)}
                self.result['content'].append(content)
                pass

            if f'{task_name} Finished' in line or f'{task_name} Error' in line:
                self.result['status'] = -1 if 'Error' in line else 1
                self.result['end_time'] = this_time()
                log(line)

    def kill(self, info='Kill'):
        log(info)  # 记录关闭信息
        self.exe.kill()  # 关闭api
        while self.exe.poll() is None:
            self.exe.kill()

    def restart(self):
        pass


class Trade(Base):
    detail = []

    def read_result(self):
        pre_line = ''
        while 1:
            line = self.exe.stdout.readline(block=not self.success)  # 读入flush_time_of_out s以内所有的数据
            line = line.decode('gbk').replace('\r\n', '').strip()  # 清除回车键
            if line:
                if line != pre_line:
                    pre_line = line
                else:
                    continue
                print(line)
                self.detail.append(line)
                task_name = self.result["task_name"]
                if not self.result['status'] and f'OnRsp_{task_name}' in line:  # 开始一个新的任务
                    # 构建json
                    content = line.split('\t')[1:]
                    content = {i: j for i, j in zip(self.json_title[task_name], content)}
                    self.result['content'].append(content)
                    pass

                if f'{task_name} Finished' in line or f'{task_name} Error' in line:
                    self.result['status'] = -1 if 'Error' in line else 1
                    self.result['end_time'] = this_time()
                    log(line)

    def qry_fill(self, account='C5908'):
        # 字段返回
        '''
        TAPISTR_20					AccountNo;						///< 客户资金帐号

            TAPISTR_10					ExchangeNo;						///< 交易所编号
            TAPICommodityType			CommodityType;					///< 品种类型
            TAPISTR_10					CommodityNo;					///< 品种编码类型
            TAPISTR_10					ContractNo;						///< 合约1
            TAPISTR_10					StrikePrice;					///< 执行价格
            TAPICallOrPutFlagType		CallOrPutFlag;					///< 看张看跌

            TAPIMatchSourceType			MatchSource;					///< 委托来源
            TAPISideType				MatchSide;						///< 买入卖出
            TAPIPositionEffectType              PositionEffect;					///< 开平标志1

            TAPICHAR					ServerFlag;						///< 服务器标识
            TAPISTR_20					OrderNo;						///< 委托编码
            TAPISTR_50					OrderSystemNo;					///< 系统号

            TAPISTR_20					MatchNo;						///< 本地成交号
            TAPISTR_70					UpperMatchNo;					///< 上手成交号
            TAPISTR_70					ExchangeMatchNo;				///< 交易所成交号

            TAPIDATETIME				MatchDateTime;					///< 成交时间
            TAPIDATETIME				UpperMatchDateTime;				///< 上手成交时间

            TAPISTR_10					UpperNo;						///< 上手号

            TAPIREAL64					MatchPrice;						///< 成交价
            TAPIUINT32					MatchQty;						///< 成交量

            TAPIYNFLAG					IsDeleted;						///< 委托成交删除标
            TAPIYNFLAG					IsAddOne;						///< 是否为T+1单

            TAPISTR_10					FeeCurrencyGroup;				///< 客户手续费币种组
            TAPISTR_10					FeeCurrency;					///< 客户手续费币种
            TAPIREAL64					FeeValue;						///< 手续费
            TAPIYNFLAG					IsManualFee;					///< 人工客户手续费标记

            TAPIREAL64					ClosePrositionPrice;					///< 指定价格平仓
        :param account:
        :return:
        '''
        self.init_ope('7')
        # 定义任务头
        self.init_header('qry_fill')
        # 开始执行任务
        self.write_msg(account)

    def qry_order(self, account='C5908'):
        # 返回字段
        '''
        TAPISTR_20					AccountNo;						///< 客户资金帐号

            TAPISTR_10					ExchangeNo;						///< 交易所编号
            TAPICommodityType			CommodityType;					///< 品种类型
            TAPISTR_10					CommodityNo;					///< 品种编码类型
            TAPISTR_10					ContractNo;						///< 合约1
            TAPISTR_10					StrikePrice;					///< 执行价格1
            TAPICallOrPutFlagType		CallOrPutFlag;					///< 看张看跌1
            TAPISTR_10					ContractNo2;					///< 合约2
            TAPISTR_10					StrikePrice2;					///< 执行价格2
            TAPICallOrPutFlagType		CallOrPutFlag2;					///< 看张看跌2

            TAPIOrderTypeType			OrderType;						///< 委托类型
            TAPIOrderSourceType			OrderSource;					///< 委托来源
            TAPITimeInForceType			TimeInForce;					///< 委托有效类型
            TAPIDATETIME				ExpireTime;						///< 有效日期(GTD情况下使用)

            TAPIYNFLAG					IsRiskOrder;					///< 是否风险报单
            TAPISideType				OrderSide;						///< 买入卖出
            TAPIPositionEffectType		PositionEffect;					///< 开平标志1
            TAPIPositionEffectType		PositionEffect2;				///< 开平标志2
            TAPISTR_50					InquiryNo;						///< 询价号
            TAPIHedgeFlagType			HedgeFlag;						///< 投机保值
            TAPIREAL64					OrderPrice;						///< 委托价格1
            TAPIREAL64					OrderPrice2;					///< 委托价格2，做市商应价使用
            TAPIREAL64					StopPrice;						///< 触发价格
            TAPIUINT32					OrderQty;						///< 委托数量
            TAPIUINT32					OrderMinQty;					///< 最小成交量

            TAPIINT32					RefInt;							///< 整型参考值
            TAPIREAL64					RefDouble;						///< 浮点参考值
            TAPISTR_50					RefString;						///< 字符串参考值

            TAPIUINT32					MinClipSize;					///< 冰山单最小随机量
            TAPIUINT32					MaxClipSize;					///< 冰山单最大随机量
            TAPISTR_50					LicenseNo;						///< 软件授权号



            TAPICHAR					ServerFlag;						///< 服务器标识
            TAPISTR_20					OrderNo;						///< 委托编码
            TAPISTR_50                  ClientOrderNo;					///< 客户端本地委托编号
			TAPIClientIDType            ClientID;						///< 客户子账号.
            TAPITacticsTypeType			TacticsType;					///< 策略单类型
            TAPITriggerConditionType	TriggerCondition;				///< 触发条件
            TAPITriggerPriceTypeType	TriggerPriceType;				///< 触发价格类型
            TAPIYNFLAG					AddOneIsValid;					///< 是否T+1有效

            TAPISTR_40					ClientLocalIP;					///< 终端本地IP
            TAPIMACTYPE					ClientMac;						///< 终端本地Mac地址
            TAPISTR_40					ClientIP;						///< 终端网络地址.

            TAPIUINT32					OrderStreamID;					///< 委托流水号
            TAPISTR_10					UpperNo;						///< 上手号
            TAPISTR_10					UpperChannelNo;					///< 上手通道号

            TAPISTR_20					OrderLocalNo;					///< 本地号
            TAPIUINT32					UpperStreamID;					///< 上手流号

            TAPISTR_50					OrderSystemNo;					///< 系统号
            TAPISTR_50					OrderExchangeSystemNo;			///< 交易所系统号
            TAPISTR_50					OrderParentSystemNo;			///< 父单系统号

            TAPISTR_20					OrderInsertUserNo;				///< 下单人
            TAPIDATETIME				OrderInsertTime;				///< 下单时间
            TAPISTR_20					OrderCommandUserNo;				///< 录单操作人
            TAPISTR_20					OrderUpdateUserNo;				///< 委托更新人
            TAPIDATETIME				OrderUpdateTime;				///< 委托更新时间

            TAPIOrderStateType			OrderState;						///< 委托状态

            TAPIREAL64					OrderMatchPrice;				///< 成交价1
            TAPIREAL64					OrderMatchPrice2;				///< 成交价2
            TAPIUINT32					OrderMatchQty;					///< 成交量1
            TAPIUINT32					OrderMatchQty2;					///< 成交量2

            TAPIUINT32					ErrorCode;						///< 最后一次操作错误信息码
            TAPISTR_50					ErrorText;						///< 错误信息

            TAPIYNFLAG					IsBackInput;					///< 是否为录入委托单
            TAPIYNFLAG					IsDeleted;						///< 委托成交删除标
            TAPIYNFLAG					IsAddOne;						///< 是否为T+1单
        :param account:
        :return:
        '''
        self.init_ope('8')
        # 定义任务头
        self.init_header('qry_order')
        # 开始执行任务
        self.write_msg(account)


class Example(Trade):
    insert_success = False  # 下单的参数，刘先生，这是一个示例，您按照您的思路，用最优雅的形式展现

    def read_result(self):
        pre_line = ''
        while 1:
            line = self.exe.stdout.readline(block=not self.success)  # 读入flush_time_of_out s以内所有的数据
            line = line.decode('gbk').replace('\r\n', '').strip()  # 清除回车键
            if line:
                if line != pre_line:
                    pre_line = line
                else:
                    continue
                print(line)
                self.detail.append(line)
                task_name = self.result["task_name"]
                if not self.result['status'] and f'OnRsp_{task_name}' in line:  # 开始一个新的任务
                    # 构建json
                    content = line.split('\t')[1:]
                    content = {i: j for i, j in zip(self.json_title[task_name], content)}
                    self.result['content'].append(content)
                    pass
                # 二次验证
                if '输入二次验证手机号或者邮箱' in line:
                    self.set_ver_code()
                if f'{task_name} Finished' in line or f'{task_name} Error' in line:
                    self.result['status'] = -1 if 'Error' in line else 1
                    self.result['end_time'] = this_time()
                    log(line)
                if '报单成功' in line:
                    self.insert_success = True
