from typing import Dict, Any
from urllib.parse import urlparse
import os

class Config:
    def __init__(self, config_dict: Dict[str, Any]):
        self.package_name = config_dict['package_name']
        self.repository = config_dict['repository']
        self.test_mode = config_dict['test_mode']
        self.version = config_dict['version']
        self.max_depth = config_dict['max_depth']
        self.reverse = config_dict['reverse']
        self.output = config_dict['output']
        
        self._validate()
    
    def _validate(self):
        self._validate_package_name()
        self._validate_repository()
        self._validate_version()
        self._validate_max_depth()
        self._validate_output()
    
    def _validate_package_name(self):
        if not self.package_name or not isinstance(self.package_name, str):
            raise ValueError("Имя пакета должно быть непустой строкой")
        if not all(c.isalnum() or c in ['-', '_', '.'] for c in self.package_name):
            raise ValueError(f"Некорректное имя пакета: {self.package_name}")
    
    def _validate_repository(self):
        if not self.repository or not isinstance(self.repository, str):
            raise ValueError("Репозиторий должен быть непустой строкой")
        if self.test_mode:
            if not os.path.exists(self.repository):
                raise ValueError(f"Тестовый файл не найден: {self.repository}")
        else:
            try:
                result = urlparse(self.repository)
                if not all([result.scheme, result.netloc]):
                    raise ValueError("Некорректный URL репозитория")
            except Exception as e:
                raise ValueError(f"Некорректный URL репозитория: {e}")
    
    def _validate_version(self):
        if not self.version or not isinstance(self.version, str):
            raise ValueError("Версия пакета должна быть непустой строкой")
    
    def _validate_max_depth(self):
        if not isinstance(self.max_depth, int) or self.max_depth <= 0:
            raise ValueError("Максимальная глубина должна быть положительным целым числом")
        if self.max_depth > 100:
            raise ValueError("Максимальная глубина не может превышать 100")
    
    def _validate_output(self):
        if self.output and not isinstance(self.output, str):
            raise ValueError("Имя выходного файла должно быть строкой")
        if self.output:
            invalid_chars = set('/\\:*?"<>|')
            if any(char in self.output for char in invalid_chars):
                raise ValueError("Имя файла содержит недопустимые символы")
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'package_name': self.package_name,
            'repository': self.repository,
            'test_mode': self.test_mode,
            'version': self.version,
            'max_depth': self.max_depth,
            'reverse': self.reverse,
            'output': self.output
        }