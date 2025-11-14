import sys
import os

# Добавляем путь к src в PYTHONPATH
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.cli import parse_arguments
from src.config import Config
from src.dependency_fetcher import DependencyFetcher
from src.graph_builder import GraphBuilder

def main():
    try:
        # Парсим аргументы командной строки
        args_dict = parse_arguments()
        
        # Создаем и валидируем конфигурацию
        config = Config(args_dict)
        
        # ВЫВОД ПАРАМЕТРОВ (требование этапа 1)
        print("=== Параметры конфигурации ===")
        for key, value in config.to_dict().items():
            print(f"{key}: {value}")
        print("==============================")
        
        # ЭТАП 2: Получение прямых зависимостей
        print(f"\n=== Получение зависимостей для {config.package_name} ===")
        
        fetcher = DependencyFetcher(config)
        package = fetcher.fetch_dependencies()
        
        print(f"Прямые зависимости пакета {package.name} версии {package.version}:")
        if package.dependencies:
            for i, dep in enumerate(package.dependencies, 1):
                print(f"  {i}. {dep}")
        else:
            print("  Зависимости не найдены")
        
        # ЭТАП 3: Построение полного графа зависимостей
        print(f"\n=== Построение графа зависимостей (макс. глубина: {config.max_depth}) ===")
        
        graph_builder = GraphBuilder(config, fetcher)
        graph = graph_builder.build_dependency_graph()
        
        # Выводим результаты
        print(f"Всего пакетов в графе: {len(graph.all_packages)}")
        print(f"Транзитивные зависимости: {len(graph.get_all_dependencies())}")
        
        if graph_builder.cycles_detected:
            print(f"Обнаружены циклические зависимости: {graph_builder.cycles_detected}")
        else:
            print("Циклические зависимости не обнаружены")
        
        # Демонстрация работы с тестовым репозиторием
        if config.test_mode:
            print(f"\n=== Режим тестирования ===")
            print("Граф успешно построен из тестового файла")
            print("Пакеты в графе:", list(graph.all_packages.keys()))
        
        print("==============================")
        
    except Exception as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()