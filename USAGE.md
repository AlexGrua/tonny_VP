# Инструкция по использованию

## Быстрый старт

### 1. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 2. Подготовка данных
Поместите ваши CSV файлы в папку `data/`. Ожидаемые колонки:
- `dates` - дата транзакции
- `consumerName` - имя покупателя  
- `producerName` - имя поставщика
- `countryName` - страна
- `webserviceName` - сервис
- `consumerAmount` - цена продажи
- `producerAmount` - цена закупки
- `all_orders` - количество
- `Profit` - прибыль

### 3. Создание тестовых данных (опционально)
```bash
python create_sample_data.py
```

### 4. Запуск анализа
```bash
python weekly_pricing.py
```

### 5. Просмотр результатов
```bash
python visualize_results.py
```

## Структура проекта

```
arbitration_pricing_analysis/
├── data/                    # Исходные CSV файлы
├── output/                  # Результаты анализа
├── backup/                  # Резервные копии
├── config.py               # Конфигурация параметров
├── data_loader.py          # Загрузка и подготовка данных
├── pricing_algorithm.py    # Алгоритмы ценообразования
├── weekly_pricing.py       # Основной скрипт анализа
├── visualize_results.py    # Визуализация результатов
├── create_sample_data.py   # Создание тестовых данных
└── requirements.txt        # Зависимости Python
```

## Настройка параметров

Отредактируйте файл `config.py` для изменения параметров:

- `MIN_MARGIN` / `MAX_MARGIN` - минимальная и максимальная маржа
- `STEP_DOWN_PCT` - процент снижения цены при отсутствии продаж
- `MIN_REQS_TO_KEEP` - минимум запросов для сохранения товара
- `NO_SALE_WEEKS_TO_DISABLE` - недель без продаж для отключения

## Результаты

После запуска анализа в папке `output/` появятся файлы:

- `weekly_pricing_recos_YYYYMMDD_HHMMSS.csv` - рекомендации по ценам
- `pricing_analysis_YYYYMMDD_HHMMSS.png` - графики анализа
- `summary_report_YYYYMMDD_HHMMSS.txt` - текстовый отчет

## Формат результатов

CSV файл с рекомендациями содержит:
- `consumer_id` / `consumer_name` - ID и имя клиента
- `item_id` - товар (страна | сервис)
- `enabled` - включить/отключить товар
- `price_rec` - рекомендуемая цена
- `baseline_cost` - базовая себестоимость
- `target_margin` - целевая маржа
- `reason` - причина решения
- `reqs` / `sales` - запросы и продажи за неделю
- `conversion_rate` - конверсия
- `profit` - прибыль

## Автоматизация

Для еженедельного запуска создайте bat-файл (Windows) или cron-задачу (Linux):

**Windows (weekly_analysis.bat):**
```batch
@echo off
cd /d "D:\arbitration_pricing_analysis"
python weekly_pricing.py
python visualize_results.py
```

**Linux (crontab):**
```bash
0 9 * * 1 cd /path/to/arbitration_pricing_analysis && python weekly_pricing.py
```

## Поддержка

При возникновении проблем:
1. Проверьте формат CSV файлов
2. Убедитесь, что все зависимости установлены
3. Проверьте логи в консоли
4. Адаптируйте `COLUMN_MAPPING` в `config.py` под ваши данные

