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

from colour_printing.config import CPConfig, Term

from datetime import datetime

from colour_printing import Mode, Fore, Back

get_time = lambda: datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S.%f')[:-3]

TEMPLATE = "{created} {name}     {levelname}  {owner}   {message}"
CP = CPConfig(TEMPLATE)  # 导出CP


class Paper(object):

    @CP.wrap
    def info(self):
        self.created = Term(Fore.RED, default=get_time)
        self.name = Term()
        self.levelname = Term(Fore.PURPLE, default="INFO")
        self.owner = Term(Fore.CYAN)
        self.message = Term(Fore.GREEN)

    @CP.wrap
    def success(self):
        self.created = Term(Fore.CYAN, default=get_time)
        self.name = Term(Fore.CYAN)
        self.levelname = Term(default="SUCCESS")
        self.owner = Term(Fore.CYAN)
        self.message = Term(Fore.CYAN)

    @CP.wrap
    def warning(self):
        self.created = Term(Fore.RED, default=get_time)
        self.name = Term()
        self.levelname = Term(Fore.PURPLE, default="WARNING")
        self.owner = Term(Fore.CYAN)
        self.message = Term(Fore.YELLOW)

    @CP.wrap
    def error(self):
        self.created = Term(Fore.RED, default=get_time)
        self.name = Term()
        self.levelname = Term(Fore.PURPLE, default="ERROR")
        self.owner = Term(Fore.CYAN)
        self.message = Term(Fore.RED)

    @CP.wrap
    def debug(self):
        self.created = Term(Fore.RED, default=get_time)
        self.name = Term()
        self.levelname = Term(Fore.PURPLE, default="DEBUG")
        self.owner = Term(Fore.CYAN)
        self.message = Term(Fore.PURPLE)
