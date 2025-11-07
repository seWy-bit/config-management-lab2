import os
import re
import requests
from typing import List, Optional
from urllib.parse import urljoin

from src.models import Package
from src.config import Config

class DependencyFetcher:
    """Класс для получения информации о зависимостях Python-пакетов"""
    
    def __init__(self, config: Config):
        self.config = config
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'DependencyVisualizer/1.0'
        })
    
    def fetch_dependencies(self) -> Package:
        if self.config.test_mode:
            return self._fetch_from_test_repository()
        else:
            return self._fetch_from_pypi()
    
    def _fetch_from_test_repository(self) -> Package:
        try:
            with open(self.config.repository, 'r', encoding='utf-8') as f:
                dependencies = []
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):  # Игнорируем пустые строки и комментарии
                        dependencies.append(line)
                
                return Package(
                    name=self.config.package_name,
                    version=self.config.version,
                    dependencies=dependencies
                )
        except Exception as e:
            raise Exception(f"Ошибка чтения тестового репозитория: {e}")
    
    def _fetch_from_pypi(self) -> Package:
        package_name = self.config.package_name
        version = self.config.version if self.config.version != 'latest' else None
        
        try:
            # Получаем информацию о пакете
            if version:
                url = f"https://pypi.org/pypi/{package_name}/{version}/json"
            else:
                url = f"https://pypi.org/pypi/{package_name}/json"
            
            response = self.session.get(url)
            response.raise_for_status()
            
            package_data = response.json()
            info = package_data['info']
            
            # Извлекаем зависимости
            dependencies = self._extract_dependencies(info)
            
            return Package(
                name=info['name'],
                version=info['version'],
                dependencies=dependencies
            )
            
        except requests.RequestException as e:
            raise Exception(f"Ошибка получения данных с PyPI: {e}")
        except KeyError as e:
            raise Exception(f"Некорректный формат данных от PyPI: {e}")
    
    def _extract_dependencies(self, package_info: dict) -> List[str]:
        dependencies = []
        
        # Зависимости указываются в requires_dist
        requires_dist = package_info.get('requires_dist', [])
        
        for requirement in requires_dist:
            # Извлекаем имя пакета из строки требования
            # Форматы: "package", "package>=1.0", "package[extra]"
            package_name = self._parse_requirement(requirement)
            if package_name and package_name not in dependencies:
                dependencies.append(package_name)
        
        return dependencies
    
    def _parse_requirement(self, requirement: str) -> Optional[str]:
        # Убираем пробелы
        requirement = requirement.strip()
        
        # Разделяем по операторам сравнения
        for operator in ['==', '!=', '<=', '>=', '<', '>', '~=']:
            if operator in requirement:
                requirement = requirement.split(operator)[0].strip()
        
        # Убираем extras [something]
        if '[' in requirement:
            requirement = requirement.split('[')[0].strip()
        
        # Проверяем, что осталось валидное имя пакета
        if requirement and re.match(r'^[a-zA-Z0-9-_\.]+$', requirement):
            return requirement
        
        return None