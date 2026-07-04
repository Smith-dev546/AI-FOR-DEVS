"""
Módulo de Normalización de Transacciones
Decisión humana: Definir las reglas de mapeo y transformación
"""

import json
import re
from datetime import datetime
from typing import Dict, Any, Optional, List
import yaml
from pathlib import Path

class TransactionNormalizer:
    """
    Clase encargada de normalizar transacciones de diferentes fuentes
    IA ayudó con: Sugerencia de estructura de clases y métodos
    Decisión humana: Reglas de transformación específicas
    """
    
    def __init__(self, config_path: str = "data/config.yaml"):
        """
        Inicializa el normalizador con la configuración
        """
        self.config = self._load_config(config_path)
        self.normalized_transactions = []
        self.invalid_transactions = []
        self.source_detection_rules = self._build_source_rules()
        
    def _load_config(self, config_path: str) -> Dict:
        """Carga la configuración desde archivo YAML"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            # Decisión humana: Configuración por defecto si no existe archivo
            return self._default_config()
    
    def _default_config(self) -> Dict:
        """Configuración por defecto - Decisión humana"""
        return {
            'currency_mapping': {
                'usd': 'USD', 'eur': 'EUR', 'gbp': 'GBP',
                '€': 'EUR', '$': 'USD', '£': 'GBP'
            },
            'status_mapping': {
                'completed': 'SUCCESS', 'ok': 'SUCCESS', 'success': 'SUCCESS',
                'failed': 'FAILED', 'error': 'FAILED',
                'pending': 'PENDING', 'processing': 'PENDING'
            },
            'date_formats': [
                "%Y-%m-%d %H:%M:%S",
                "%d/%m/%Y %H:%M",
                "%Y-%m-%dT%H:%M:%SZ",
                "%Y-%m-%d"
            ],
            'sources': {
                'source_a': {
                    'id_field': 'id', 'amount_field': 'amount',
                    'currency_field': 'currency', 'date_field': 'timestamp',
                    'status_field': 'status'
                },
                'source_b': {
                    'id_field': 'transaction_id', 'amount_field': 'total',
                    'currency_field': 'currency_code', 'date_field': 'created_at',
                    'status_field': 'state'
                },
                'source_c': {
                    'id_field': 'ref', 'amount_field': 'amount',
                    'currency_field': 'currency', 'date_field': 'date',
                    'status_field': 'result'
                }
            }
        }
    
    def _build_source_rules(self) -> Dict:
        """Construye reglas para detectar la fuente basado en campos"""
        rules = {}
        for source, fields in self.config['sources'].items():
            rules[source] = set(fields.values())
        return rules
    
    def detect_source(self, transaction: Dict) -> Optional[str]:
        """
        Detecta la fuente de la transacción basado en sus campos
        Decisión humana: Usar coincidencia de campos para identificar fuente
        """
        transaction_keys = set(transaction.keys())
        best_match = None
        max_matches = 0
        
        for source, required_fields in self.source_detection_rules.items():
            matches = len(transaction_keys.intersection(required_fields))
            if matches >= 2 and matches > max_matches:
                max_matches = matches
                best_match = source
        
        return best_match
    
    def parse_amount(self, amount: Any, source_type: str) -> Optional[float]:
        """
        Convierte el monto a float según el formato de origen
        IA sugirió: Uso de expresiones regulares
        Decisión humana: Reglas específicas por tipo de formato
        """
        if amount is None:
            return None
        
        if isinstance(amount, (int, float)):
            # source_b usa centavos
            if source_type == 'integer_cents':
                return float(amount) / 100
            return float(amount)
        
        if isinstance(amount, str):
            # Limpiar y convertir
            amount_clean = amount.strip()
            
            # Decisión humana: Manejar formato europeo (€99,99)
            if source_type == 'euro_format' or ',' in amount_clean:
                # Reemplazar coma por punto para decimales
                amount_clean = amount_clean.replace(',', '.')
                # Eliminar símbolos de moneda
                amount_clean = re.sub(r'[^\d.]', '', amount_clean)
            
            # Eliminar símbolos de moneda
            amount_clean = re.sub(r'[^0-9.]', '', amount_clean)
            
            try:
                return float(amount_clean)
            except ValueError:
                return None
        
        return None
    
    def parse_currency(self, currency: Any) -> Optional[str]:
        """
        Normaliza el código de moneda
        Decisión humana: Mapeo de códigos y símbolos a ISO 4217
        """
        if not currency:
            return None
        
        if isinstance(currency, str):
            currency_clean = currency.strip().upper()
            
            # Verificar si está en el mapeo
            if currency_clean in self.config['currency_mapping']:
                return self.config['currency_mapping'][currency_clean]
            
            # Verificar si ya es un código ISO válido
            if currency_clean in self.config['currency_mapping'].values():
                return currency_clean
            
            # Decisión humana: Si no se reconoce, asumir USD
            return 'USD'
        
        return None
    
    def parse_date(self, date_str: Any) -> Optional[str]:
        """
        Convierte fecha a formato ISO-8601
        IA sugirió: Probar múltiples formatos
        Decisión humana: Orden de formatos y manejo de errores
        """
        if not date_str:
            return None
        
        if isinstance(date_str, str):
            for fmt in self.config['date_formats']:
                try:
                    date_obj = datetime.strptime(date_str.strip(), fmt)
                    return date_obj.strftime('%Y-%m-%dT%H:%M:%SZ')
                except ValueError:
                    continue
            
            # Decisión humana: Intentar limpiar y parsear automáticamente
            try:
                date_clean = re.sub(r'[^0-9\-:T\.Z ]', '', date_str)
                for fmt in self.config['date_formats']:
                    try:
                        date_obj = datetime.strptime(date_clean, fmt)
                        return date_obj.strftime('%Y-%m-%dT%H:%M:%SZ')
                    except ValueError:
                        continue
            except:
                pass
        
        return None
    
    def parse_status(self, status: Any) -> Optional[str]:
        """
        Normaliza el estado de la transacción
        Decisión humana: Mapeo de estados a SUCCESS, FAILED, PENDING
        """
        if not status:
            return 'PENDING'  # Decisión humana: por defecto PENDING
        
        if isinstance(status, str):
            status_clean = status.strip().upper()
            
            # Buscar en el mapeo
            for key, value in self.config['status_mapping'].items():
                if status_clean == key.upper():
                    return value
                # Decisión humana: Coincidencia parcial
                if key.upper() in status_clean or status_clean in key.upper():
                    return value
        
        return 'PENDING'
    
    def normalize_transaction(self, transaction: Dict) -> Dict:
        """
        Normaliza una transacción al formato estándar
        """
        # Detectar fuente
        source = self.detect_source(transaction)
        if not source:
            self.invalid_transactions.append({
                'transaction': transaction,
                'reason': 'Fuente no detectada'
            })
            return None
        
        source_config = self.config['sources'][source]
        source_type = source_config.get('amount_type', 'decimal')
        
        # Extraer campos según configuración
        try:
            transaction_id = transaction.get(source_config['id_field'])
            amount_raw = transaction.get(source_config['amount_field'])
            currency_raw = transaction.get(source_config['currency_field'])
            date_raw = transaction.get(source_config['date_field'])
            status_raw = transaction.get(source_config['status_field'])
        except Exception as e:
            self.invalid_transactions.append({
                'transaction': transaction,
                'reason': f'Error extrayendo campos: {str(e)}'
            })
            return None
        
        # Validar campos obligatorios
        if transaction_id is None:
            self.invalid_transactions.append({
                'transaction': transaction,
                'reason': 'ID no encontrado'
            })
            return None
        
        # Parsear monto
        amount = self.parse_amount(amount_raw, source_type)
        if amount is None:
            self.invalid_transactions.append({
                'transaction': transaction,
                'reason': 'Monto inválido'
            })
            return None
        
        # Parsear moneda
        currency = self.parse_currency(currency_raw)
        if currency is None:
            self.invalid_transactions.append({
                'transaction': transaction,
                'reason': 'Moneda inválida'
            })
            return None
        
        # Parsear fecha
        timestamp = self.parse_date(date_raw)
        if timestamp is None:
            # Decisión humana: Si no hay fecha, usar fecha actual
            timestamp = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
        
        # Parsear estado
        status = self.parse_status(status_raw)
        
        # Construir transacción normalizada
        normalized = {
            'id': str(transaction_id),
            'amount': round(amount, 2),
            'currency': currency,
            'timestamp': timestamp,
            'status': status,
            'source': source,
            'original_data': transaction
        }
        
        return normalized
    
    def normalize_file(self, file_path: str) -> Dict:
        """
        Normaliza todas las transacciones de un archivo JSON
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Si es un objeto con lista de transacciones
            if isinstance(data, dict) and 'transactions' in data:
                transactions = data['transactions']
            elif isinstance(data, list):
                transactions = data
            else:
                transactions = [data]
            
        except Exception as e:
            return {
                'error': f'Error leyendo archivo: {str(e)}',
                'normalized': [],
                'invalid': []
            }
        
        normalized_list = []
        for tx in transactions:
            normalized = self.normalize_transaction(tx)
            if normalized:
                normalized_list.append(normalized)
                self.normalized_transactions.append(normalized)
        
        return {
            'total': len(transactions),
            'normalized': len(normalized_list),
            'invalid': len(self.invalid_transactions),
            'invalid_details': self.invalid_transactions,
            'data': normalized_list
        }
