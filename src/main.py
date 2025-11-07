import sys
import os

# Добавляем путь к src в PYTHONPATH
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.cli import parse_arguments
from src.config import Config

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
        
        # Здесь в будущих этапах будет основная логика
        print("\nКонфигурация успешно загружена и валидирована!")
        
    except Exception as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()