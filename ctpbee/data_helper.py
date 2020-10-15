class DataHelper:
    """ ctpbee开发的数据读取器 ‘
    针对各自csv数据以及json或者 数据库里面的数据
    需要你提供数据地图以及如何进行字段转换
    """

    def __init__(self, mapping: str):
        self.mapping = mapping

    def read_json(self, json_path: str):
        raise NotImplemented

    def read_csv(self, csv_path: str):
        raise NotImplemented
