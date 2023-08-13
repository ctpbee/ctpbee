## 对接open_ctp

open_ctp兼容ctp交易接口， 但是底层dll不一样, 需要你手动进行dll替换

1. 下载open_ctp交易的dll或者so依赖文件,前往[此处](https://github.com/openctp/openctp)下载对应平台以及对应系统的下的交易依赖支持
2. 找到你项目的路径 执行以下命令

```bash
python3 -m pip show ctpbee_api
```

会看到类似以下输出

```text
C:\Users\somew〉pip show ctpbee_api                                                             08/11/2023 05:06:22 下午
Name: ctpbee-api
Version: 0.40
Summary: single CTP API support
Home-page: https://github.com/ctpbee/ctpbee_api
Author: somewheve
Author-email: somewheve@gmail.com
License: MIT
Location: c:\users\somew\appdata\local\programs\python\python39\lib\site-packages
Requires:
Required-by: ctpbe
```

执行以下命令, 记得将路径替换成你本地机器下面输出`Location`位置

```bash
# cd c:\users\somew\appdata\local\programs\python\python39\lib\site-packages
# cd ctpbee_api/ctp
```

然后将对应的dll或者so文件进行替换即可, 再次启动即可完成open_ctp的替换工作。

