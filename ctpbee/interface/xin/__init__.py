import platform

if platform.system() == "Windows":
    from .md_api import XinMdApi
    from .td_api import XinTdApi
else:
    XinMdApi = None
    XinTdApi = None

__all__ = [XinMdApi, XinTdApi]
