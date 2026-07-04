"""
Sistema de Análisis de Logs
Autor: José Smimth Méndez Hernández
Fecha: 2026-07-03
Descripción: Script para analizar archivos de logs y generar estadísticas
Versión: 1.0.0
"""

import re
import sys
import os
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from pathlib import Path

class LogAnalyzer:
    """
    Clase principal para análisis de archivos de log
    Decisión humana: Estructura orientada a objetos para mejor organización
    """
    
    def __init__(self):
        """
        Inicializa el analizador con configuraciones predeterminadas
        Decisión humana: Definir patrones y estadísticas en el constructor
        """
        # Patrón de expresión regular para parsear líneas de log
        # IA ayudó con la sugerencia inicial, pero fue modificado por criterio humano
        self.log_pattern = re.compile(
            r'^\s*\[(INFO|WARNING|ERROR)\](?:\s+(\d{4}-\d{2}-\d{2}))?\s*(.+)?$',
            re.IGNORECASE  # Decisión humana: hacer case-insensitive
        )
        
        # Decisión humana: definir estructura de estadísticas
        self.stats = {
            'total': 0,
            'by_level': {'INFO': 0, 'WARNING': 0, 'ERROR': 0},
            'invalid_lines': 0,
            'no_date': 0,
            'invalid_date': 0,
            'empty_lines': 0,
            'line_details': []  # Para análisis detallado
        }
        
        # Decisión humana: definir niveles válidos
        self.valid_levels = {'INFO', 'WARNING', 'ERROR'}
    
    def validate_date(self, date_str: str) -> bool:
        """
        Valida si una fecha tiene formato YYYY-MM-DD
        
        Args:
            date_str: String de fecha a validar
            
        Returns:
            bool: True si la fecha es válida, False en caso contrario
            
        Decisión humana: Usar datetime para validación rigurosa
        IA sugerió usar datetime.strptime, se agregó manejo de errores
        """
        if not date_str:
            return False
        
        try:
            # Validación de fecha con formato específico
            datetime.strptime(date_str, '%Y-%m-%d')
            
            # Decisión humana: validación adicional de rango de años
            year = int(date_str.split('-')[0])
            if year < 2000 or year > 2100:
                return False
                
            return True
        except ValueError:
            return False
    
    def parse_line(self, line: str) -> Tuple[bool, Dict]:
        """
        Analiza una línea de log y extrae información estructurada
        
        Args:
            line: Línea de texto a analizar
            
        Returns:
            Tuple[bool, Dict]: (es_válida, datos_extraídos)
            
        Decisión humana: Estructura de retorno y manejo de casos específicos
        """
        line = line.strip()
        
        # Decisión humana: Manejar líneas vacías como caso especial
        if not line:
            return False, {'reason': 'empty_line', 'line': line}
        
        match = self.log_pattern.match(line)
        if not match:
            return False, {'reason': 'invalid_format', 'line': line}
        
        level, date, message = match.groups()
        
        # Decisión humana: Validar que el nivel sea válido (case-insensitive)
        if level.upper() not in self.valid_levels:
            return False, {'reason': 'invalid_level', 'line': line}
        
        # Decisión humana: Validar que haya mensaje
        if not message or message.strip() == '':
            return False, {'reason': 'no_message', 'line': line}
        
        # Construir resultado
        result = {
            'level': level.upper(),
            'date': date,
            'message': message.strip(),
            'has_date': bool(date),
            'date_valid': False,
            'line': line
        }
        
        # Validar fecha si existe
        if date:
            result['date_valid'] = self.validate_date(date)
            if not result['date_valid']:
                return False, {'reason': 'invalid_date', 'line': line}
        
        return True, result
    
    def analyze_file(self, file_path: str) -> Dict:
        """
        Analiza un archivo de log completo
        
        Args:
            file_path: Ruta al archivo de log
            
        Returns:
            Dict: Estadísticas del análisis
            
        Decisión humana: Manejo robusto de errores de archivo
        """
        # Resetear estadísticas para cada análisis
        self.stats = {
            'total': 0,
            'by_level': {'INFO': 0, 'WARNING': 0, 'ERROR': 0},
            'invalid_lines': 0,
            'no_date': 0,
            'invalid_date': 0,
            'empty_lines': 0,
            'line_details': []
        }
        
        # Decisión humana: Verificar que el archivo existe y es legible
        if not os.path.exists(file_path):
            return {'error': f'Archivo no encontrado: {file_path}'}
        
        if not os.path.isfile(file_path):
            return {'error': f'La ruta no es un archivo: {file_path}'}
        
        # Decisión humana: Manejar diferentes codificaciones
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
        except UnicodeDecodeError:
            try:
                # Intento con codificación diferente
                with open(file_path, 'r', encoding='latin-1') as file:
                    lines = file.readlines()
            except Exception as e:
                return {'error': f'Error de codificación: {str(e)}'}
        except Exception as e:
            return {'error': f'Error al leer archivo: {str(e)}'}
        
        # Decisión humana: Procesar línea por línea con información detallada
        for line_num, line in enumerate(lines, 1):
            self.stats['total'] += 1
            
            # Decisión humana: Manejar líneas vacías
            if not line.strip():
                self.stats['empty_lines'] += 1
                self.stats['invalid_lines'] += 1
                self.stats['line_details'].append({
                    'line_num': line_num,
                    'status': 'empty',
                    'original': line
                })
                continue
            
            is_valid, result = self.parse_line(line)
            
            if not is_valid:
                self.stats['invalid_lines'] += 1
                self.stats['line_details'].append({
                    'line_num': line_num,
                    'status': 'invalid',
                    'reason': result.get('reason', 'unknown'),
                    'original': line
                })
                continue
            
            # Línea válida
            self.stats['by_level'][result['level']] += 1
            
            if not result['has_date']:
                self.stats['no_date'] += 1
            elif not result['date_valid']:
                self.stats['invalid_date'] += 1
            
            self.stats['line_details'].append({
                'line_num': line_num,
                'status': 'valid',
                'level': result['level'],
                'date': result['date'],
                'message': result['message'],
                'original': line
            })
        
        return self.stats
    
    def display_results(self, stats: Dict, verbose: bool = False):
        """
        Muestra los resultados del análisis en formato claro y legible
        
        Args:
            stats: Diccionario con estadísticas
            verbose: Si mostrar detalles de cada línea
            
        Decisión humana: Diseño de UI en consola con formato claro
        """
        if 'error' in stats:
            print(f"\n ERROR: {stats['error']}")
            return
        
        print("\n" + "="*60)
        print(" ANÁLISIS DE LOGS COMPLETADO")
        print("="*60)
        print(f" Total de eventos: {stats['total']}")
        print("-"*60)
        
        # Decisión humana: Mostrar distribución por nivel con porcentajes
        print(" Distribución por nivel:")
        for level in ['INFO', 'WARNING', 'ERROR']:
            count = stats['by_level'][level]
            if count > 0:
                percentage = (count / stats['total']) * 100 if stats['total'] > 0 else 0
                bar = '' * int(percentage / 2)  # Barra visual
                print(f"  • {level:<7}: {count:>4} ({percentage:>5.1f}%) {bar}")
            else:
                print(f"  • {level:<7}: {count:>4} (  0.0%)")
        
        print("-"*60)
        print("  Estadísticas de calidad:")
        print(f"  • Líneas inválidas:     {stats['invalid_lines']:>4}")
        print(f"  • Líneas vacías:        {stats['empty_lines']:>4}")
        print(f"  • Sin fecha:            {stats['no_date']:>4}")
        print(f"  • Fechas inválidas:     {stats['invalid_date']:>4}")
        print("="*60)
        
        # Decisión humana: Calcular métricas de calidad
        if stats['total'] > 0:
            quality = ((stats['total'] - stats['invalid_lines']) / stats['total']) * 100
            print(f" Calidad del log: {quality:.1f}% de líneas válidas")
            
            # Decisión humana: Mostrar nivel de calidad con emojis
            if quality >= 90:
                print(" Excelente calidad de log!")
            elif quality >= 70:
                print(" Buena calidad de log")
            elif quality >= 50:
                print(" Calidad regular - Revisar líneas inválidas")
            else:
                print(" Calidad baja - Muchas líneas inválidas")
        else:
            print(" No hay líneas para analizar")
        
        print("="*60)
        
        # Decisión humana: Mostrar detalles si se solicita
        if verbose and 'line_details' in stats:
            print("\n DETALLE DE LÍNEAS:")
            print("-"*60)
            for detail in stats['line_details']:
                status_icon = '' if detail['status'] == 'valid' else '❌'
                print(f"{status_icon} Línea {detail['line_num']:>3}: {detail['original'].strip()[:50]}")
                if detail['status'] == 'invalid' and 'reason' in detail:
                    print(f"   → Motivo: {detail['reason']}")
            print("="*60)
    
    def generate_report(self, stats: Dict, output_file: str = None):
        """
        Genera un reporte detallado en formato texto
        
        Args:
            stats: Estadísticas del análisis
            output_file: Ruta para guardar el reporte
            
        Decisión humana: Capacidad de exportar resultados
        """
        report_lines = []
        report_lines.append("="*60)
        report_lines.append("REPORTE DE ANÁLISIS DE LOGS")
        report_lines.append("="*60)
        report_lines.append(f"Fecha de análisis: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append(f"Total de eventos: {stats['total']}")
        report_lines.append("-"*60)
        report_lines.append("Distribución por nivel:")
        for level in ['INFO', 'WARNING', 'ERROR']:
            count = stats['by_level'][level]
            percentage = (count / stats['total']) * 100 if stats['total'] > 0 else 0
            report_lines.append(f"  {level}: {count} ({percentage:.1f}%)")
        report_lines.append("-"*60)
        report_lines.append("Estadísticas de calidad:")
        report_lines.append(f"  Líneas inválidas: {stats['invalid_lines']}")
        report_lines.append(f"  Líneas vacías: {stats['empty_lines']}")
        report_lines.append(f"  Sin fecha: {stats['no_date']}")
        report_lines.append(f"  Fechas inválidas: {stats['invalid_date']}")
        
        if stats['total'] > 0:
            quality = ((stats['total'] - stats['invalid_lines']) / stats['total']) * 100
            report_lines.append(f"Calidad del log: {quality:.1f}%")
        
        report_text = "\n".join(report_lines)
        
        if output_file:
            try:
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(report_text)
                print(f" Reporte guardado en: {output_file}")
            except Exception as e:
                print(f" Error al guardar reporte: {e}")
        
        return report_text

def main():
    """
    Función principal del programa
    Decisión humana: Interfaz de usuario interactiva
    """
    print(" ANALIZADOR DE LOGS")
    print("="*50)
    print("Bienvenido al analizador de archivos de log")
    print("El script analizará líneas con formato:")
    print("  • [INFO] YYYY-MM-DD Mensaje")
    print("  • [WARNING] YYYY-MM-DD Mensaje")
    print("  • [ERROR] YYYY-MM-DD Mensaje")
    print("  • [INFO] Mensaje (sin fecha)")
    print("="*50)
    
    analyzer = LogAnalyzer()
    
    while True:
        print("\n Opciones:")
        print("  1. Analizar archivo de log")
        print("  2. Analizar archivo con detalles")
        print("  3. Generar reporte")
        print("  4. Salir")
        
        choice = input("\nSelecciona una opción (1-4): ").strip()
        
        if choice == '4':
            print("\n ¡Hasta luego!")
            break
        
        if choice not in ['1', '2', '3']:
            print(" Opción inválida. Intenta de nuevo.")
            continue
        
        file_path = input("\n Ingresa la ruta del archivo de log: ").strip()
        
        if not file_path:
            print(" Ruta vacía. Intenta de nuevo.")
            continue
        
        # Decisión humana: Validar extensión del archivo
        if not file_path.lower().endswith(('.txt', '.log')):
            print("  El archivo no tiene extensión .txt o .log, pero se intentará analizar")
        
        results = analyzer.analyze_file(file_path)
        
        if choice == '1':
            analyzer.display_results(results, verbose=False)
        elif choice == '2':
            analyzer.display_results(results, verbose=True)
        elif choice == '3':
            analyzer.display_results(results, verbose=False)
            report_choice = input("\n¿Guardar reporte en archivo? (s/n): ").lower()
            if report_choice == 's':
                report_name = input("Nombre del archivo de reporte (por defecto: reporte.txt): ").strip()
                if not report_name:
                    report_name = "reporte.txt"
                if not report_name.endswith('.txt'):
                    report_name += '.txt'
                analyzer.generate_report(results, report_name)
        
        # Decisión humana: Preguntar si continuar
        continue_choice = input("\n¿Analizar otro archivo? (s/n): ").lower()
        if continue_choice != 's':
            print("\n ¡Hasta luego!")
            break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n Programa interrumpido por el usuario. ¡Hasta luego!")
        sys.exit(0)
    except Exception as e:
        print(f"\n Error inesperado: {e}")
        print("Por favor, reporta este error al desarrollador.")
        sys.exit(1)