"""
#                     *Colour-printing Reference*
#########################################################################################
#   @'fore': # 前景色         @'back':# 背景              @'mode':# 显示模式               # 
#            'black': 黑色            'black':  黑色              'normal': 终端默认设置   # 
#            'red': 红色              'red':  红色                'bold':  高亮显示        # 
#            'green': 绿色            'green': 绿色               'underline':  使用下划线 #
#            'yellow': 黄色           'yellow': 黄色              'blink': 闪烁           # 
#            'blue':  蓝色            'blue':  蓝色               'invert': 反白显示       #    
#            'purple':  紫红色        'purple':  紫红色            'hide': 不可见          #    
#            'cyan':  青蓝色          'cyan':  青蓝色                                     #
#            'white':  白色           'white':  白色                                     #
#########################################################################################
"""
from datetime import datetime
from colour_printing import Mode, Fore, Back

get_time = lambda: datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S,%f')[:-3]

TEMPLATE = "{created} {name}     {levelname}  {owner}   {message}"

created_default = get_time

name_default = ""

levelname_default = ""

owner_default = ""

message_default = ""

INFO = {
    "created": {
        "DEFAULT": created_default,  # 默认值
        "fore": Fore.RED,  # 前景色
        "back": Back,  # 背景色
        "mode": Mode,  # 模式
    },

    "name": {
        "DEFAULT": name_default,  # 默认值
        "fore": Fore,  # 前景色
        "back": Back,  # 背景色
        "mode": Mode,  # 模式
    },

    "levelname": {
        "DEFAULT": "INFO",  # 默认值
        "fore": Fore.PURPLE,  # 前景色
        "back": Back,  # 背景色
        "mode": Mode,  # 模式
    },

    "owner": {
        "DEFAULT": owner_default,  # 默认值
        "fore": Fore.CYAN,  # 前景色
        "back": Back,  # 背景色
        "mode": Mode,  # 模式
    },

    "message": {
        "DEFAULT": message_default,  # 默认值
        "fore": Fore.GREEN,  # 前景色
        "back": Back,  # 背景色
        "mode": Mode,  # 模式
    },
}

SUCCESS = {
    "created": {
        "DEFAULT": created_default,  # 默认值
        "fore": Fore.CYAN,  # 前景色
        "back": Back,  # 背景色
        "mode": Mode,  # 模式
    },

    "name": {
        "DEFAULT": name_default,  # 默认值
        "fore": Fore.CYAN,  # 前景色
        "back": Back,  # 背景色
        "mode": Mode,  # 模式
    },

    "levelname": {
        "DEFAULT": "SUCCESS",  # 默认值
        "fore": Fore.CYAN,  # 前景色
        "back": Back,  # 背景色
        "mode": Mode,  # 模式
    },

    "owner": {
        "DEFAULT": owner_default,  # 默认值
        "fore": Fore.CYAN,  # 前景色
        "back": Back,  # 背景色
        "mode": Mode,  # 模式
    },

    "message": {
        "DEFAULT": message_default,  # 默认值
        "fore": Fore.CYAN,  # 前景色
        "back": Back,  # 背景色
        "mode": Mode,  # 模式
    },
}

WARNING = {
    "created": {
        "DEFAULT": created_default,  # 默认值
        "fore": Fore.RED,  # 前景色
        "back": Back,  # 背景色
        "mode": Mode,  # 模式
    },

    "name": {
        "DEFAULT": name_default,  # 默认值
        "fore": Fore,  # 前景色
        "back": Back,  # 背景色
        "mode": Mode,  # 模式
    },

    "levelname": {
        "DEFAULT": "WARNING",  # 默认值
        "fore": Fore.PURPLE,  # 前景色
        "back": Back,  # 背景色
        "mode": Mode,  # 模式
    },

    "owner": {
        "DEFAULT": owner_default,  # 默认值
        "fore": Fore.CYAN,  # 前景色
        "back": Back,  # 背景色
        "mode": Mode,  # 模式
    },

    "message": {
        "DEFAULT": message_default,  # 默认值
        "fore": Fore.YELLOW,  # 前景色
        "back": Back,  # 背景色
        "mode": Mode,  # 模式
    },
}

ERROR = {
    "created": {
        "DEFAULT": created_default,  # 默认值
        "fore": Fore.RED,  # 前景色
        "back": Back,  # 背景色
        "mode": Mode,  # 模式
    },

    "name": {
        "DEFAULT": name_default,  # 默认值
        "fore": Fore,  # 前景色
        "back": Back,  # 背景色
        "mode": Mode,  # 模式
    },

    "levelname": {
        "DEFAULT": "ERROR",  # 默认值
        "fore": Fore.PURPLE,  # 前景色
        "back": Back,  # 背景色
        "mode": Mode,  # 模式
    },

    "owner": {
        "DEFAULT": owner_default,  # 默认值
        "fore": Fore.CYAN,  # 前景色
        "back": Back,  # 背景色
        "mode": Mode,  # 模式
    },

    "message": {
        "DEFAULT": message_default,  # 默认值
        "fore": Fore.RED,  # 前景色
        "back": Back,  # 背景色
        "mode": Mode,  # 模式
    },
}

DEBUG = {
    "created": {
        "DEFAULT": created_default,  # 默认值
        "fore": Fore.RED,  # 前景色
        "back": Back,  # 背景色
        "mode": Mode,  # 模式
    },

    "name": {
        "DEFAULT": name_default,  # 默认值
        "fore": Fore,  # 前景色
        "back": Back,  # 背景色
        "mode": Mode,  # 模式
    },

    "levelname": {
        "DEFAULT": "DEBUG",  # 默认值
        "fore": Fore.PURPLE,  # 前景色
        "back": Back,  # 背景色
        "mode": Mode,  # 模式
    },

    "owner": {
        "DEFAULT": owner_default,  # 默认值
        "fore": Fore.CYAN,  # 前景色
        "back": Back,  # 背景色
        "mode": Mode,  # 模式
    },

    "message": {
        "DEFAULT": message_default,  # 默认值
        "fore": Fore.PURPLE,  # 前景色
        "back": Back,  # 背景色
        "mode": Mode,  # 模式
    },
}
