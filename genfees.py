from dataclasses import dataclass
import demjson
from numpy import save
import pandas as pd
from ctpbee.interface.ctp.td_api import BeeTdApi #和 mycpp 冲突  BeeTdApi.close()释放不了,我只能分两步,步骤1开本行,步骤2开行6
# from mycpp import get_margin,get_commission #需要填写config.ini
from ctpbee.signals import AppSignal
from ctpbee.record import Recorder
import pandas as pd
import time as ct
from servsetting import info　# 此处直接拷个info过来用.
from mylog import MyLogger
from ctpbee.constant import Exchange
from ctpbee.config import Config
import pickle


def decode(x):
    return demjson.decode(x)

def getallfees():
    mkt_codes = {
        'SHFE': [
            'cu', 'al', 'zn', 'pb', 'au', 'ag', 'rb', 'wr', 'fu', 'bu', 'ru',
            'hc', 'ni', 'sn', 'sp', 'ss'
        ],
        'DCE': [
            'a', 'b', 'bb', 'c', 'fb', 'i', 'j', 'jd', 'jm', 'l', 'm', 'p',
            'pp', 'v', 'y', 'cs', 'eg', 'rr', 'eb', 'pg', 'lh'
        ],
        'CZCE': [
            'cf', 'fg', 'jr', 'oi', 'pm', 'ri', 'rm', 'sr', 'ta', 'sm', 'wh',
            'rs', 'ma', 'lr', 'sf', 'zc', 'cy', 'ap', 'cj', 'ur', 'sa', 'pf',
            'pk'
        ],
        'CFFEX': ['if', 'tf', 't', 'ih', 'ic', 'ts'],
        'INE': ['sc', 'nr', 'lu', 'bc']
    }

    # cat margin.txt | grep -E \"[Aa-zZ]{1,2}\" -o >product.txt
    month = "2205"

    with open("./product.txt", "r") as f:
        products = f.readlines()
        products = [x.strip("\n") for x in products]
        f.close()

    instrument = {}

    for p in products:
        for k, v in mkt_codes.items():
            if p in v:
                exchange = k
                break
            else:
                continue
        inst = decode(get_contract(p + month, exchange))
        print(f"getting contracts {p+month}.{exchange} margin \n")
        instrument.update({(p + month): inst})

    cts = [x.strip("\n") + month for x in products]

    rows = []
    for code in cts:
        print(f"geting margin {code}\n")
        margin = decode(get_margin(code))
        print(f"geting get_commission {code}\n")
        commission = decode(get_commission(code))

        longM = margin["longbyM"] + instrument[code]["longbyM"]
        shortM = margin["shortbyM"] + instrument[code]["shortbyM"]

        openV = commission["openbyV"]
        closeV = commission["closebyV"]
        closetV = commission["closetbyV"]

        openM = commission["openbyM"]
        closeM = commission["closetbyM"]
        closetM = commission["closetbyM"]

        row = [
            code, longM, shortM, openM, closeM, closetM, openV, closeV, closetV
        ]
        rows.append(row)

    data = pd.DataFrame(data=rows,
                        columns=[
                            "code", "longM", "shortM", "openM", "closeM",
                            "closetM", "openV", "closeV", "closetV"
                        ])
    data.sort_values(by="longM", ascending=True)

    # data.to_excel('margin.xlsx', sheet_name='Sheet1', index=False)
    # data.to_csv('margin.txt', sep='\t', index=False)
    # print(data)
    return data


def getfees_bycode(code):
    print(f"geting margin {code}\n")
    margin = decode(get_margin(code))
    print(f"geting get_commission {code}\n")
    commission = decode(get_commission(code))

    longM = margin["longbyM"] 
    shortM = margin["shortbyM"]

    openV = commission["openbyV"]
    closeV = commission["closebyV"]
    closetV = commission["closetbyV"]

    openM = commission["openbyM"]
    closeM = commission["closetbyM"]
    closetM = commission["closetbyM"]

    row = [code, longM, shortM, openM, closeM, closetM, openV, closeV, closetV]
    return row



@dataclass
class FeeData:
    local_symbol:str =""
    name: str=""
    longM1 : float=0 #from contract
    shortM1 :float=0
    longM2 : float=0 #from myctpdll
    shortM2 :float=0
    openM:float =0     #from myctpdll
    closeM:float =0 
    closetM:float =0 
    openV:float =0    
    closeV:float =0 
    closetV:float =0 
    pre_settle_price:float =0 
    pricetick:float =0 
    size:float =0 
    value:float =0 
    onehandL:float =0 
    onehandS:float =0 
    pertick:float =0 
    symbol: str = ""
    longM: float =0 
    shortM: float =0 
    cjcb: float =0 #冲击成本
    
    def fake__post__init(self):
        if self.value==0 and (self.pre_settle_price>0 and self.size>0):
            self.value =  self.pre_settle_price*self.size
            self.pertick = self.pricetick * self.size
        try:
            if not self.symbol:
                self.symbol = self.local_symbol.split(".")[0]
        except Exception as e:
            print(f"init symbol error {e}\n")
        
        if self.longM==0 and (self.longM1>0 and self.longM2>0):
            self.longM = self.longM1 + self.longM2
        
        if self.shortM==0 and (self.shortM1>0 and self.shortM2>0):
            self.shortM = self.shortM1 + self.shortM2
        
        if self.longM>0:
            self.onehandL = self.value * self.longM
            
        if self.shortM>0:
            self.onehandS = self.value * self.shortM
            
        if self.openM==0 and self.openV!=0:
            self.cjcb = self.pertick /(self.openV+self.closeV+self.closetV)
            
        elif self.openV==0 and self.openM!=0:
            self.cjcb = self.pertick /(self.value*(self.openM+self.closeM+self.closetM))
        
    def repost(self):
        self.fake__post__init()
    
    
    
