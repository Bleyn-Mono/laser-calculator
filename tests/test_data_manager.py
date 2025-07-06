import unittest
import pandas as pd

from unittest.mock import patch, MagicMock
from core.data_manager import ExcelDataLoader

from core.data_manager import DataManager



class TestData(unittest.TestCase):


    def setUp(self):
        DataManager._instance = None

    def test_excel_loader(self):
        loader = ExcelDataLoader()
        test_df = loader.load_data()
        if not test_df.empty:
            print("\nDataLoader успешно загрузил данные. Head:\n", test_df.head())

    @patch('core.data_manager.ExcelDataLoader.load_data')
    def test_get_materials(self, mock_data_loader_material):
        # Подготавливаем фиктивные данные
        mock_data_loader_material.return_value = pd.DataFrame({
            'materials': ['Steel', 'Aluminum', 'Steel'],
            'thickness': [1, 2, 3]
        })

        dm = DataManager()
        materials = dm.get_materials()

        self.assertTrue(materials, ['Aluminum', 'Steel'])

    @patch('core.data_manager.ExcelDataLoader.load_data')
    def test_get_thickness_option(self, mock_data_loader_thickness):
        mock_data_loader_thickness.return_value = pd.DataFrame({
            'materials': ['Steel', 'Aluminum', 'Steel'],
            'thickness мм': [1, 2, 3]
        })

        dm = DataManager()

        self.assertEqual(dm.get_thickness_option('Lufi'), [])
        self.assertEqual(dm.get_thickness_option('Steel'), [1, 3])
        self.assertEqual(dm.get_thickness_option('Aluminum'), [2])

    @patch('core.data_manager.ExcelDataLoader.load_data')
    def test_get_tip_option(self, mock_data_load_tip_option):
        mock_data_load_tip_option.return_value = pd.DataFrame({
            'materials': ['Steel', 'Aluminum', 'Steel'],
            'thickness мм': [1, 2, 3],
            'tip':[1, 1.5, 2]
        })

        dm = DataManager()
        self.assertEqual(dm.get_tip_option('Lufi'), [])
        self.assertEqual(dm.get_tip_option('Steel', 1), [1])
        self.assertEqual(dm.get_tip_option('Steel'), [1, 2])


if __name__ == '__main__':
    unittest.main()
