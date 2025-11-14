import os
import re
import requests
from typing import List, Optional, Dict
from urllib.parse import urljoin

from src.models import Package
from src.config import Config

class DependencyFetcher:
    def __init__(self, config: Config):
        self.config = config
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'DependencyVisualizer/1.0'
        })
        self.cache: Dict[str, Package] = {}  # Кеш для избежания повторных запросов
    
    def fetch_dependencies(self) -> Package:
        cache_key = f"{self.config.package_name}_{self.config.version}"
        
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        if self.config.test_mode:
            result = self._fetch_from_test_repository()
        else:
            result = self._fetch_from_pypi()
        
        self.cache[cache_key] = result
        return result
    
    def _fetch_from_test_repository(self) -> Package:
        try:
            with open(self.config.repository, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        parts = line.split()
                        if parts[0] == self.config.package_name:
                            dependencies = parts[1:] if len(parts) > 1 else []
                            return Package(
                                name=self.config.package_name,
                                version=self.config.version,
                                dependencies=dependencies
                            )
                
                return Package(
                    name=self.config.package_name,
                    version=self.config.version,
                    dependencies=[]
                )
                
        except Exception as e:
            raise Exception(f"Ошибка чтения тестового репозитория: {e}")

    def load_entire_test_repository(self) -> Dict[str, Package]:
        packages = {}
        try:
            with open(self.config.repository, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        parts = line.split()
                        package_name = parts[0]
                        dependencies = parts[1:] if len(parts) > 1 else []
                        packages[package_name] = Package(
                            name=package_name,
                            version='latest',
                            dependencies=dependencies
                        )
        except Exception as e:
            raise Exception(f"Ошибка чтения тестового репозитория: {e}")
        
        return packages
    
    def _fetch_from_pypi(self) -> Package:
        package_name = self.config.package_name
        version = self.config.version if self.config.version != 'latest' else None
        
        try:
            if version:
                url = f"https://pypi.org/pypi/{package_name}/{version}/json"
            else:
                url = f"https://pypi.org/pypi/{package_name}/json"
            
            response = self.session.get(url)
            response.raise_for_status()
            
            package_data = response.json()
            info = package_data['info']
            
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
        requires_dist = package_info.get('requires_dist', [])
        
        # ЗАЩИТА ОТ None
        if requires_dist is None:
            requires_dist = []
        
        for requirement in requires_dist:
            package_name = self._parse_requirement(requirement)
            if package_name and package_name not in dependencies:
                dependencies.append(package_name)
        
        return dependencies
    
    def _parse_requirement(self, requirement: str):
        requirement = requirement.strip()
        
        for operator in ['==', '!=', '<=', '>=', '<', '>', '~=']:
            if operator in requirement:
                requirement = requirement.split(operator)[0].strip()
        
        if '[' in requirement:
            requirement = requirement.split('[')[0].strip()
        
        if requirement and re.match(r'^[a-zA-Z0-9-_\.]+$', requirement):
            requirement = requirement.replace('_', '-')
            return requirement
        
        return None