import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.cli import parse_arguments
from src.config import Config
from src.dependency_fetcher import DependencyFetcher

def main():
    try:
        args_dict = parse_arguments()
        
        config = Config(args_dict)
        
        # ВЫВОД ПАРАМЕТРОВ
        print("=== Параметры конфигурации ===")
        for key, value in config.to_dict().items():
            print(f"{key}: {value}")
        print("==============================")
        
        print(f"\n=== Получение зависимостей для {config.package_name} ===")
        
        fetcher = DependencyFetcher(config)
        package = fetcher.fetch_dependencies()
        
        # ВЫВОД ПРЯМЫХ ЗАВИСИМОСТЕЙ (требование этапа 2)
        print(f"Прямые зависимости пакета {package.name} версии {package.version}:")
        if package.dependencies:
            for i, dep in enumerate(package.dependencies, 1):
                print(f"  {i}. {dep}")
        else:
            print("  Зависимости не найдены")
        
        print("==============================")
        
    except Exception as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()