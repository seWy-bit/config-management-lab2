from dataclasses import dataclass, field
from typing import List, Dict, Any, Set

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
    all_packages: Dict[str, Package] = field(default_factory=dict)  # name -> Package
    adjacency_list: Dict[str, List[str]] = field(default_factory=dict)  # Граф связей
    
    def add_package(self, package: Package):
        self.all_packages[package.name] = package
        self.adjacency_list[package.name] = package.dependencies
    
    def get_direct_dependencies(self) -> List[str]:
        return self.root_package.dependencies
    
    def get_all_dependencies(self) -> Set[str]:
        return set(self.all_packages.keys()) - {self.root_package.name}
    
    def has_cycle(self) -> bool:
        visited = set()
        recursion_stack = set()
        
        def dfs(package_name: str) -> bool:
            if package_name in recursion_stack:
                return True
            if package_name in visited:
                return False
                
            visited.add(package_name)
            recursion_stack.add(package_name)
            
            for dependency in self.adjacency_list.get(package_name, []):
                if dependency in self.all_packages and dfs(dependency):
                    return True
            
            recursion_stack.remove(package_name)
            return False
        
        for package_name in self.all_packages:
            if dfs(package_name):
                return True
        return False