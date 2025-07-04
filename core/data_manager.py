import os
import pandas as pd
import sys


class DataManager:
    _instance = None
    _data_df = None

    def __new__(cls):
        # Эта часть обеспечивает Singleton-поведение
        if cls._instance is None:
            cls._instance = super(DataManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        # Метод __init__ будет вызван только один раз, при первом создании экземпляра
        if DataManager._data_df is None:
            self._load_data()

    def _load_data(self):
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
        data_folder_path = os.path.join(base_dir, 'data')
        file_name = 'calculator_data.xlsx'
        file_path = os.path.join(data_folder_path, file_name)

        try:
            DataManager._data_df = pd.read_excel(file_path)
        except FileNotFoundError:
            print(f"Ошибка: Файл '{file_name}' не найден по пути: {file_path}")
            print("Убедитесь, что файл существует и путь к нему указан верно.")
        except Exception as e:
            print(f"Произошла ошибка при чтении файла Excel: {e}")

    def get_materials(self):
        #Предоставить список всех уникальных материалов, доступных в вашем calculator_data.xlsx.
        if DataManager._data_df is not None and DataManager._data_df.empty:
            return sorted(DataManager._data_df['material'].unique().tolist())
        return []

    def get_thickness_option(self):
        if DataManager._data_df is None or DataManager._data_df.empty:
            return []
        

