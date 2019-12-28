"""
抽象组件
"""


class DataSupport:
    @staticmethod
    def _get_link(**kwargs):
        if "host" in kwargs.keys():
            host = kwargs.get("host")
        else:
            host = "127.0.0.1"

        if "port" in kwargs.keys():
            port = kwargs.get("port")

        else:
            port = 27017

        if "user" in kwargs.keys():
            user = kwargs.get("user")
        else:
            user = None
        if "pwd" in kwargs.keys():
            pwd = kwargs.get("pwd")
        else:
            pwd = None
        auth = ""
        if user and pwd:
            auth = f"{user}:{'*' * len(pwd)}@"
        return f"mongodb://{auth}{host}:{port}"
