# ctpbee 
bee bee .... 为二次开发而生 ~~ 

>  tiny but strong

ctpbee 提供了一个可供使用的交易微框架, 你可以通过这个微小的核心来构建值得信赖的工具， 
当然这需要你的编程功力。 你所需要关心的是如何编程来处理行情和交易信息即可。

## 开始之前 
```bash
# just for linux/ 生成中文环境
sudo ctpbee -auto generate
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

## 文档
文档中描述相关教程，请认真阅读。如有问题，请到底部加群或者邮件联系作者 ^_^  
> 当前文档已经落后, 请等待作者进行更新 ~
[文档](http://docs.ctpbee.com)

    
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

## Todo
- [x] 对接自定义行情 
- [ ] 对接账户qifi格式
- [ ] 对接qifi_struct
- [ ] bug/维护
- [ ] 模拟实现 ---> sim interface ==> will send to next release
- [ ] [fast_pub 计划](https://github.com/ctpbee/fast-pub) ---> 描述为提供HTTP API进行实盘下单的解决方案


## 插件支持

- [ ] 套利 ---> ready to support
- [ ] 历史数据 support 


## QA_SUPPORT
当前针对[QUANTAXIS](http://github.com/QUANTAXIS/QUANTAXIS)的数据对接!
ctpbee作为开发框架并不具有历史数据的功能，我们也因为条件所限无法提供，**但是现在这些都不是问题**
我们提供了QA_SUPPORT版本支持，能让你轻松通过几个命令来获取历史数据。
> 此处感谢[QA作者yutiansut](https://github.com/yutiansut)，阻止了我重复造轮子

关于此个版本的支持，请参见[文档](https://docs.ctpbee.com/)中的[安装](https://docs.ctpbee.com/install)

## 模拟/SIM
ctpbee基于回测的机制添加了`sim`接口， 通过配置的接口`INTERFACE`填入`sim`即可进行载入,
此处描述为通过[fast-pub](https://github.com/ctpbee/fast-pub)拉起一个模拟服务器，通过`HTTP API`来获取策略机制. 此项功能正在研发中~~ 欢迎通过`issue`来进行反馈!


## 一些可能会减少你工作量的工作
- [x] 7×24小时无人值守 (可选)
- [x] 定时查持仓和账户信息  (可选)
- [x] 策略对应订阅行情 (可选)
- [ ] 对接多种指标计算                     
- [ ] 优化代码  / Hope for your work ^_^

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

## 命令行运行截图 
![avatar](source/运行.png)

## 贡献代码
如果你希望贡献代码，请遵循以下步骤，注意我们仅仅接受向dev`分支提交代码 ! ! ! ! 

1. `fork`本项目到你的`github`本地仓库
2. `clone`你账户的`ctpbee dev`分支的代码到本地
3. 修改提交到你自己本地仓库到dev分支中。
4. 打开[地址](https://github.com/ctpbee/ctpbee/compare/dev?expand=1)。点击`compare across forks`，将`base`中的`branch`选为`dev`,`head`选取你自己的项目地址，分支选取`dev`，点击提交即可。


## 最后一句 
ctpbee是开源项目, 如果你同意使用ctpbee, 那么我们默认你 *清楚* 你的每个行为带来的*后果*, 加以思考并自行承担后果！

如果这个能帮助到你, 请点击star来支持我噢. ^_^  

QQ群号(: 756319143)， [点进加入群聊以了解更多](https://jq.qq.com/?_wv=1027&k=5xWbIq3)

如果你有遇到问题请发邮件给我 邮箱: somewheve@gmail.com 我会及时回复! 
最后一句 ----> 祝各位大佬都能赚钱 ！



