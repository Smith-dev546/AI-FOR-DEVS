"""
Módulo de Interfaz Interactiva
Decisión humana: Diseño de menú y opciones de filtrado
IA ayudó con: Estructura de menú y manejo de entrada
"""

import sys
import os
from typing import List, Dict, Optional
from datetime import datetime

# Agregar la carpeta src al path para imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from normalizer import TransactionNormalizer
from validator import TransactionValidator
from metrics import MetricsCalculator

class TransactionInterface:
    """
    Interfaz CLI interactiva para explorar transacciones normalizadas
    Decisión humana: Diseño de la experiencia de usuario
    """
    
    def __init__(self):
        self.normalizer = TransactionNormalizer()
        self.validator = TransactionValidator(self.normalizer.config)
        self.metrics_calc = MetricsCalculator()
        self.transactions = []
        self.current_filter = {}
        self.validated_data = None
    
    def clear_screen(self):
        """Limpia la consola"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self, title: str):
        """Imprime un encabezado formateado"""
        print("\n" + "="*60)
        print(f"💰 {title}")
        print("="*60)
    
    def print_menu(self):
        """Muestra el menú principal"""
        self.clear_screen()
        print("="*60)
        print("💰 SISTEMA DE NORMALIZACIÓN DE TRANSACCIONES")
        print("="*60)
        print("\n📋 Menú Principal:")
        print("  1. Cargar y normalizar transacciones")
        print("  2. Ver métricas y estadísticas")
        print("  3. Listar transacciones")
        print("  4. Filtrar transacciones")
        print("  5. Ver transacciones inválidas")
        print("  6. Exportar resultados")
        print("  7. Salir")
        print("\n" + "-"*60)
    
    def load_and_normalize(self):
        """Carga y normaliza transacciones"""
        self.print_header("CARGAR TRANSACCIONES")
        
        file_path = input("\n📁 Ruta del archivo JSON: ").strip()
        
        if not file_path:
            file_path = "data/transacciones.json"
            print(f"⚠️  Usando archivo por defecto: {file_path}")
        
        result = self.normalizer.normalize_file(file_path)
        
        if 'error' in result:
            print(f"\n❌ Error: {result['error']}")
            input("\nPresiona Enter para continuar...")
            return
        
        self.transactions = result['data']
        
        # Validar transacciones
        validation_result = self.validator.validate_batch(self.transactions)
        self.validated_data = validation_result
        
        print(f"\n✅ Procesamiento completado:")
        print(f"  • Total de transacciones: {result['total']}")
        print(f"  • Normalizadas: {result['normalized']}")
        print(f"  • Inválidas: {result['invalid']}")
        print(f"  • Válidas según reglas: {validation_result['valid_count']}")
        
        # Mostrar detalles de inválidas
        if result['invalid'] > 0:
            print("\n⚠️  Transacciones inválidas:")
            for inv in result['invalid_details'][:3]:  # Mostrar primeras 3
                print(f"  • ID: {inv.get('transaction', {}).get('id', 'unknown')}")
                print(f"    Motivo: {inv.get('reason', 'desconocido')}")
            if result['invalid'] > 3:
                print(f"  ... y {result['invalid'] - 3} más")
        
        input("\nPresiona Enter para continuar...")
    
    def show_metrics(self):
        """Muestra métricas y estadísticas"""
        if not self.transactions:
            print("\n⚠️  Primero debes cargar transacciones (Opción 1)")
            input("\nPresiona Enter para continuar...")
            return
        
        self.print_header("MÉTRICAS Y ESTADÍSTICAS")
        
        metrics = self.metrics_calc.calculate_metrics(self.transactions)
        summary = self.metrics_calc.get_summary(metrics)
        print(f"\n{summary}")
        
        input("\nPresiona Enter para continuar...")
    
    def list_transactions(self, transactions: List[Dict] = None, title: str = "TRANSACCIONES"):
        """Lista transacciones con paginación"""
        if transactions is None:
            transactions = self.transactions
        
        if not transactions:
            print("\n⚠️  No hay transacciones para mostrar")
            input("\nPresiona Enter para continuar...")
            return
        
        self.print_header(title)
        print(f"\n📝 Total: {len(transactions)} transacciones")
        print("-"*60)
        
        # Decisión humana: Mostrar en formato tabla
        print(f"{'ID':<12} {'Monto':>10} {'Moneda':<6} {'Estado':<10} {'Fuente':<10} {'Fecha':<20}")
        print("-"*60)
        
        # Paginación
        page_size = 10
        total_pages = (len(transactions) + page_size - 1) // page_size
        current_page = 0
        
        while current_page < total_pages:
            start = current_page * page_size
            end = min(start + page_size, len(transactions))
            
            # Limpiar pantalla
            self.clear_screen()
            print(f"\n📋 {title} - Página {current_page + 1}/{total_pages}")
            print("-"*60)
            print(f"{'ID':<12} {'Monto':>10} {'Moneda':<6} {'Estado':<10} {'Fuente':<10} {'Fecha':<20}")
            print("-"*60)
            
            for tx in transactions[start:end]:
                amount = tx.get('amount', 0)
                currency = tx.get('currency', 'N/A')
                status = tx.get('status', 'N/A')
                source = tx.get('source', 'N/A')
                timestamp = tx.get('timestamp', 'N/A')
                
                # Truncar timestamp para mostrar
                if len(timestamp) > 19:
                    timestamp = timestamp[:19]
                
                print(f"{tx.get('id', 'N/A'):<12} {amount:>10.2f} {currency:<6} {status:<10} {source:<10} {timestamp:<20}")
            
            print("-"*60)
            
            # Controles de paginación
            if current_page < total_pages - 1:
                choice = input("\n[S]iguiente | [A]nterior | [V]er detalles | [M]enú principal: ").strip().upper()
                
                if choice == 'S':
                    current_page += 1
                elif choice == 'A' and current_page > 0:
                    current_page -= 1
                elif choice == 'V':
                    self.show_transaction_detail(transactions[start:end])
                elif choice == 'M':
                    break
            else:
                if input("\nPresiona Enter para continuar..."):
                    break
                break
    
    def show_transaction_detail(self, transactions: List[Dict]):
        """Muestra detalles de una transacción específica"""
        print("\n📋 Detalle de transacción")
        print("-"*60)
        
        for i, tx in enumerate(transactions, 1):
            print(f"{i}. ID: {tx.get('id', 'N/A')}")
        
        choice = input("\nSelecciona el número de transacción (0 para cancelar): ").strip()
        
        try:
            idx = int(choice) - 1
            if idx >= 0 and idx < len(transactions):
                tx = transactions[idx]
                self.clear_screen()
                print("\n" + "="*60)
                print("📋 DETALLE DE TRANSACCIÓN")
                print("="*60)
                for key, value in tx.items():
                    if key != 'original_data':
                        print(f"  {key}: {value}")
                
                # Mostrar datos originales si existen
                if 'original_data' in tx:
                    print("\n📄 Datos originales:")
                    for key, value in tx['original_data'].items():
                        print(f"  {key}: {value}")
                
                print("="*60)
                input("\nPresiona Enter para continuar...")
        except ValueError:
            pass
    
    def filter_transactions(self):
        """Filtra transacciones por criterios"""
        if not self.transactions:
            print("\n⚠️  Primero debes cargar transacciones (Opción 1)")
            input("\nPresiona Enter para continuar...")
            return
        
        self.print_header("FILTRAR TRANSACCIONES")
        print("\nCriterios de filtro:")
        print("  1. Estado")
        print("  2. Moneda")
        print("  3. Fuente")
        print("  4. Rango de montos")
        print("  5. Limpiar filtros")
        print("  0. Volver")
        
        choice = input("\nSelecciona una opción: ").strip()
        
        filtered = self.transactions.copy()
        
        if choice == '1':
            status = input("Estado a filtrar (SUCCESS, FAILED, PENDING): ").strip().upper()
            filtered = [tx for tx in filtered if tx.get('status') == status]
            self.current_filter['status'] = status
        
        elif choice == '2':
            currency = input("Moneda a filtrar (USD, EUR, GBP, etc): ").strip().upper()
            filtered = [tx for tx in filtered if tx.get('currency') == currency]
            self.current_filter['currency'] = currency
        
        elif choice == '3':
            source = input("Fuente a filtrar: ").strip()
            filtered = [tx for tx in filtered if tx.get('source') == source]
            self.current_filter['source'] = source
        
        elif choice == '4':
            min_amount = float(input("Monto mínimo: ").strip() or "0")
            max_amount = float(input("Monto máximo: ").strip() or "9999999")
            filtered = [tx for tx in filtered if min_amount <= tx.get('amount', 0) <= max_amount]
            self.current_filter['min_amount'] = min_amount
            self.current_filter['max_amount'] = max_amount
        
        elif choice == '5':
            self.current_filter = {}
            print("\n✅ Filtros limpiados")
            input("\nPresiona Enter para continuar...")
            return
        
        elif choice == '0':
            return
        
        if filtered:
            self.list_transactions(filtered, "TRANSACCIONES FILTRADAS")
        else:
            print("\n⚠️  No hay transacciones que coincidan con el filtro")
            input("\nPresiona Enter para continuar...")
    
    def show_invalid_transactions(self):
        """Muestra transacciones inválidas"""
        if not self.validated_data or not self.validated_data['invalid_transactions']:
            print("\n✅ No hay transacciones inválidas")
            input("\nPresiona Enter para continuar...")
            return
        
        self.print_header("TRANSACCIONES INVÁLIDAS")
        print(f"\n📝 Total: {self.validated_data['invalid_count']} transacciones inválidas")
        print("-"*60)
        
        for inv in self.validated_data['invalid_transactions']:
            tx = inv['transaction']
            errors = inv['errors']
            print(f"\n❌ ID: {tx.get('id', 'N/A')}")
            print(f"   Errores:")
            for error in errors:
                print(f"     • {error}")
            print("-"*40)
        
        input("\nPresiona Enter para continuar...")
    
    def export_results(self):
        """Exporta resultados a archivo"""
        if not self.transactions:
            print("\n⚠️  Primero debes cargar transacciones")
            input("\nPresiona Enter para continuar...")
            return
        
        import json
        from datetime import datetime
        
        self.print_header("EXPORTAR RESULTADOS")
        
        metrics = self.metrics_calc.calculate_metrics(self.transactions)
        
        output = {
            'export_date': datetime.now().isoformat(),
            'summary': {
                'total': len(self.transactions),
                'valid_count': self.validated_data['valid_count'] if self.validated_data else 0,
                'invalid_count': self.validated_data['invalid_count'] if self.validated_data else 0,
            },
            'metrics': metrics,
            'transactions': self.transactions,
            'invalid_transactions': self.validated_data['invalid_transactions'] if self.validated_data else []
        }
        
        filename = f"export_transacciones_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(output, f, indent=2, default=str)
            print(f"\n✅ Exportado a: {filename}")
        except Exception as e:
            print(f"\n❌ Error exportando: {e}")
        
        input("\nPresiona Enter para continuar...")
    
    def run(self):
        """Ejecuta el bucle principal de la interfaz"""
        while True:
            self.print_menu()
            
            choice = input("\nSelecciona una opción (1-7): ").strip()
            
            if choice == '1':
                self.load_and_normalize()
            elif choice == '2':
                self.show_metrics()
            elif choice == '3':
                self.list_transactions()
            elif choice == '4':
                self.filter_transactions()
            elif choice == '5':
                self.show_invalid_transactions()
            elif choice == '6':
                self.export_results()
            elif choice == '7':
                print("\n👋 ¡Hasta luego!")
                break
            else:
                print("\n❌ Opción inválida. Intenta de nuevo.")
                input("Presiona Enter para continuar...")

def main():
    """Punto de entrada principal"""
    interface = TransactionInterface()
    interface.run()

if __name__ == "__main__":
    main()