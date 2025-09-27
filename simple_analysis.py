"""
Упрощенный анализ данных без внешних зависимостей
Работает только с встроенными библиотеками Python
"""

import csv
import os
from datetime import datetime, timedelta
from collections import defaultdict, Counter

def load_data(filename):
    """Загрузка данных из CSV файла"""
    data = []
    print(f"Загружаем данные из {filename}...")
    
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    
    print(f"Загружено {len(data)} строк")
    return data

def analyze_data(data):
    """Анализ данных"""
    print("\nАнализируем данные...")
    
    # Статистика по данным
    total_rows = len(data)
    unique_consumers = len(set(row.get('consumerName', '') for row in data))
    unique_suppliers = len(set(row.get('producerName', '') for row in data))
    unique_countries = len(set(row.get('countryName', '') for row in data))
    unique_services = len(set(row.get('webserviceName', '') for row in data))
    
    # Анализ цен
    sell_prices = []
    buy_prices = []
    profits = []
    
    for row in data:
        try:
            sell_price = float(row.get('consumerAmount', 0))
            buy_price = float(row.get('producerAmount', 0))
            profit = float(row.get('Profit', 0))
            
            if sell_price > 0:
                sell_prices.append(sell_price)
            if buy_price > 0:
                buy_prices.append(buy_price)
            if profit != 0:
                profits.append(profit)
        except (ValueError, TypeError):
            continue
    
    # Расчет статистики
    avg_sell_price = sum(sell_prices) / len(sell_prices) if sell_prices else 0
    avg_buy_price = sum(buy_prices) / len(buy_prices) if buy_prices else 0
    total_profit = sum(profits)
    
    # Анализ по товарам (страна + сервис)
    item_stats = defaultdict(lambda: {
        'requests': 0,
        'sales': 0,
        'total_profit': 0,
        'sell_prices': [],
        'buy_prices': []
    })
    
    for row in data:
        country = row.get('countryName', '').strip().upper()
        service = row.get('webserviceName', '').strip().upper()
        item_id = f"{country} | {service}"
        
        try:
            sell_price = float(row.get('consumerAmount', 0))
            buy_price = float(row.get('producerAmount', 0))
            quantity = int(row.get('all_orders', 0))
            profit = float(row.get('Profit', 0))
            
            item_stats[item_id]['requests'] += 1
            item_stats[item_id]['sales'] += quantity
            item_stats[item_id]['total_profit'] += profit
            
            if sell_price > 0:
                item_stats[item_id]['sell_prices'].append(sell_price)
            if buy_price > 0:
                item_stats[item_id]['buy_prices'].append(buy_price)
                
        except (ValueError, TypeError):
            continue
    
    return {
        'total_rows': total_rows,
        'unique_consumers': unique_consumers,
        'unique_suppliers': unique_suppliers,
        'unique_countries': unique_countries,
        'unique_services': unique_services,
        'avg_sell_price': avg_sell_price,
        'avg_buy_price': avg_buy_price,
        'total_profit': total_profit,
        'item_stats': dict(item_stats)
    }

def generate_recommendations(stats):
    """Генерация рекомендаций"""
    print("\nГенерируем рекомендации...")
    
    recommendations = []
    
    for item_id, item_data in stats['item_stats'].items():
        if not item_data['sell_prices'] or not item_data['buy_prices']:
            continue
            
        # Расчет средней цены продажи и закупки
        avg_sell = sum(item_data['sell_prices']) / len(item_data['sell_prices'])
        avg_buy = sum(item_data['buy_prices']) / len(item_data['buy_prices'])
        
        # Расчет конверсии
        conversion_rate = item_data['sales'] / max(item_data['requests'], 1)
        
        # Рекомендация цены (базовая логика)
        if conversion_rate > 0.1:  # Высокая конверсия
            recommended_price = avg_buy * 1.25  # 25% маржа
            enabled = True
            reason = "high_conversion"
        elif conversion_rate > 0.05:  # Средняя конверсия
            recommended_price = avg_buy * 1.15  # 15% маржа
            enabled = True
            reason = "medium_conversion"
        elif item_data['requests'] > 10:  # Есть спрос, но низкая конверсия
            recommended_price = avg_buy * 1.05  # 5% маржа
            enabled = True
            reason = "low_conversion_high_demand"
        else:  # Нет спроса
            recommended_price = 0
            enabled = False
            reason = "no_demand"
        
        recommendations.append({
            'item_id': item_id,
            'enabled': enabled,
            'recommended_price': round(recommended_price, 4),
            'avg_buy_price': round(avg_buy, 4),
            'avg_sell_price': round(avg_sell, 4),
            'conversion_rate': round(conversion_rate, 4),
            'requests': item_data['requests'],
            'sales': item_data['sales'],
            'total_profit': round(item_data['total_profit'], 2),
            'reason': reason
        })
    
    return recommendations

