"""
Módulo de Métricas y Estadísticas
Decisión humana: Definir qué métricas son relevantes
"""

from typing import Dict, List
from collections import Counter
from datetime import datetime

class MetricsCalculator:
    """
    Calcula métricas a partir de transacciones normalizadas
    """
    
    def __init__(self):
        self.metrics = {}
    
    def calculate_metrics(self, transactions: List[Dict]) -> Dict:
        """
        Calcula métricas completas
        """
        if not transactions:
            return {
                'total': 0,
                'by_status': {},
                'by_currency': {},
                'by_source': {},
                'total_amount_by_currency': {},
                'date_range': None,
                'average_amount': 0,
                'median_amount': 0,
                'min_amount': 0,
                'max_amount': 0
            }
        
        # Métricas básicas
        total = len(transactions)
        
        # Distribución por estado
        status_count = Counter([tx.get('status', 'UNKNOWN') for tx in transactions])
        
        # Distribución por moneda
        currency_count = Counter([tx.get('currency', 'UNKNOWN') for tx in transactions])
        
        # Distribución por fuente
        source_count = Counter([tx.get('source', 'UNKNOWN') for tx in transactions])
        
        # Montos por moneda
        amount_by_currency = {}
        for tx in transactions:
            currency = tx.get('currency', 'UNKNOWN')
            amount = tx.get('amount', 0)
            if currency not in amount_by_currency:
                amount_by_currency[currency] = []
            amount_by_currency[currency].append(amount)
        
        total_amount_by_currency = {
            currency: sum(amounts) 
            for currency, amounts in amount_by_currency.items()
        }
        
        # Rango de fechas
        dates = []
        for tx in transactions:
            timestamp = tx.get('timestamp')
            if timestamp:
                try:
                    # Decisión humana: Manejar formato ISO-8601
                    date_obj = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                    dates.append(date_obj)
                except:
                    continue
        
        date_range = None
        if dates:
            date_range = {
                'min': min(dates).strftime('%Y-%m-%d %H:%M:%S'),
                'max': max(dates).strftime('%Y-%m-%d %H:%M:%S')
            }
        
        # Estadísticas de montos
        all_amounts = [tx.get('amount', 0) for tx in transactions]
        if all_amounts:
            all_amounts_sorted = sorted(all_amounts)
            
            # Cálculo de mediana
            n = len(all_amounts_sorted)
            if n % 2 == 0:
                median = (all_amounts_sorted[n//2 - 1] + all_amounts_sorted[n//2]) / 2
            else:
                median = all_amounts_sorted[n//2]
            
            avg_amount = sum(all_amounts) / len(all_amounts)
            min_amount = min(all_amounts)
            max_amount = max(all_amounts)
        else:
            avg_amount = 0
            median = 0
            min_amount = 0
            max_amount = 0
        
        # Calcular calidad de datos
        # Decisión humana: Asumir que todos los campos relevantes están presentes
        complete_records = 0
        for tx in transactions:
            if all(key in tx and tx[key] for key in ['id', 'amount', 'currency', 'timestamp', 'status']):
                complete_records += 1
        
        data_quality = (complete_records / total * 100) if total > 0 else 0
        
        return {
            'total': total,
            'by_status': dict(status_count),
            'by_currency': dict(currency_count),
            'by_source': dict(source_count),
            'total_amount_by_currency': total_amount_by_currency,
            'date_range': date_range,
            'average_amount': round(avg_amount, 2),
            'median_amount': round(median, 2),
            'min_amount': round(min_amount, 2),
            'max_amount': round(max_amount, 2),
            'data_quality': round(data_quality, 2),
            'complete_records': complete_records
        }
    
    def get_summary(self, metrics: Dict) -> str:
        """
        Genera un resumen legible de las métricas
        """
        lines = []
        lines.append("="*60)
        lines.append("📊 RESUMEN DE MÉTRICAS")
        lines.append("="*60)
        lines.append(f"📝 Total de transacciones: {metrics['total']}")
        lines.append("")
        
        lines.append("📈 Distribución por estado:")
        for status, count in metrics['by_status'].items():
            percentage = (count / metrics['total'] * 100) if metrics['total'] > 0 else 0
            bar = '█' * int(percentage / 2)
            lines.append(f"  • {status:<10}: {count:>4} ({percentage:>5.1f}%) {bar}")
        lines.append("")
        
        lines.append("💰 Distribución por moneda:")
        for currency, count in metrics['by_currency'].items():
            percentage = (count / metrics['total'] * 100) if metrics['total'] > 0 else 0
            lines.append(f"  • {currency:<5}: {count:>4} ({percentage:>5.1f}%)")
        lines.append("")
        
        lines.append("📊 Montos totales por moneda:")
        for currency, amount in metrics['total_amount_by_currency'].items():
            lines.append(f"  • {currency}: {amount:,.2f}")
        lines.append("")
        
        lines.append("📅 Rango de fechas:")
        if metrics['date_range']:
            lines.append(f"  • Desde: {metrics['date_range']['min']}")
            lines.append(f"  • Hasta: {metrics['date_range']['max']}")
        else:
            lines.append("  • No disponible")
        lines.append("")
        
        lines.append("📊 Estadísticas de montos:")
        lines.append(f"  • Promedio: {metrics['average_amount']:,.2f}")
        lines.append(f"  • Mediana:  {metrics['median_amount']:,.2f}")
        lines.append(f"  • Mínimo:   {metrics['min_amount']:,.2f}")
        lines.append(f"  • Máximo:   {metrics['max_amount']:,.2f}")
        lines.append("")
        
        lines.append("✅ Calidad de datos:")
        lines.append(f"  • Registros completos: {metrics['complete_records']} de {metrics['total']}")
        lines.append(f"  • Porcentaje: {metrics['data_quality']}%")
        
        if metrics['data_quality'] >= 90:
            lines.append("  🏆 Excelente calidad de datos!")
        elif metrics['data_quality'] >= 70:
            lines.append("  👍 Buena calidad de datos")
        elif metrics['data_quality'] >= 50:
            lines.append("  ⚠️ Calidad regular - Revisar datos incompletos")
        else:
            lines.append("  🚨 Calidad baja - Muchos datos incompletos")
        
        lines.append("="*60)
        
        return "\n".join(lines)
