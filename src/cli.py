import argparse
from typing import Dict, Any

def parse_arguments() -> Dict[str, Any]:
    parser = argparse.ArgumentParser(
        description="Инструмент визуализации графа зависимостей для пакетов Python",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    # Обязательные параметры
    parser.add_argument(
        '--package',
        type=str,
        required=True,
        help='Имя анализируемого пакета'
    )
    
    parser.add_argument(
        '--repository',
        type=str,
        required=True,
        help='URL-адрес репозитория или путь к файлу тестового репозитория'
    )
    
    # Опциональные параметры
    parser.add_argument(
        '--test-mode',
        action='store_true',
        help='Режим работы с тестовым репозиторием'
    )
    
    parser.add_argument(
        '--version',
        type=str,
        default='latest',
        help='Версия пакета (по умолчанию: latest)'
    )
    
    parser.add_argument(
        '--max-depth',
        type=int,
        default=10,
        help='Максимальная глубина анализа зависимостей (по умолчанию: 10)'
    )
    
    args = parser.parse_args()
    
    return {
        'package_name': args.package,
        'repository': args.repository,
        'test_mode': args.test_mode,
        'version': args.version,
        'max_depth': args.max_depth
    }