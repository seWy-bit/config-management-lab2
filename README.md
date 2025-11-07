# Dependency Visualizer

Инструмент визуализации графа зависимостей для менеджера пакетов Python (pip).

## Вариант №18

### Этап 1: Минимальный прототип с конфигурацией ✅
### Этап 2: Сбор данных ✅

Реализовано:
- Получение информации о зависимостях из PyPI через API
- Поддержка тестового режима с чтением из файла
- Извлечение и парсинг прямых зависимостей
- Вывод списка прямых зависимостей на экран

### Использование

```bash
# Режим работы с реальным репозиторием (PyPI)
python src/main.py --package requests --repository https://pypi.org/simple/

# С указанием версии
python src/main.py --package django --repository https://pypi.org/simple/ --version 4.2.0

# Тестовый режим
python src/main.py --package TEST --repository tests/test_data/test_repo.txt --test-mode