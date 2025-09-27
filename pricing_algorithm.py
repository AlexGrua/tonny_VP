"""
Алгоритмы ценообразования на основе исторических данных
"""

import pandas as pd
import numpy as np
from config import (
    MIN_MARGIN, MAX_MARGIN, DEFAULT_MARGIN,
    STEP_DOWN_PCT, STEP_UP_PCT,
    MIN_REQS_TO_KEEP, NO_SALE_WEEKS_TO_DISABLE,
    HIGH_CONVERSION_THRESHOLD, LOW_CONVERSION_THRESHOLD,
    HIGH_DEMAND_THRESHOLD, LOW_DEMAND_THRESHOLD
)

class PricingAlgorithm:
    def __init__(self):
        self.recommendations = []
    
    def calculate_supplier_costs(self, historical_data):
        """Расчет закупочных цен поставщиков"""
        if historical_data.empty:
            return pd.DataFrame()
            
        supplier_costs = historical_data.groupby('item_id').agg({
            'producerAmount': [
                lambda x: np.nanmedian(x),  # медиана
                lambda x: np.nanpercentile(x, 10),  # 10-й перцентиль
                lambda x: np.nanpercentile(x, 90),  # 90-й перцентиль
                'count'  # количество котировок
            ]
        }).round(4)
        
        supplier_costs.columns = ['cost_p50', 'cost_p10', 'cost_p90', 'quotes_count']
        supplier_costs = supplier_costs.reset_index()
        
        return supplier_costs
    
    def calculate_consumer_metrics(self, weekly_data, historical_data):
        """Расчет метрик по клиентам"""
        if weekly_data.empty:
            return pd.DataFrame()
            
        # Агрегация за текущую неделю
        weekly_agg = weekly_data.groupby(['consumer_id', 'item_id']).agg({
            'consumerAmount': ['size', 'sum', lambda x: np.nanmedian(x), 'mean', 'last'],
            'all_orders': 'sum',
            'Profit': 'sum'
        }).round(4)
        
        weekly_agg.columns = ['reqs', 'total_sell_value', 'sell_p50', 'sell_pavg', 'last_price', 'sales', 'profit']
        weekly_agg = weekly_agg.reset_index()
        
        # Агрегация за исторический период
        if not historical_data.empty:
            hist_agg = historical_data.groupby(['consumer_id', 'item_id']).agg({
                'consumerAmount': ['size', 'sum', lambda x: np.nanmedian(x), 'mean'],
                'all_orders': 'sum',
                'Profit': 'sum'
            }).round(4)
            
            hist_agg.columns = ['reqs_hist', 'total_sell_value_hist', 'sell_p50_hist', 'sell_pavg_hist', 'sales_hist', 'profit_hist']
            hist_agg = hist_agg.reset_index()
            
            # Объединение данных
            consumer_metrics = weekly_agg.merge(hist_agg, on=['consumer_id', 'item_id'], how='left')
        else:
            consumer_metrics = weekly_agg
            # Добавляем пустые колонки для исторических данных
            for col in ['reqs_hist', 'total_sell_value_hist', 'sell_p50_hist', 'sell_pavg_hist', 'sales_hist', 'profit_hist']:
                consumer_metrics[col] = 0
        
        return consumer_metrics
    
    def calculate_conversion_rates(self, consumer_metrics):
        """Расчет конверсии"""
        consumer_metrics['conversion_rate'] = np.where(
            consumer_metrics['reqs'] > 0,
            consumer_metrics['sales'] / consumer_metrics['reqs'],
            0
        )
        
        consumer_metrics['conversion_rate_hist'] = np.where(
            consumer_metrics['reqs_hist'] > 0,
            consumer_metrics['sales_hist'] / consumer_metrics['reqs_hist'],
            0
        )
        
        return consumer_metrics
    
    def recommend_price_for_item(self, row, supplier_costs):
        """Рекомендация цены для конкретного товара и клиента"""
        item_id = row['item_id']
        consumer_id = row['consumer_id']
        
        # Получаем закупочную цену
        cost_data = supplier_costs[supplier_costs['item_id'] == item_id]
        if cost_data.empty:
            return {
                'enabled': False,
                'reason': 'no_supplier_cost',
                'price_rec': None,
                'baseline_cost': None,
                'target_margin': None
            }
        
        cost_p50 = cost_data.iloc[0]['cost_p50']
        if pd.isna(cost_p50) or cost_p50 <= 0:
            return {
                'enabled': False,
                'reason': 'invalid_cost',
                'price_rec': None,
                'baseline_cost': cost_p50,
                'target_margin': None
            }
        
        # Определяем базовую маржу
        if row['sales'] > 0 and not pd.isna(row['sell_p50']):
            # Если были продажи - используем историческую маржу
            hist_margin = (row['sell_p50'] - cost_p50) / max(cost_p50, 1e-6)
            target_margin = np.clip(hist_margin, MIN_MARGIN, MAX_MARGIN)
            baseline = cost_p50 * (1 + target_margin)
        elif row['reqs'] > 0 and row['sales'] == 0 and not pd.isna(row['last_price']):
            # Если были запросы, но нет продаж - снижаем цену
            baseline = row['last_price'] * (1 - STEP_DOWN_PCT)
            target_margin = (baseline - cost_p50) / max(cost_p50, 1e-6)
        else:
            # Используем маржу по умолчанию
            target_margin = DEFAULT_MARGIN
            baseline = cost_p50 * (1 + target_margin)
        
        # Проверяем условия для отключения товара
        no_sale_2w = (row['sales'] == 0) and ((row['sales_hist'] or 0) == 0)
        low_demand = (row['reqs'] + (row['reqs_hist'] or 0)) < MIN_REQS_TO_KEEP
        
        if no_sale_2w and low_demand:
            return {
                'enabled': False,
                'reason': 'no_sales_two_weeks',
                'price_rec': None,
                'baseline_cost': cost_p50,
                'target_margin': target_margin
            }
        
        # Корректировка цены на основе конверсии
        if row['conversion_rate'] > HIGH_CONVERSION_THRESHOLD:
            # Высокая конверсия - можно поднять цену
            baseline *= (1 + STEP_UP_PCT)
        elif row['conversion_rate'] < LOW_CONVERSION_THRESHOLD and row['reqs'] > 20:
            # Низкая конверсия при высоком спросе - снижаем цену
            baseline *= (1 - STEP_DOWN_PCT)
        
        return {
            'enabled': True,
            'reason': 'ok',
            'price_rec': round(float(baseline), 4),
            'baseline_cost': round(float(cost_p50), 4),
            'target_margin': round(float(target_margin), 4)
        }
    
    def generate_recommendations(self, weekly_data, historical_data):
        """Генерация рекомендаций по ценообразованию"""
        print("Генерируем рекомендации...")
        
        # Расчет закупочных цен
        supplier_costs = self.calculate_supplier_costs(historical_data)
        print(f"Обработано {len(supplier_costs)} товаров с данными поставщиков")
        
        # Расчет метрик клиентов
        consumer_metrics = self.calculate_consumer_metrics(weekly_data, historical_data)
        consumer_metrics = self.calculate_conversion_rates(consumer_metrics)
        print(f"Обработано {len(consumer_metrics)} комбинаций клиент-товар")
        
        # Генерация рекомендаций
        recommendations = []
        for _, row in consumer_metrics.iterrows():
            rec = self.recommend_price_for_item(row, supplier_costs)
            
            recommendation = {
                'consumer_id': row['consumer_id'],
                'item_id': row['item_id'],
                'enabled': rec['enabled'],
                'price_rec': rec['price_rec'],
                'baseline_cost': rec['baseline_cost'],
                'target_margin': rec['target_margin'],
                'reason': rec['reason'],
                'reqs': row['reqs'],
                'sales': row['sales'],
                'reqs_hist': row.get('reqs_hist', 0),
                'sales_hist': row.get('sales_hist', 0),
                'conversion_rate': row['conversion_rate'],
                'conversion_rate_hist': row.get('conversion_rate_hist', 0),
                'profit': row['profit']
            }
            recommendations.append(recommendation)
        
        self.recommendations = pd.DataFrame(recommendations)
        return self.recommendations
    
    def get_summary_stats(self):
        """Получение сводной статистики по рекомендациям"""
        if self.recommendations.empty:
            return {}
        
        total_items = len(self.recommendations)
        enabled_items = len(self.recommendations[self.recommendations['enabled'] == True])
        disabled_items = total_items - enabled_items
        
        avg_price = self.recommendations[self.recommendations['enabled'] == True]['price_rec'].mean()
        avg_margin = self.recommendations[self.recommendations['enabled'] == True]['target_margin'].mean()
        
        return {
            'total_items': total_items,
            'enabled_items': enabled_items,
            'disabled_items': disabled_items,
            'avg_recommended_price': round(avg_price, 4) if not pd.isna(avg_price) else 0,
            'avg_target_margin': round(avg_margin, 4) if not pd.isna(avg_margin) else 0,
            'total_profit': self.recommendations['profit'].sum()
        }

