"""
Основной скрипт для еженедельного анализа и генерации рекомендаций по ценообразованию
"""

import pandas as pd
import numpy as np
from datetime import datetime
import os
import sys

from data_loader import DataLoader
from pricing_algorithm import PricingAlgorithm
from config import (
    DATA_FOLDER, OUTPUT_FOLDER, BACKUP_FOLDER,
    LOOKBACK_WEEKS, CURRENT_WEEK_DAYS,
    DATE_FORMAT
)

def main():
    """Основная функция для запуска анализа"""
    print("=" * 60)
    print("АНАЛИЗ АРБИТРАЖА - ЕЖЕНЕДЕЛЬНЫЕ РЕКОМЕНДАЦИИ")
    print("=" * 60)
    
    # Проверяем наличие папок
    for folder in [DATA_FOLDER, OUTPUT_FOLDER, BACKUP_FOLDER]:
        if not os.path.exists(folder):
            os.makedirs(folder)
            print(f"Создана папка: {folder}")
    
    # Инициализация
    loader = DataLoader()
    algorithm = PricingAlgorithm()
    
    try:
        # Поиск CSV файлов в папке data
        csv_files = [f for f in os.listdir(DATA_FOLDER) if f.endswith('.csv')]
        if not csv_files:
            print(f"❌ В папке {DATA_FOLDER} не найдено CSV файлов!")
            print("Поместите ваши CSV файлы в папку data/ и запустите скрипт снова.")
            return
        
        print(f"📁 Найдено CSV файлов: {len(csv_files)}")
        for file in csv_files:
            print(f"   - {file}")
        
        # Загружаем первый CSV файл (можно расширить для обработки нескольких файлов)
        main_file = csv_files[0]
        print(f"\n📊 Загружаем данные из {main_file}...")
        
        # Загрузка и подготовка данных
        df = loader.load_csv(main_file)
        df = loader.prepare_data()
        
        # Получение сводки по данным
        summary = loader.get_data_summary()
        print(f"\n📈 СВОДКА ПО ДАННЫМ:")
        print(f"   Всего строк: {summary['total_rows']:,}")
        print(f"   Период: {summary['date_range'][0].strftime(DATE_FORMAT)} - {summary['date_range'][1].strftime(DATE_FORMAT)}")
        print(f"   Уникальных клиентов: {summary['unique_consumers']}")
        print(f"   Уникальных поставщиков: {summary['unique_suppliers']}")
        print(f"   Уникальных товаров: {summary['unique_items']}")
        print(f"   Общая прибыль: ${summary['total_profit']:,.2f}")
        print(f"   Средняя цена продажи: ${summary['avg_sell_price']:.2f}")
        print(f"   Средняя цена закупки: ${summary['avg_buy_price']:.2f}")
        
        # Получение данных за текущую неделю
        print(f"\n📅 Анализируем данные за последнюю неделю...")
        weekly_data = loader.get_weekly_data(weeks_back=1)
        
        if weekly_data.empty:
            print("❌ Нет данных за последнюю неделю!")
            return
        
        # Получение исторических данных
        print(f"📚 Загружаем исторические данные за {LOOKBACK_WEEKS} недель...")
        historical_data = loader.get_historical_data(weeks_back=LOOKBACK_WEEKS)
        
        # Генерация рекомендаций
        print(f"\n🎯 Генерируем рекомендации...")
        recommendations = algorithm.generate_recommendations(weekly_data, historical_data)
        
        # Статистика по рекомендациям
        stats = algorithm.get_summary_stats()
        print(f"\n📊 СТАТИСТИКА РЕКОМЕНДАЦИЙ:")
        print(f"   Всего товаров: {stats['total_items']}")
        print(f"   Включить: {stats['enabled_items']}")
        print(f"   Отключить: {stats['disabled_items']}")
        print(f"   Средняя рекомендуемая цена: ${stats['avg_recommended_price']}")
        print(f"   Средняя целевая маржа: {stats['avg_target_margin']:.1%}")
        print(f"   Общая прибыль: ${stats['total_profit']:,.2f}")
        
        # Сохранение результатов
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(OUTPUT_FOLDER, f"weekly_pricing_recos_{timestamp}.csv")
        
        # Подготовка финального отчета
        final_report = recommendations.copy()
        
        # Добавляем человеко-читаемые названия
        if 'consumer_id' in final_report.columns:
            # Создаем маппинг ID -> название клиента
            consumer_mapping = df.groupby('consumer_id')['consumerName'].first().to_dict()
            final_report['consumer_name'] = final_report['consumer_id'].map(consumer_mapping)
        
        # Переупорядочиваем колонки для удобства
        columns_order = [
            'consumer_id', 'consumer_name', 'item_id', 'enabled', 'price_rec',
            'baseline_cost', 'target_margin', 'reason', 'reqs', 'sales',
            'reqs_hist', 'sales_hist', 'conversion_rate', 'conversion_rate_hist', 'profit'
        ]
        
        # Оставляем только существующие колонки
        existing_columns = [col for col in columns_order if col in final_report.columns]
        final_report = final_report[existing_columns]
        
        # Сохранение
        final_report.to_csv(output_file, index=False, encoding='utf-8')
        print(f"\n💾 Результаты сохранены в: {output_file}")
        
        # Создание резервной копии
        backup_file = os.path.join(BACKUP_FOLDER, f"backup_{timestamp}.csv")
        final_report.to_csv(backup_file, index=False, encoding='utf-8')
        print(f"💾 Резервная копия: {backup_file}")
        
        # Показываем топ-5 рекомендаций
        print(f"\n🏆 ТОП-5 РЕКОМЕНДАЦИЙ:")
        top_recommendations = final_report[final_report['enabled'] == True].nlargest(5, 'price_rec')
        for _, row in top_recommendations.iterrows():
            consumer_name = row.get('consumer_name', f"Client_{row['consumer_id']}")
            print(f"   {consumer_name} | {row['item_id']} | ${row['price_rec']} | {row['target_margin']:.1%} маржа")
        
        # Показываем товары для отключения
        disabled_items = final_report[final_report['enabled'] == False]
        if not disabled_items.empty:
            print(f"\n❌ ТОВАРЫ ДЛЯ ОТКЛЮЧЕНИЯ ({len(disabled_items)} шт.):")
            for reason in disabled_items['reason'].value_counts().items():
                print(f"   {reason[0]}: {reason[1]} товаров")
        
        print(f"\n✅ Анализ завершен успешно!")
        print(f"📁 Проверьте папку {OUTPUT_FOLDER} для результатов")
        
    except Exception as e:
        print(f"\n❌ ОШИБКА: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)