class FakeAppForGenFees:
    default_config = dict(LOG_OUTPUT=True,  # 是否开启输出模式
                          TD_FUNC=False,  # 是否开启交易功能
                          INTERFACE="ctp",  # 接口参数，默认指定国内期货ctp
                          MD_FUNC=True,  # 是否开启行情功能
                          XMIN=[],  # k线序列周期， 支持一小时以内的k线任意生成
                          ALL_SUBSCRIBE=False,
                          SHARE_MD=False,  # 是否多账户之间共享行情，---> 等待完成
                          SLIPPAGE_COVER=0,  # 平多头滑点设置
                          SLIPPAGE_SELL=0,  # 平空头滑点设置
                          SLIPPAGE_SHORT=0,  # 卖空滑点设置
                          SLIPPAGE_BUY=0,  # 买多滑点设置
                          SHARED_FUNC=False,  # 分时图数据 --> 等待优化
                          REFRESH_INTERVAL=1.5,  # 定时刷新秒数， 需要在CtpBee实例化的时候将refresh设置为True才会生效
                          INSTRUMENT_INDEPEND=False,  # 是否开启独立行情，策略对应相应的行情
                          CLOSE_PATTERN="today",  # 面对支持平今的交易所，优先平今或者平昨 ---> today: 平今, yesterday: 平昨， 其他:d
                          TODAY_EXCHANGE=[Exchange.SHFE.value, Exchange.INE.value],  # 需要支持平今的交易所代码列表
                          AFTER_TIMEOUT=3,  # 设置after线程执行超时,
                          TIMER_INTERVAL=1,
                          PATTERN="real"
                          )
    config_class = Config
    
    def __init__(self,name) -> None:
        self.name = name
        self.instance_path = None
        self.app_signal = AppSignal(self.name)
        self.recorder = Recorder(self)
        self.trader = BeeTdApi(self.app_signal)
        self.main_contract = self.recorder.main_contract_list
        self.config = self.make_config()
        self.logger = MyLogger()
        self._extensions = {}
    
    def make_config(self):
        """
        生成config实例
        """
        defaults = dict(self.default_config)
        return self.config_class(self.instance_path, defaults)
    
    def getfees1(self):
        self.trader.connect(info.get("CONNECT_INFO"))
        all_fees = []
        while(len(self.main_contract)==0):
            self.trader.reqQryDepthMarketData({},1)
            ct.sleep(5)
            self.main_contract = self.recorder.main_contract_list
        for local_symbol in self.main_contract:
            
            pre_settle_price = self.recorder.get_contract_last_price(
                local_symbol
            )  #获取前结算价 maketdepth数据,main_contract_mapping中的local_contract_price_mapping
            
            contract = self.recorder.get_contract(
                local_symbol)  # recorder.contracts
            
            if not contract.product.name == "FUTURES":  #非期货下一个
                continue

            pricetick = contract.pricetick  #一跳
            size = contract.size  #合约乘数
            longMr = contract.long_margin_ratio 
            shortMr = contract.short_margin_ratio
            feedata = FeeData()
            feedata.local_symbol=local_symbol
            feedata.name = contract.name
            feedata.longM1=longMr
            feedata.shortM1=shortMr
            feedata.pricetick=pricetick
            feedata.size=size
            feedata.pre_settle_price=pre_settle_price
            
            all_fees.append(feedata)
        
        self.all_fees = all_fees
        self.trader.close()
  

def load_fees_from_pickcle():
    all_fees = []
    
    with open(r"./feetmp.data","rb") as f:
        feesdatas =pickle.load(f)
        f.close()
        
    for feedata in feesdatas:
        feedata.repost()#生成symbol
        fees_row = getfees_bycode(feedata.symbol)#这里是symbol
        
        code, longM, shortM, openM, closeM, closetM, openV, closeV, closetV = fees_row
        
        feedata.longM2 =longM
        feedata.shortM2 =shortM
        feedata.openM = openM
        feedata.closeM = closeM
        feedata.closetM = closetM
        feedata.openV = openV
        feedata.closetV = closetV        
        feedata.repost()
        all_fees.append(feedata)
   
    cols = [
            "代码", "名称","多保证金1", "多保证金2", "空保证金1","空保证金2", "开费%", "平费%", "平今费%", "开费(手)", "平费(手)","平今费(手)","一跳价格", "合约乘数","一跳盈亏", "昨结算价", "合约价值","一手多","一手空","冲击成本"
        ]       
    
    datas = []
    for x in all_fees:
        datas.append([x.local_symbol,x.name, x.longM1, x.longM2,x.shortM1,x.shortM2,x.openM,x.closeM,x.closetM,x.openV,x.closeV,x.closetV,x.pricetick,x.size,x.pertick,x.pre_settle_price,x.value,x.onehandL,x.onehandS,x.cjcb])
    
    pdatas = pd.DataFrame(data=datas, columns=cols)
    pdatas.to_excel('margin.xlsx', sheet_name='Sheet1', index=False)
    print(f"feedata is \n{pdatas}\n")  

def save_feesdata_pickle():
    app = FakeAppForGenFees("fake")
    app.getfees1()
    feesdatas = app.all_fees
    with open(r"./feetmp.data","wb") as f:
        pickle.dump(feesdatas,f) 
        f.close() 
    
if __name__ == "__main__":
    save_feesdata_pickle() # 步骤1
    # load_fees_from_pickcle() #步骤2 分开.


    
    
    
    

        
        