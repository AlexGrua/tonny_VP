"""
Скрипт для создания примерных данных для тестирования
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def create_sample_data():
    """Создание примерных данных для тестирования"""
    
    # Параметры
    num_days = 60  # 2 месяца данных
    num_consumers = 20
    num_suppliers = 10
    num_countries = 5
    num_services = 8
    
    # Генерация базовых данных
    countries = ['USA', 'UK', 'DE', 'FR', 'CA']
    services = ['SMS', 'EMAIL', 'WHATSAPP', 'TELEGRAM', 'VIBER', 'SIGNAL', 'DISCORD', 'SLACK']
    consumers = [f'Consumer_{i:02d}' for i in range(1, num_consumers + 1)]
    suppliers = [f'Supplier_{i:02d}' for i in range(1, num_suppliers + 1)]
    
    # Генерация дат
    start_date = datetime.now() - timedelta(days=num_days)
    dates = [start_date + timedelta(days=i) for i in range(num_days)]
    
    # Генерация транзакций
    transactions = []
    
    for date in dates:
        # Количество транзакций в день (случайное)
        daily_transactions = np.random.poisson(50)
        
        for _ in range(daily_transactions):
            # Случайные параметры
            country = np.random.choice(countries)
            service = np.random.choice(services)
            consumer = np.random.choice(consumers)
            supplier = np.random.choice(suppliers)
            
            # Базовые цены (закупка и продажа)
            base_buy_price = np.random.uniform(0.01, 0.10)  # $0.01 - $0.10
            margin = np.random.uniform(0.10, 0.40)  # 10% - 40% маржа
            sell_price = base_buy_price * (1 + margin)
            
            # Количество
            quantity = np.random.poisson(5) + 1  # 1-20 штук
            
            # Прибыль
            profit = (sell_price - base_buy_price) * quantity
            
            transaction = {
                'dates': date,
                'consumerName': consumer,
                'producerName': supplier,
                'countryName': country,
                'webserviceName': service,
                'consumerAmount': round(sell_price, 4),
                'producerAmount': round(base_buy_price, 4),
                'all_orders': quantity,
                'Profit': round(profit, 4)
            }
            
            transactions.append(transaction)
    
    # Создание DataFrame
    df = pd.DataFrame(transactions)
    
    # Сортировка по дате
    df = df.sort_values('dates').reset_index(drop=True)
    
    # Сохранение
    output_file = os.path.join('data', 'sample_arbitration_data.csv')
    df.to_csv(output_file, index=False)
    
    print(f"✅ Создан файл с примерными данными: {output_file}")
    print(f"📊 Статистика:")
    print(f"   Всего транзакций: {len(df):,}")
    print(f"   Период: {df['dates'].min().strftime('%Y-%m-%d')} - {df['dates'].max().strftime('%Y-%m-%d')}")
    print(f"   Уникальных клиентов: {df['consumerName'].nunique()}")
    print(f"   Уникальных поставщиков: {df['producerName'].nunique()}")
    print(f"   Уникальных товаров: {df['countryName'].nunique() * df['webserviceName'].nunique()}")
    print(f"   Общая прибыль: ${df['Profit'].sum():,.2f}")
    print(f"   Средняя цена продажи: ${df['consumerAmount'].mean():.4f}")
    print(f"   Средняя цена закупки: ${df['producerAmount'].mean():.4f}")
    
    return df

if __name__ == "__main__":
    # Создаем папку data если её нет
    if not os.path.exists('data'):
        os.makedirs('data')
    
    create_sample_data()

