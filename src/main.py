import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.cli import parse_arguments
from src.config import Config
from src.dependency_fetcher import DependencyFetcher
from src.graph_builder import GraphBuilder
from src.d2_visualizer import D2Visualizer

def main():
    try:
        args_dict = parse_arguments()
        
        config = Config(args_dict)
        
        print("=== Параметры конфигурации ===")
        for key, value in config.to_dict().items():
            print(f"{key}: {value}")
        print("==============================")
        
        print(f"\n=== Получение зависимостей для {config.package_name} ===")
        
        fetcher = DependencyFetcher(config)
        package = fetcher.fetch_dependencies()
        
        print(f"Прямые зависимости пакета {package.name} версии {package.version}:")
        if package.dependencies:
            for i, dep in enumerate(package.dependencies, 1):
                print(f"  {i}. {dep}")
        else:
            print("  Зависимости не найдены")
        
        print(f"\n=== Построение графа зависимостей (макс. глубина: {config.max_depth}) ===")
        
        graph_builder = GraphBuilder(config, fetcher)
        graph = graph_builder.build_dependency_graph()
        
        print(f"Всего пакетов в графе: {len(graph.all_packages)}")
        print(f"Транзитивные зависимости: {len(graph.get_all_dependencies())}")
        
        if graph_builder.cycles_detected:
            print(f"Обнаружены циклические зависимости: {graph_builder.cycles_detected}")
        else:
            print("Циклические зависимости не обнаружены")
        
        if config.reverse:
            print(f"\n=== Обратные зависимости для {config.package_name} ===")
            reverse_deps = graph_builder.find_reverse_dependencies(graph, config.package_name)
            if reverse_deps:
                print(f"Пакеты, зависящие от {config.package_name}:")
                for i, dep in enumerate(reverse_deps, 1):
                    print(f"  {i}. {dep}")
            else:
                print(f"Нет пакетов, зависящих от {config.package_name}")
            print("==============================")
        
        if config.output:
            print(f"\n=== Визуализация графа зависимостей ===")
            visualizer = D2Visualizer()
            
            d2_code = visualizer.generate_d2_code(graph)
            print("Сгенерирован код D2:")
            print(d2_code)
            
            filename = config.output or config.package_name
            d2_path = visualizer.save_d2_file(d2_code, filename)
            print(f"D2 файл сохранен: {d2_path}")
            
            try:
                svg_path = visualizer.render_svg(d2_path, filename)
                visualizer.display_svg_info(svg_path)
            except Exception as e:
                print(f"Ошибка визуализации: {e}")
                print("Установите D2: https://github.com/terrastruct/d2")
            
            print("==============================")
        
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