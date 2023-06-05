lines = '''
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
# 为OnRS服务，对应qry
res = ''
lines = lines.replace('///<', '').replace(';', '').replace('\t', ' ')
for line in lines.split('\n'):
    line = line.strip()
    line = [i.strip() for i in line.split(' ') if i.strip()]
    if line:
        if res:
            res += fr"<<'\t'<<info->{line[1]}"
        else:
            res = f'cout<<info->{line[1]}'
res += '<<endl;'
print(res)
# 为python构建解析OnRS的json服务
res = ''
lines = lines.replace('///<', '').replace(';', '').replace('\t', ' ')
for line in lines.split('\n'):
    line = line.strip()
    line = [i.strip() for i in line.split(' ') if i.strip()]
    if line:
        if res:
            res += f'"{line[1]}",'
        else:
            res = "["
res += ']'
print(res)
# 将rtn的输出做成json格式
res = ''
lines = lines.replace('///<', '').replace(';', '').replace('\t', ' ')
for line in lines.split('\n'):
    line = line.strip()
    line = [i.strip() for i in line.split(' ') if i.strip()]
    if line:
        if res:
            res += fr"<<'\t'" + f'"{line[1]}:"<<info->{line[1]}'
        else:
            res = f'cout<<"{line[1]}:"<<info->{line[1]}'
res += '<<endl;'
print(res)

# lines = 'AccountNo >> ExchangeNo >> CommodityType >> CommodityNo >> ContractNo >> StrikePrice >> CallOrPutFlag >> ContractNo2 >> StrikePrice2 >> CallOrPutFlag2 >> OrderType >> OrderSource >> TimeInForce >> ExpireTime >> IsRiskOrder >> OrderSide >> PositionEffect >> PositionEffect2 >> InquiryNo >> HedgeFlag >> OrderPrice >> OrderPrice2 >> StopPrice >> OrderQty >> OrderMinQty >> MinClipSize >> MaxClipSize >> ClientID >> TacticsType >> TriggerCondition >> TriggerPriceType >> AddOneIsValid'
# for line in lines.split('>>'):
#     line = line.strip()
#     print(f'strcpy_s(stNewOrder.{line}, {line});')
#
# lines = '''
# 	strcpy_s(stNewOrder.OrderSide, OrderSide);
# 	strcpy_s(stNewOrder.PositionEffect, PositionEffect);
# 	strcpy_s(stNewOrder.PositionEffect2, PositionEffect2);
# 	strcpy_s(stNewOrder.HedgeFlag, HedgeFlag);
# 	strcpy_s(stNewOrder.OrderPrice, OrderPrice);
# 	strcpy_s(stNewOrder.OrderPrice2, OrderPrice2);
# 	strcpy_s(stNewOrder.StopPrice, StopPrice);
# 	strcpy_s(stNewOrder.OrderQty, OrderQty);
# 	strcpy_s(stNewOrder.OrderMinQty, OrderMinQty);
# 	strcpy_s(stNewOrder.MinClipSize, MinClipSize);
# 	strcpy_s(stNewOrder.MaxClipSize, MaxClipSize);
# 	strcpy_s(stNewOrder.TacticsType, TacticsType);
# 	strcpy_s(stNewOrder.TriggerCondition, TriggerCondition);
# 	strcpy_s(stNewOrder.TriggerPriceType, TriggerPriceType);
# 	strcpy_s(stNewOrder.AddOneIsValid, AddOneIsValid);
# '''
# for line in lines.split('\n'):
#     line = line.strip()
#     if line:
#         line = line.replace('strcpy_s(', '').replace(')', '').replace(',', '=')
#         print(line)

# 参数
lines = '''
account='account', exchange_no='COMEX', commodity_type='F', commodity_no='GC',
                     contract_no='2012', strike_price='', call_or_put_flag='N',
                     contract_no2='', strike_price2='', call_or_put_flag2='N',
                     order_type='1',
                     order_source='6', time_in_force='1',  # 取消前有效
                     expire_time='', is_risk_order='N',
                     order_side='B',
                     position_effect='N', position_effect2='N', inquiry_no='', hedge_flag='N',
                     order_price='1913', order_price2='0', stop_price='0',
                     order_qty='1', order_min_qty='1', min_clip_size='0', max_clip_size='0',
                     client_id='', tactics_type='N', trigger_condition='N', trigger_price_type='N',
                     add_one_is_valid='Y'
                     '''
res = []
for line in lines.split(','):
    line = line.split('=')[0].strip()
    res.append(line)

print(','.join(res))
