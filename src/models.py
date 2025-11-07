from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class Package:
    name: str
    version: str
    dependencies: List[str]  # Список прямых зависимостей
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'name': self.name,
            'version': self.version,
            'dependencies': self.dependencies
        }

@dataclass
class DependencyGraph:
    root_package: Package
    all_dependencies: Dict[str, Package]  # name -> Package
    
    def get_direct_dependencies(self) -> List[str]:
        return self.root_package.dependencies