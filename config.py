"""
Конфигурация параметров для алгоритма ценообразования
"""

# Параметры маржи
MIN_MARGIN = 0.10  # 10% минимальная маржа
MAX_MARGIN = 0.45  # 45% максимальная маржа
DEFAULT_MARGIN = 0.15  # 15% маржа по умолчанию

# Параметры корректировки цен
STEP_DOWN_PCT = 0.05  # 5% шаг вниз при отсутствии продаж
STEP_UP_PCT = 0.03    # 3% шаг вверх при высокой конверсии

# Параметры для отключения товаров
MIN_REQS_TO_KEEP = 10  # Минимум запросов для сохранения товара
NO_SALE_WEEKS_TO_DISABLE = 2  # Недель без продаж для отключения
MIN_CONVERSION_RATE = 0.01  # 1% минимальная конверсия

# Параметры анализа
LOOKBACK_WEEKS = 8  # Недель истории для анализа
CURRENT_WEEK_DAYS = 7  # Дней в текущей неделе

# Пороги для принятия решений
HIGH_CONVERSION_THRESHOLD = 0.15  # 15% высокая конверсия
LOW_CONVERSION_THRESHOLD = 0.05   # 5% низкая конверсия
HIGH_DEMAND_THRESHOLD = 100       # Высокий спрос (запросов в неделю)
LOW_DEMAND_THRESHOLD = 5          # Низкий спрос

# Настройки файлов
DATA_FOLDER = "data"
OUTPUT_FOLDER = "output"
BACKUP_FOLDER = "backup"

# Форматы дат
DATE_FORMAT = "%Y-%m-%d"
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

# Названия колонок в CSV (адаптируйте под ваши данные)
COLUMN_MAPPING = {
    'date': 'dates',
    'consumer': 'consumerName', 
    'supplier': 'producerName',
    'country': 'countryName',
    'service': 'webserviceName',
    'sell_price': 'consumerAmount',
    'buy_price': 'producerAmount',
    'quantity': 'all_orders',

}

