from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib

from ctpbee.constant import OrderData, TradeData, Offset, Direction


class MessageHelper:

    def send_message(self, title, sub, message: str = None):
        """ 实现基准的发送消息结构 """
        raise NotImplemented

    def send_trade(self, order: OrderData or TradeData):
        """  报单信息提醒 """
        raise NotImplemented


class Mail(MessageHelper):
    def __init__(self, mail_config: dict):
        self.to = mail_config.get("TO", [])
        self.passwd = mail_config.get("PASSWD")
        self.user_email = mail_config.get("USER_EMAIL")
        self.port = mail_config.get("PORT", 465)
        self.smtp = mail_config.get("SERVER_URI")

        self.smtp_api = smtplib.SMTP_SSL(self.smtp, self.port)
        self.smtp_api.login(self.user_email, self.passwd)

    def send_message(self, title="ctpbee 日内邮件提醒", sub="日内邮件提醒", message: str = None):
        email = MIMEMultipart()
        email['Subject'] = title
        email['From'] = self.user_email
        email['To'] = self.to[0]
        text = MIMEText(f"{datetime.now()} \n邮件类型: {sub}\n{message if message is not None else ''}")
        email.attach(text)
        try:
            self.smtp.sendmail(self.user_email, self.to, email.as_string())  # 发送邮件
        except smtplib.SMTPDataError as e:
            print(f"{datetime.now()} 邮件发送失败 Reason: {e}")
        except smtplib.SMTPServerDisconnected:
            self.smtp_api = smtplib.SMTP_SSL(self.smtp, self.port)
            self.smtp_api.login(self.user_email, self.passwd)
            self.smtp_api.sendmail(self.user_email, self.to, email.as_string())  # 发送邮件

    def send_trade(self, order: OrderData or TradeData):
        email = MIMEMultipart()
        email['Subject'] = f"{order.local_symbol} 报单提醒"
        email['From'] = self.user_email
        email['To'] = self.to[0]

        if order.offset == Offset.OPEN:
            direction = '多' if order.direction == Direction.LONG else '空'
        else:
            direction = '空' if order.direction == Direction.LONG else '多'

        offset = '开' if order.offset == Offset.OPEN else '平'
        beh = offset + direction
        text = MIMEText(f"报单价格: {order.price}\n报单手数: {order.volume} \n"
                        f"报单行为: {beh} \n")
        email.attach(text)
        try:
            self.smtp_api.sendmail(self.user_email, self.to, email.as_string())  # 发送邮件
        except smtplib.SMTPDataError as e:
            print(f"{datetime.now()} 邮件发送失败 Reason: {e}")
        except smtplib.SMTPServerDisconnected:
            self.smtp_api = smtplib.SMTP_SSL(self.smtp, self.port)
            self.smtp_api.login(self.user_email, self.passwd)
            self.smtp_api.sendmail(self.user_email, self.to, email.as_string())  # 发送邮件


class DingTalk(MessageHelper):
    """ Wait to Implement"""


if __name__ == '__main__':
    """ 简单的调用例子 """
    config = {
        "USER_EMAIL": "somewheve@gmail.com",
        "TO": ["somewheve@gmail.com"],
        "SERVER_URI": "smtp.exmail.qq.com",
        "PASSWD": "passwd",
        "PORT": 465
    }
    mail = Mail(mail_config=config)
    mail.send_message(message="你好呀")
