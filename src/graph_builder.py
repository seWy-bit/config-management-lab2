from typing import Dict, Set, List
from src.models import Package, DependencyGraph
from src.dependency_fetcher import DependencyFetcher
from src.config import Config

class GraphBuilder:
    def __init__(self, config: Config, fetcher: DependencyFetcher):
        self.config = config
        self.fetcher = fetcher
        self.visited: Set[str] = set()
        self.cycles_detected: Set[str] = set()
    
    def build_dependency_graph(self) -> DependencyGraph:
        if self.config.test_mode and self.config.output:
            all_packages = self.fetcher.load_entire_test_repository()
            root_package = all_packages.get(self.config.package_name)
            if not root_package:
                root_package = Package(
                    name=self.config.package_name,
                    version=self.config.version,
                    dependencies=[]
                )
            graph = DependencyGraph(root_package=root_package)
            for package in all_packages.values():
                graph.add_package(package)
            return graph
        
        if self.config.test_mode and self.config.reverse:
            all_packages = self.fetcher.load_entire_test_repository()
            root_package = all_packages.get(self.config.package_name)
            if not root_package:
                root_package = Package(
                    name=self.config.package_name,
                    version=self.config.version,
                    dependencies=[]
                )
            graph = DependencyGraph(root_package=root_package)
            for package in all_packages.values():
                graph.add_package(package)
            return graph

        root_package = self.fetcher.fetch_dependencies()
        graph = DependencyGraph(root_package=root_package)
        graph.add_package(root_package)
        
        self._bfs_with_recursion(root_package.name, graph, current_depth=0)
        
        return graph
    
    def _bfs_with_recursion(self, package_name: str, graph: DependencyGraph, current_depth: int):
        if current_depth >= self.config.max_depth:
            return
        
        if package_name in self.visited:
            self.cycles_detected.add(package_name)
            return
        
        package = graph.all_packages.get(package_name)
        if not package:
            return
        
        self.visited.add(package_name)
        
        for dependency_name in package.dependencies:
            if dependency_name not in graph.all_packages:
                try:
                    temp_config = type(self.config)({
                        'package_name': dependency_name,
                        'repository': self.config.repository,
                        'test_mode': self.config.test_mode,
                        'version': 'latest',
                        'max_depth': self.config.max_depth
                    })
                    
                    temp_fetcher = DependencyFetcher(temp_config)
                    dependency_package = temp_fetcher.fetch_dependencies()
                    graph.add_package(dependency_package)
                    
                except Exception as e:
                    graph.add_package(Package(
                        name=dependency_name, 
                        version="unknown", 
                        dependencies=[]
                    ))
            
            self._bfs_with_recursion(dependency_name, graph, current_depth + 1)
        
        self.visited.remove(package_name)
    
    def find_reverse_dependencies(self, graph: DependencyGraph, target_package: str) -> List[str]:
        reverse_deps = []
        for package_name, package in graph.all_packages.items():
            if target_package in package.dependencies:
                reverse_deps.append(package_name)
        return reverse_deps