"""
测试持仓管理相关功能
"""

from unittest import TestCase
from ctpbee.data_handle.local_position import PositionModel, LocalPositionManager
from ctpbee.constant import Direction, Offset, Exchange, OrderRequest


class TestPositionModel(TestCase):
    """测试PositionModel类的基本功能"""

    def setUp(self):
        """设置测试环境"""
        self.local_symbol = "rb2401.SHFE"
        self.position_model = PositionModel(self.local_symbol)

    def test_initialization(self):
        """测试初始化功能"""
        self.assertEqual(self.position_model.local_symbol, self.local_symbol)
        self.assertEqual(self.position_model.symbol, "rb2401")
        self.assertEqual(self.position_model.exchange, "SHFE")

        # 验证初始持仓为0
        self.assertEqual(self.position_model.long_pos, 0)
        self.assertEqual(self.position_model.short_pos, 0)
        self.assertEqual(self.position_model.long_available, 0)
        self.assertEqual(self.position_model.short_available, 0)

    def test_property_access(self):
        """测试属性访问"""
        # 验证所有property装饰的属性都能正常访问
        self.assertIsInstance(self.position_model.long_pos, int)
        self.assertIsInstance(self.position_model.short_pos, int)
        self.assertIsInstance(self.position_model.long_pos_frozen, int)
        self.assertIsInstance(self.position_model.short_pos_frozen, int)
        self.assertIsInstance(self.position_model.long_td, int)
        self.assertIsInstance(self.position_model.short_td, int)
        self.assertIsInstance(self.position_model.long_yd, int)
        self.assertIsInstance(self.position_model.short_yd, int)
        self.assertIsInstance(self.position_model.long_available, int)
        self.assertIsInstance(self.position_model.short_available, int)

    def test_to_dict_method(self):
        """测试to_dict方法"""
        pos_dict = self.position_model.to_dict()
        self.assertIsInstance(pos_dict, dict)
        self.assertIn("symbol", pos_dict)
        self.assertIn("exchange", pos_dict)
        self.assertIn("long_pos", pos_dict)
        self.assertIn("short_pos", pos_dict)

    def test_position_calculation(self):
        """测试持仓计算"""
        # 模拟更新持仓
        self.position_model.long["td"] = 10
        self.position_model.long["yd"] = 20
        self.position_model.short["td"] = 5
        self.position_model.short["yd"] = 15

        # 调用计算方法
        self.position_model._calculate_position()

        # 验证计算结果
        self.assertEqual(self.position_model.long_pos, 30)  # 10+20
        self.assertEqual(self.position_model.short_pos, 20)  # 5+15


class TestLocalPositionManager(TestCase):
    """测试LocalPositionManager类的功能"""

    def setUp(self):
        """设置测试环境"""
        self.local_position_manager = LocalPositionManager(None)
        self.local_symbol = "rb2401.SHFE"

    def test_initialization(self):
        """测试初始化功能"""
        self.assertIsInstance(self.local_position_manager, LocalPositionManager)
        self.assertEqual(len(self.local_position_manager), 0)

    def test_add_position_model(self):
        """测试添加PositionModel"""
        # 添加持仓模型
        self.local_position_manager[self.local_symbol] = PositionModel(
            self.local_symbol
        )

        # 验证添加成功
        self.assertEqual(len(self.local_position_manager), 1)
        self.assertIn(self.local_symbol, self.local_position_manager)

        # 验证获取的是PositionModel实例
        pos_model = self.local_position_manager.get(self.local_symbol)
        self.assertIsInstance(pos_model, PositionModel)

    def test_get_position(self):
        """测试get_position方法"""
        # 初始状态，返回None
        self.assertIsNone(self.local_position_manager.get_position("non_existent.SHFE"))

        # 添加后，返回PositionModel
        self.local_position_manager[self.local_symbol] = PositionModel(
            self.local_symbol
        )
        pos_model = self.local_position_manager.get_position(self.local_symbol)
        self.assertIsInstance(pos_model, PositionModel)

    def test_get_all_positions(self):
        """测试get_all_positions方法"""
        # 初始状态，返回空列表
        positions = self.local_position_manager.get_all_positions()
        self.assertEqual(len(positions), 0)

        # 添加两个持仓模型
        self.local_position_manager[self.local_symbol] = PositionModel(
            self.local_symbol
        )
        self.local_position_manager["au2406.SHFE"] = PositionModel("au2406.SHFE")

        # 验证获取的列表包含两个元素
        positions = self.local_position_manager.get_all_positions()
        self.assertEqual(len(positions), 2)
        for pos in positions:
            self.assertIsInstance(pos, PositionModel)

    def test_is_convert_required(self):
        """测试is_convert_required方法"""
        # 由于app为None，get_contract返回None，所以返回False
        result = self.local_position_manager.is_convert_required(self.local_symbol)
        self.assertFalse(result)

    def test_get_contract(self):
        """测试get_contract方法"""
        # 由于app为None，应该返回None
        result = self.local_position_manager.get_contract(self.local_symbol)
        self.assertIsNone(result)

    def test_to_position_data(self):
        """测试PositionModel的to_position_data方法"""
        pos_model = PositionModel(self.local_symbol)

        # 测试获取多头持仓数据
        long_pos_data = pos_model.to_position_data(Direction.LONG)
        self.assertIsNotNone(long_pos_data)
        self.assertEqual(long_pos_data.direction, Direction.LONG)

        # 测试获取空头持仓数据
        short_pos_data = pos_model.to_position_data(Direction.SHORT)
        self.assertIsNotNone(short_pos_data)
        self.assertEqual(short_pos_data.direction, Direction.SHORT)

        # 测试获取所有持仓数据
        all_pos_data = pos_model.to_position_data()
        self.assertIsInstance(all_pos_data, list)