def save_results(stats, recommendations):
    """Сохранение результатов"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Создаем папку output если её нет
    if not os.path.exists('output'):
        os.makedirs('output')
    
    # Сохраняем рекомендации
    output_file = f'output/simple_recommendations_{timestamp}.csv'
    with open(output_file, 'w', newline='', encoding='utf-8') as file:
        if recommendations:
            writer = csv.DictWriter(file, fieldnames=recommendations[0].keys())
            writer.writeheader()
            writer.writerows(recommendations)
    
    # Сохраняем отчет
    report_file = f'output/simple_report_{timestamp}.txt'
    with open(report_file, 'w', encoding='utf-8') as file:
        file.write("ОТЧЕТ ПО АНАЛИЗУ АРБИТРАЖА\n")
        file.write("=" * 50 + "\n\n")
        
        file.write(f"Дата анализа: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        file.write("ОБЩАЯ СТАТИСТИКА:\n")
        file.write(f"  Всего транзакций: {stats['total_rows']:,}\n")
        file.write(f"  Уникальных клиентов: {stats['unique_consumers']}\n")
        file.write(f"  Уникальных поставщиков: {stats['unique_suppliers']}\n")
        file.write(f"  Уникальных стран: {stats['unique_countries']}\n")
        file.write(f"  Уникальных сервисов: {stats['unique_services']}\n")
        file.write(f"  Средняя цена продажи: ${stats['avg_sell_price']:.4f}\n")
        file.write(f"  Средняя цена закупки: ${stats['avg_buy_price']:.4f}\n")
        file.write(f"  Общая прибыль: ${stats['total_profit']:,.2f}\n\n")
        
        file.write("РЕКОМЕНДАЦИИ:\n")
        enabled_count = sum(1 for r in recommendations if r['enabled'])
        disabled_count = len(recommendations) - enabled_count
        
        file.write(f"  Всего товаров: {len(recommendations)}\n")
        file.write(f"  Рекомендуется включить: {enabled_count}\n")
        file.write(f"  Рекомендуется отключить: {disabled_count}\n\n")
        
        # Топ-10 товаров по прибыли
        top_items = sorted(recommendations, key=lambda x: x['total_profit'], reverse=True)[:10]
        file.write("ТОП-10 ТОВАРОВ ПО ПРИБЫЛИ:\n")
        for i, item in enumerate(top_items, 1):
            file.write(f"  {i:2d}. {item['item_id']} | ${item['recommended_price']:.4f} | ${item['total_profit']:.2f}\n")
    
    print(f"\nРезультаты сохранены:")
    print(f"  Рекомендации: {output_file}")
    print(f"  Отчет: {report_file}")
    
    return output_file, report_file

def main():
    """Основная функция"""
    print("=" * 60)
    print("УПРОЩЕННЫЙ АНАЛИЗ АРБИТРАЖА")
    print("=" * 60)
    
    # Поиск CSV файлов
    csv_files = [f for f in os.listdir('data') if f.endswith('.csv')]
    if not csv_files:
        print("❌ В папке data/ не найдено CSV файлов!")
        return
    
    print(f"📁 Найден файл: {csv_files[0]}")
    
    try:
        # Загрузка данных
        data = load_data(os.path.join('data', csv_files[0]))
        
        # Анализ
        stats = analyze_data(data)
        
        # Генерация рекомендаций
        recommendations = generate_recommendations(stats)
        
        # Сохранение результатов
        save_results(stats, recommendations)
        
        # Вывод сводки
        print(f"\n📊 СВОДКА:")
        print(f"  Всего транзакций: {stats['total_rows']:,}")
        print(f"  Уникальных клиентов: {stats['unique_consumers']}")
        print(f"  Уникальных товаров: {len(stats['item_stats'])}")
        print(f"  Общая прибыль: ${stats['total_profit']:,.2f}")
        
        enabled_count = sum(1 for r in recommendations if r['enabled'])
        print(f"  Рекомендуется включить: {enabled_count}")
        print(f"  Рекомендуется отключить: {len(recommendations) - enabled_count}")
        
        print(f"\n✅ Анализ завершен успешно!")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()