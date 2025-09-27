"""
Скрипт для визуализации результатов анализа
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from datetime import datetime

def visualize_pricing_results(csv_file=None):
    """Визуализация результатов ценообразования"""
    
    # Поиск последнего файла результатов
    if csv_file is None:
        output_files = [f for f in os.listdir('output') if f.startswith('weekly_pricing_recos_') and f.endswith('.csv')]
        if not output_files:
            print("❌ Не найдено файлов результатов в папке output/")
            return
        
        csv_file = os.path.join('output', sorted(output_files)[-1])
    
    print(f"📊 Загружаем результаты из {csv_file}")
    df = pd.read_csv(csv_file)
    
    # Настройка стиля
    plt.style.use('default')
    sns.set_palette("husl")
    
    # Создание фигуры с несколькими графиками
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    fig.suptitle('Анализ рекомендаций по ценообразованию', fontsize=16, fontweight='bold')
    
    # 1. Распределение рекомендуемых цен
    enabled_data = df[df['enabled'] == True]
    if not enabled_data.empty:
        axes[0, 0].hist(enabled_data['price_rec'], bins=30, alpha=0.7, color='skyblue', edgecolor='black')
        axes[0, 0].set_title('Распределение рекомендуемых цен')
        axes[0, 0].set_xlabel('Цена ($)')
        axes[0, 0].set_ylabel('Количество')
        axes[0, 0].grid(True, alpha=0.3)
    
    # 2. Распределение маржи
    if not enabled_data.empty:
        axes[0, 1].hist(enabled_data['target_margin'] * 100, bins=30, alpha=0.7, color='lightgreen', edgecolor='black')
        axes[0, 1].set_title('Распределение целевой маржи')
        axes[0, 1].set_xlabel('Маржа (%)')
        axes[0, 1].set_ylabel('Количество')
        axes[0, 1].grid(True, alpha=0.3)
    
    # 3. Статус товаров (включено/отключено)
    status_counts = df['enabled'].value_counts()
    colors = ['lightcoral', 'lightgreen']
    axes[0, 2].pie(status_counts.values, labels=['Отключено', 'Включено'], 
                   autopct='%1.1f%%', colors=colors, startangle=90)
    axes[0, 2].set_title('Статус товаров')
    
    # 4. Конверсия vs Цена
    if not enabled_data.empty:
        scatter = axes[1, 0].scatter(enabled_data['conversion_rate'] * 100, 
                                   enabled_data['price_rec'], 
                                   c=enabled_data['target_margin'] * 100, 
                                   cmap='viridis', alpha=0.6)
        axes[1, 0].set_title('Конверсия vs Цена')
        axes[1, 0].set_xlabel('Конверсия (%)')
        axes[1, 0].set_ylabel('Цена ($)')
        axes[1, 0].grid(True, alpha=0.3)
        
        # Добавляем цветовую шкалу
        cbar = plt.colorbar(scatter, ax=axes[1, 0])
        cbar.set_label('Маржа (%)')
    
    # 5. Топ-10 товаров по цене
    if not enabled_data.empty:
        top_items = enabled_data.nlargest(10, 'price_rec')
        axes[1, 1].barh(range(len(top_items)), top_items['price_rec'], color='orange', alpha=0.7)
        axes[1, 1].set_title('Топ-10 товаров по цене')
        axes[1, 1].set_xlabel('Цена ($)')
        axes[1, 1].set_yticks(range(len(top_items)))
        axes[1, 1].set_yticklabels([f"{row['item_id'][:20]}..." for _, row in top_items.iterrows()], fontsize=8)
        axes[1, 1].grid(True, alpha=0.3)
    
    # 6. Причины отключения товаров
    disabled_data = df[df['enabled'] == False]
    if not disabled_data.empty:
        reason_counts = disabled_data['reason'].value_counts()
        axes[1, 2].bar(range(len(reason_counts)), reason_counts.values, color='lightcoral', alpha=0.7)
        axes[1, 2].set_title('Причины отключения товаров')
        axes[1, 2].set_xlabel('Причина')
        axes[1, 2].set_ylabel('Количество')
        axes[1, 2].set_xticks(range(len(reason_counts)))
        axes[1, 2].set_xticklabels(reason_counts.index, rotation=45, ha='right', fontsize=8)
        axes[1, 2].grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    # Сохранение графика
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join('output', f'pricing_analysis_{timestamp}.png')
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"📊 График сохранен: {output_file}")
    
    # Показываем график
    plt.show()
    
    # Выводим сводную статистику
    print(f"\n📈 СВОДНАЯ СТАТИСТИКА:")
    print(f"   Всего товаров: {len(df)}")
    print(f"   Включено: {len(enabled_data)} ({len(enabled_data)/len(df)*100:.1f}%)")
    print(f"   Отключено: {len(disabled_data)} ({len(disabled_data)/len(df)*100:.1f}%)")
    
    if not enabled_data.empty:
        print(f"   Средняя рекомендуемая цена: ${enabled_data['price_rec'].mean():.4f}")
        print(f"   Медианная рекомендуемая цена: ${enabled_data['price_rec'].median():.4f}")
        print(f"   Средняя маржа: {enabled_data['target_margin'].mean()*100:.1f}%")
        print(f"   Медианная маржа: {enabled_data['target_margin'].median()*100:.1f}%")
        print(f"   Общая прибыль: ${enabled_data['profit'].sum():,.2f}")

def create_summary_report(csv_file=None):
    """Создание текстового отчета"""
    
    # Поиск последнего файла результатов
    if csv_file is None:
        output_files = [f for f in os.listdir('output') if f.startswith('weekly_pricing_recos_') and f.endswith('.csv')]
        if not output_files:
            print("❌ Не найдено файлов результатов в папке output/")
            return
        
        csv_file = os.path.join('output', sorted(output_files)[-1])
    
    df = pd.read_csv(csv_file)
    
    # Создание отчета
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = os.path.join('output', f'summary_report_{timestamp}.txt')
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("ОТЧЕТ ПО АНАЛИЗУ ЦЕНООБРАЗОВАНИЯ\n")
        f.write("=" * 50 + "\n\n")
        
        f.write(f"Дата создания отчета: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Источник данных: {csv_file}\n\n")
        
        # Общая статистика
        enabled_data = df[df['enabled'] == True]
        disabled_data = df[df['enabled'] == False]
        
        f.write("ОБЩАЯ СТАТИСТИКА:\n")
        f.write(f"  Всего товаров: {len(df)}\n")
        f.write(f"  Включено: {len(enabled_data)} ({len(enabled_data)/len(df)*100:.1f}%)\n")
        f.write(f"  Отключено: {len(disabled_data)} ({len(disabled_data)/len(df)*100:.1f}%)\n\n")
        
        if not enabled_data.empty:
            f.write("СТАТИСТИКА ПО ВКЛЮЧЕННЫМ ТОВАРАМ:\n")
            f.write(f"  Средняя рекомендуемая цена: ${enabled_data['price_rec'].mean():.4f}\n")
            f.write(f"  Медианная рекомендуемая цена: ${enabled_data['price_rec'].median():.4f}\n")
            f.write(f"  Минимальная цена: ${enabled_data['price_rec'].min():.4f}\n")
            f.write(f"  Максимальная цена: ${enabled_data['price_rec'].max():.4f}\n")
            f.write(f"  Средняя маржа: {enabled_data['target_margin'].mean()*100:.1f}%\n")
            f.write(f"  Медианная маржа: {enabled_data['target_margin'].median()*100:.1f}%\n")
            f.write(f"  Общая прибыль: ${enabled_data['profit'].sum():,.2f}\n\n")
        
        # Причины отключения
        if not disabled_data.empty:
            f.write("ПРИЧИНЫ ОТКЛЮЧЕНИЯ ТОВАРОВ:\n")
            reason_counts = disabled_data['reason'].value_counts()
            for reason, count in reason_counts.items():
                f.write(f"  {reason}: {count} товаров\n")
            f.write("\n")
        
        # Топ товары
        if not enabled_data.empty:
            f.write("ТОП-10 ТОВАРОВ ПО ЦЕНЕ:\n")
            top_items = enabled_data.nlargest(10, 'price_rec')
            for i, (_, row) in enumerate(top_items.iterrows(), 1):
                consumer_name = row.get('consumer_name', f"Client_{row['consumer_id']}")
                f.write(f"  {i:2d}. {consumer_name} | {row['item_id']} | ${row['price_rec']:.4f} | {row['target_margin']*100:.1f}%\n")
    
    print(f"📄 Отчет сохранен: {report_file}")

if __name__ == "__main__":
    # Проверяем наличие папки output
    if not os.path.exists('output'):
        print("❌ Папка output/ не найдена. Сначала запустите weekly_pricing.py")
        exit(1)
    
    # Визуализация
    visualize_pricing_results()
    
    # Создание отчета
    create_summary_report()

