import argparse
from typing import Dict, Any

def parse_arguments() -> Dict[str, Any]:
    parser = argparse.ArgumentParser(
        description="Инструмент визуализации графа зависимостей для пакетов Python",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('--package', type=str, required=True, help='Имя анализируемого пакета')
    parser.add_argument('--repository', type=str, required=True, help='URL или путь к файлу')
    parser.add_argument('--test-mode', action='store_true', help='Режим тестирования')
    parser.add_argument('--version', type=str, default='latest', help='Версия пакета')
    parser.add_argument('--max-depth', type=int, default=10, help='Максимальная глубина')
    parser.add_argument('--reverse', action='store_true', help='Режим вывода обратных зависимостей')
    
    args = parser.parse_args()
    
    return {
        'package_name': args.package,
        'repository': args.repository,
        'test_mode': args.test_mode,
        'version': args.version,
        'max_depth': args.max_depth,
        'reverse': args.reverse
    }