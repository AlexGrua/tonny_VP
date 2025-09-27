"""
Модуль для загрузки и подготовки данных
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
from config import COLUMN_MAPPING, DATA_FOLDER, DATE_FORMAT

class DataLoader:
    def __init__(self, data_folder=DATA_FOLDER):
        self.data_folder = data_folder
        self.df = None
        
    def load_csv(self, filename):
        """Загрузка CSV файла"""
        filepath = os.path.join(self.data_folder, filename)
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Файл {filepath} не найден")
            
        print(f"Загружаем данные из {filepath}...")
        self.df = pd.read_csv(filepath)
        print(f"Загружено {len(self.df)} строк")
        return self.df
    
    def prepare_data(self):
        """Подготовка данных для анализа"""
        if self.df is None:
            raise ValueError("Сначала загрузите данные с помощью load_csv()")
            
        # Нормализация названий колонок
        df = self.df.copy()
        
        # Проверяем наличие необходимых колонок
        required_cols = list(COLUMN_MAPPING.values())
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            print(f"Предупреждение: отсутствуют колонки {missing_cols}")
            print(f"Доступные колонки: {list(df.columns)}")
        
        # Нормализация данных
        if 'dates' in df.columns:
            df['dates'] = pd.to_datetime(df['dates'], errors='coerce')
        
        # Создание составных ключей
        df['country'] = df.get('countryName', '').str.upper().str.strip()
        df['service'] = df.get('webserviceName', '').str.upper().str.strip()
        df['item_id'] = df['country'] + " | " + df['service']
        
        # Нормализация ID клиентов и поставщиков
        if 'consumerName' in df.columns:
            df['consumer_id'] = df['consumerName'].astype('category').cat.codes
        if 'producerName' in df.columns:
            df['supplier_id'] = df['producerName'].astype('category').cat.codes
            
        # Очистка числовых данных
        numeric_cols = ['consumerAmount', 'producerAmount', 'all_orders', 'Profit']
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Удаление строк с некорректными данными
        initial_count = len(df)
        df = df.dropna(subset=['dates', 'item_id'])
        final_count = len(df)
        
        if initial_count != final_count:
            print(f"Удалено {initial_count - final_count} строк с некорректными данными")
        
        self.df = df
        return df
    
    def get_weekly_data(self, weeks_back=1):
        """Получение данных за последние N недель"""
        if self.df is None:
            raise ValueError("Сначала загрузите и подготовьте данные")
            
        end_date = self.df['dates'].max().normalize()
        start_date = end_date - timedelta(weeks=weeks_back)
        
        weekly_data = self.df[
            (self.df['dates'] >= start_date) & 
            (self.df['dates'] < end_date)
        ].copy()
        
        print(f"Данные за {weeks_back} недель: {len(weekly_data)} строк")
        print(f"Период: {start_date.strftime(DATE_FORMAT)} - {end_date.strftime(DATE_FORMAT)}")
        
        return weekly_data
    
    def get_historical_data(self, weeks_back=8):
        """Получение исторических данных за N недель"""
        if self.df is None:
            raise ValueError("Сначала загрузите и подготовьте данные")
            
        end_date = self.df['dates'].max().normalize()
        start_date = end_date - timedelta(weeks=weeks_back)
        
        historical_data = self.df[
            (self.df['dates'] >= start_date) & 
            (self.df['dates'] < end_date)
        ].copy()
        
        print(f"Исторические данные за {weeks_back} недель: {len(historical_data)} строк")
        print(f"Период: {start_date.strftime(DATE_FORMAT)} - {end_date.strftime(DATE_FORMAT)}")
        
        return historical_data
    
    def get_data_summary(self):
        """Получение сводки по данным"""
        if self.df is None:
            raise ValueError("Сначала загрузите данные")
            
        summary = {
            'total_rows': len(self.df),
            'date_range': (self.df['dates'].min(), self.df['dates'].max()),
            'unique_consumers': self.df['consumer_id'].nunique() if 'consumer_id' in self.df.columns else 0,
            'unique_suppliers': self.df['supplier_id'].nunique() if 'supplier_id' in self.df.columns else 0,
            'unique_items': self.df['item_id'].nunique() if 'item_id' in self.df.columns else 0,
            'total_profit': self.df['Profit'].sum() if 'Profit' in self.df.columns else 0,
            'avg_sell_price': self.df['consumerAmount'].mean() if 'consumerAmount' in self.df.columns else 0,
            'avg_buy_price': self.df['producerAmount'].mean() if 'producerAmount' in self.df.columns else 0
        }
        
        return summary

