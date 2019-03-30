# ctp-market

## download 
```
git clone https://github.com/somewheve/ctp-market
```

## libraries

- [vnpy][https://github.com/vnpy/vnpy]
- pymongo
- blinker

## start 
```bash
python start.py  

2019-03-30 14:34:28	INFO :	SYSTEM	交易服务器连接状态:True
2019-03-30 14:34:29	INFO :	SYSTEM	收到合约数据
2019-03-30 14:34:29	INFO :	SYSTEM	关闭交易服务器链接
****************************************************************************************************
CThostFtdcUserApiImplBase::OnSessionDisconnected[0x7fb160000b28][233963521][    0]
****************************************************************************************************
2019-03-30 14:34:29	INFO :	SYSTEM	数据服务器连接.
2019-03-30 14:34:29	INFO :	SYSTEM	数据服务器登录完成.
2019-03-30 14:34:31	INFO :	SYSTEM	准备订阅新的数据
2019-03-30 14:34:31	INFO :	SYSTEM	成功订阅
2019-03-30 14:34:31	INFO :	SYSTEM	启动成功
```

## 配置文件 
> ctp-market/setting.py

CONNECT_INFO : ctp连接信息

XMIN ： k线配置, 【int, int, int...】





####好用记得点个star哦  QAQ
