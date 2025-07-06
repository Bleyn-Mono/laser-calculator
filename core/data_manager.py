import os
import pandas as pd
import sys


class ExcelDataLoader:
    df=None

    def load_data(self, folder_name='data', file_name='calculator_data.xlsx'):
        """
        Загружает данные из Excel-файла.
        Возвращает DataFrame или пустой DataFrame в случае ошибки.
        """
        # Определяем базовую директорию приложения
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            # Если приложение заморожено (например, PyInstaller)
            # sys._MEIPASS указывает на временную папку, где распакованы ресурсы
            base_dir = sys._MEIPASS
        else:
            # Если приложение запущено как обычный Python скрипт
            # __file__ указывает на путь к текущему скрипту
            base_dir = os.path.dirname(os.path.abspath(__file__))
            base_dir = os.path.join(base_dir, '..')
        data_folder_path = os.path.join(base_dir, folder_name)
        file_path = os.path.join(data_folder_path, file_name)

        try:
            df = pd.read_excel(file_path)
        except FileNotFoundError:
            print(f"Ошибка: Файл '{file_name}' не найден по пути: {file_path}")
            print("Убедитесь, что файл существует и путь к нему указан верно.")
            pd.DataFrame()
        except Exception as e:
            print(f"Произошла ошибка при чтении файла Excel: {e}")
            pd.DataFrame()
        return df


class DataManager:
    _instance = None

    def __new__(cls):
        # Эта часть обеспечивает Singleton-поведение
        if cls._instance is None:
            cls._instance = super(DataManager, cls).__new__(cls)
            cls._instance._data_df = None
        return cls._instance

    def __init__(self):
        # Метод __init__ будет вызван только один раз, при первом создании экземпляра
        if self._data_df is None:
            loader = ExcelDataLoader()
            self._data_df = loader.load_data()
            if self._data_df.empty:
                print("DataManager: Данные не были загружены или DataFrame пуст.")
        else:
            print("DataManager: Данные уже загружены.")

    def _is_data_available(self):
        """
        Вспомогательный метод для проверки наличия загруженных данных.
        Возвращает True, если данные доступны, иначе False.
        """
        return self._data_df is not None and not self._data_df.empty

    def get_materials(self):
        """
        Возвращает отсортированный список всех уникальных материалов,
        доступных в таблице данных.

        Используется для заполнения выпадающего списка с выбором материала
        или других элементов интерфейса.

        Возвращает:
            list: Отсортированный список строк — названий материалов.
                  Если данные отсутствуют — возвращается пустой список.
        """
        if not self._is_data_available():
            return []

        return sorted(self._data_df['materials'].unique().tolist())

    def get_thickness_option(self, material):
        """
        Возвращает список доступных толщин (в мм) для заданного материала.

        Параметры:
            material (str): Название материала, для которого нужно получить толщины.

        Возвращает:
            list: Список значений толщины (в мм), доступных для выбранного материала.
                  Если данных нет или материал не найден — возвращается пустой список.
        """
        if not self._is_data_available():
            return []

        filter_thick_df = self._data_df[self._data_df['materials'] == material]
        return filter_thick_df['thickness мм'].tolist()

    def get_tip_option(self, material=None, thickness=None):
        """
        Возвращает список значений столбца 'tip' из таблицы данных,
        отфильтрованных по заданным материалу и/или толщине.

        Параметры:
            material (str, optional): Название материала, по которому нужно фильтровать.
                                      Если None, фильтрация по материалу не применяется.
            thickness (float | int, optional): Значение толщины в мм для фильтрации.
                                               Если None, фильтрация по толщине не применяется.

        Возвращает:
            list: Список значений из столбца 'tip', соответствующих указанным условиям фильтрации.
                  Если данные отсутствуют или условия не заданы — возвращается пустой список.
        """
        if not self._is_data_available():
            return []

        dataframe = self._data_df
        conditions = pd.Series([True] * len(dataframe))

        if material is not None:
            conditions &= (dataframe['materials'] == material)

        if thickness is not None:
            conditions &= (dataframe['thickness мм'] == thickness)

        filter_tip_df = dataframe[conditions]

        return filter_tip_df['tip'].tolist()
