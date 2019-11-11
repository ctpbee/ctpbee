# ctpbee 
bee bee .... 为二次开发而生 ~~


![ctpbee](https://github.com/ctpbee/ctpbee/blob/master/docs/source/ctpbee.jpg)

ctpbee 提供了一个可供使用的交易微框架, 你可以通过这个微小的核心来构建值得信赖的工具， 
当然这需要你的编程功力。 你所需要关心的是如何编程来处理行情和交易信息即可。

## 开始之前 
```bash
# just for linux 
sudo locale-gen zh_CN.GB18030  
```
## 起源

- 衍生自 [vnpy](https://github.com/vnpy/vnpy) 和 [flask](https://github.com/pallets/flask)  

## 安装 
```bash
# code install 
git clone https://github.com/ctpbee/ctpbee && cd ctpbee && python3 setup.py install  

# pip install
pip3 install ctpbee
```

## docker 快速部署

```
docker pull yutiansut/ctpbee:latest
docker run -p 5000:5000 yutiansut/ctpbee:latest
```

本地打开 localhost:5000 即可使用

## 文档
本地生成:

    1. git clone https://github.com/ctpbee/ctpbee 
    2. pip3 install sphinx
    3. cd ./ctpbee/docs && make html
    4. 你可以在docs/build/html 下面看到index.html, 浏览器打开即可
    
在线:
    [文档](http://docs.ctpbee.com)

## 社区支持
[地址](http://community.ctpbee.com)
    
    
## 功能支持

- [x] k线数据支持/home/somewheve/Templates
- [x] 分时图数据支持
- [x] 交易支持
- [x] 行情支持 --> 需要自己编写相应的数据库写入代码。
- [x] 自由自在的发单方式
- [x] 多账户支持
- [x] 支持申请穿透式接口
- [x] 快速下单助手
- [x] 风控层建立
- [x] 跟单信号
- [x] 多路行情对比 --> [looper_me](https://github.com/ctpbee/looper_me)
- [x] 数据快速支持 --> [ctpbee_converter](https://github.com/ctpbee/data_converter)
- [x] cta support 
- [x] 回测系统搭建  --> interface/looper


## 插件支持

- [ ] 套利 ---> ready to support
- [ ] 历史数据 support


## 一些可能会减少你工作量的工作
- [x] 7×24小时无人值守 (可选)
- [x] 定时查持仓和账户信息  (可选)
- [x] 策略对应订阅行情 (可选)
- [ ] 性能优化 --> julia支持 ？
- [ ] 对接多种指标计算                     
- [ ] 优化代码  / try to do it 

## 快速开始 
```python
from ctpbee import CtpBee
app = CtpBee("ctpbee", __name__) 
info = {
    "CONNECT_INFO": {
        "userid": "",
        "password": "",
        "brokerid": "",
        "md_address": "",
        "td_address": "",
        "appid": "",
        "auth_code": "",
        "product_info":""
    },
    "INTERFACE":"ctp",
    "TD_FUNC": True,  # 开启交易功能 
}
app.config.from_mapping(info)  # 从dict中载入信息 对于更多配置载入方式, 请参阅文档或者阅读代码
app.start() 
```




## 发展计划
ctpbee主要面对开发者, 希望能得到各位大佬的支持. 后续不再开发examples. 
策略以及指标等工具都以ctpbee_** 形式发布. ctpbee只提供最小的内核. 本人崇尚开源, 无论你是交易者还是程序员, 只要你有新的想法以及对开源感兴趣, 欢迎基于ctpbee 开发出新的可用工具. 我会维护一个工具列表, 指引用户前往使用. 

## 最后一句 
ctpbee是开源项目, 如果你同意使用ctpbee, 那么我们默认你 *清楚* 你的每个行为带来的*后果*, 加以思考并自行承担后果！

如果这个能帮助到你, 请点击star来支持我噢. ^_^  

如果你希望贡献代码, 欢迎加群一起讨论和或者提交PR  QQ群号(: 756319143) [点进加入群聊以了解更多](https://jq.qq.com/?_wv=1027&k=5xWbIq3)

如果你有遇到问题请发邮件给我 邮箱: somewheve@gmail.com 我会及时回复! 
最后一句 ----> 祝各位大佬都能赚钱 ！



