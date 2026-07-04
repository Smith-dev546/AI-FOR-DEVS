"""
Módulo de Validación de Transacciones
Decisión humana: Definir qué es válido o inválido
"""

from typing import Dict, List, Tuple
from datetime import datetime

class TransactionValidator:
    """
    Valida transacciones normalizadas
    IA ayudó con: Estructura de clases
    Decisión humana: Reglas de validación específicas
    """
    
    def __init__(self, config: Dict):
        self.config = config
        self.validation_rules = config.get('validation_rules', {})
        self.errors = []
    
    def validate_transaction(self, transaction: Dict) -> Tuple[bool, List[str]]:
        """
        Valida una transacción normalizada
        Retorna: (válido, lista_de_errores)
        """
        errors = []
        
        # Validar ID
        if not transaction.get('id'):
            errors.append("ID faltante o vacío")
        
        # Validar monto
        amount = transaction.get('amount')
        if amount is None:
            errors.append("Monto faltante")
        else:
            try:
                amount = float(amount)
                min_amount = self.validation_rules.get('min_amount', 0.01)
                max_amount = self.validation_rules.get('max_amount', 1000000)
                
                if amount <= 0:
                    errors.append(f"Monto debe ser positivo (actual: {amount})")
                elif amount < min_amount:
                    errors.append(f"Monto menor al mínimo permitido ({min_amount})")
                elif amount > max_amount:
                    errors.append(f"Monto mayor al máximo permitido ({max_amount})")
            except ValueError:
                errors.append(f"Monto inválido: {amount}")
        
        # Validar moneda
        currency = transaction.get('currency')
        allowed_currencies = self.validation_rules.get('allowed_currencies', ['USD', 'EUR', 'GBP'])
        if not currency:
            errors.append("Moneda faltante")
        elif currency not in allowed_currencies:
            errors.append(f"Moneda no soportada: {currency}")
        
        # Validar estado
        status = transaction.get('status')
        accepted_statuses = self.validation_rules.get('accepted_statuses', ['SUCCESS', 'FAILED', 'PENDING'])
        if not status:
            errors.append("Estado faltante")
        elif status not in accepted_statuses:
            errors.append(f"Estado inválido: {status}")
        
        # Validar timestamp
        timestamp = transaction.get('timestamp')
        if timestamp:
            try:
                # Intentar parsear ISO-8601
                datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            except:
                errors.append(f"Timestamp inválido: {timestamp}")
        
        is_valid = len(errors) == 0
        
        if not is_valid:
            self.errors.append({
                'transaction_id': transaction.get('id', 'unknown'),
                'errors': errors,
                'transaction': transaction
            })
        
        return is_valid, errors
    
    def validate_batch(self, transactions: List[Dict]) -> Dict:
        """
        Valida un lote de transacciones
        """
        valid = []
        invalid = []
        
        for tx in transactions:
            is_valid, errors = self.validate_transaction(tx)
            if is_valid:
                valid.append(tx)
            else:
                invalid.append({
                    'transaction': tx,
                    'errors': errors
                })
        
        return {
            'total': len(transactions),
            'valid_count': len(valid),
            'invalid_count': len(invalid),
            'valid_transactions': valid,
            'invalid_transactions': invalid,
            'error_details': self.errors
        }
