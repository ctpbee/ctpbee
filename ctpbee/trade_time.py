import datetime
import json
import os
import re

import requests
from lxml import etree


def handle_holidays(year, holidays):
    pattern = re.compile(r'\d{1,2}[\u4e00-\u9fa5]{1}\d{1,2}[\u4e00-\u9fa5]{1}')  # 1月22日
    holidays_map = {
        "元旦": [],
        "春节": [],
        "清明节": [],
        "劳动节": [],
        "端午节": [],
        "国庆节": [],
        "中秋节": [],
    }
    for festival in holidays:
        if festival[0] in holidays_map:  # 判断是否在节日map
            b_e = festival[1].split('~')
            if len(b_e) == 1:
                that = re.match(pattern, b_e[0])
                if that:
                    holidays_map[festival[0]] = [year + "-" + that.group().replace('月', '-').replace('日', '')]
            elif len(b_e) == 2:
                begin, end = b_e
                begin = re.match(pattern, begin)
                end = re.match(pattern, end)
                if begin and end:
                    begin_m_index = begin.group().index('月')  # 月 index
                    begin_m = int(begin.group()[:begin_m_index])  # 月份
                    end_m_index = end.group().index('月')  # 月 index
                    end_m = int(end.group()[:end_m_index])  # 月份
                    # 开始月份 > 结束月份  :开始年份-1
                    if begin_m > end_m:
                        b_year = str(int(year) - 1)
                    else:
                        b_year = year
                    begin = b_year + "-" + begin.group().replace('月', '-').replace('日', '')
                    end = year + "-" + end.group().replace('月', '-').replace('日', '')
                    holidays_map[festival[0]] = get_every_day(begin, end)
    return holidays_map


def get_every_day(begin_date, end_date):
    date_list = []
    # 转datetime
    begin_date = datetime.datetime.strptime(begin_date, "%Y-%m-%d")
    end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
    while begin_date <= end_date:
        # 转str
        date_str = begin_date.strftime("%Y-%m-%d")
        date_list.append(date_str)
        begin_date += datetime.timedelta(days=1)
    return date_list


class Papa:
    """
    unstabitily
    """
    url = "https://fangjia.51240.com/{year}__fangjia/"
    last = {}
    path = os.path.join(os.path.dirname(__file__), 'holiday.json')
    if not os.path.exists(path):
        open(path, 'w')

    @classmethod
    def parse(cls, year):
        html = requests.get(cls.url.format(year=year)).content.decode()
        tree = etree.HTML(html)
        raw = tree.xpath(r'//td | //td/a')
        return raw

    @classmethod
    def run(cls, start_end: list):
        years = [i for i in range(int(start_end[0]), int(start_end[1]) + 1)]
        for year in years:
            year = str(year)
            data = cls.parse(year)
            # if not data: continue
            ll = []
            # 去空项
            # ['节日', '放假时间', '调休上班日期', '放假天数',
            # '元旦', '1月1日~1月3日', '2011年12月31日（星期六）', '3天',
            # '春节', '1月22日~1月28日', '1月21日（星期六）、1月29日（星期日）', '7天',
            # '清明节', '4月2日~4月4日', '3月31日（星期六）、4月1日（星期日）', '3天',
            # '劳动节', '4月29日~5月1日', '4月28日（星期六）', '3天',
            # '端午节', '6月22日~6月24日', '无', '3天',
            # '中秋节', '9月30日', '9月29日（星期六）', '1天',
            # '国庆节', '10月1日~10月7日', '无', '7天']
            for i in data:
                if i.text is not None:
                    ll.append(i.text)
            print(year, ll)
            # 排列分组  4个一组但只取前2个
            # [['节日', '放假时间'], ['元旦', '1月1日~1月3日'],
            # ['春节', '1月22日~1月28日'], ['清明节', '4月2日~4月4日'],
            # ['劳动节', '4月29日~5月1日'], ['端午节', '6月22日~6月24日'],
            # ['中秋节', '9月30日'], ['国庆节', '10月1日~10月7日']]
            holidays = [ll[j:j + 2] for j in range(0, len(ll), 4)]
            cls.last[year] = handle_holidays(year, holidays)

    @classmethod
    def read(cls):
        if os.path.getsize(cls.path):
            with open(cls.path, 'r', encoding='utf8')as f:
                s = json.load(f)
        else:
            with open(cls.path, 'w') as f:
                s = {"2019": {"元旦": [], "春节": [], "清明节": [], "劳动节": [], "端午节": [], "国庆节": [], "中秋节": [], }}
                f.write(json.dumps(s, ensure_ascii=False))
        return s

    @classmethod
    def write(cls):
        if os.path.getsize(cls.path):
            data = cls.read()
            data.update(cls.last)
            with open(cls.path, 'w')as f:
                f.write(json.dumps(data, ensure_ascii=False))
        else:
            with open(cls.path, 'w')as f:
                f.write(json.dumps(cls.last, ensure_ascii=False))

    @classmethod
    def get_holiday(cls):
        holidays = cls.read()
        result = {}
        for year, holiday in holidays.items():
            temp = []
            for date in holiday.values():
                for i in date:
                    temp.append(datetime.datetime.strptime(i, "%Y-%m-%d"))
            result[year] = temp
        return result


class TradingDay:
    """ 交易日历支持 """
    trade_time = Papa.get_holiday()

    @classmethod
    def is_holiday(cls, date: datetime.datetime or datetime.date):

        year = date.year
        month = date.month
        day = date.day
        holiday_list = cls.trade_time.get(str(year))
        if holiday_list:
            for i in holiday_list:
                if i.month == month and i.day == day:
                    return True
        return False

    @classmethod
    def is_weekend(cls, date: datetime.datetime or datetime.date):
        weekday = date.weekday()
        if weekday == 5 or weekday == 6:
            return True
        return False

    @classmethod
    def is_trading_day(cls, date: datetime.datetime or datetime.date):
        """ 判断是否为交易日 """
        if cls.is_weekend(date) or cls.is_weekend(date):
            return False
        return True


if __name__ == '__main__':
    # 爬
    Papa.run([2004, datetime.datetime.now().year])
    # Papa.write()
