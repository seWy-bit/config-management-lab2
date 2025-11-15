import os
import subprocess
import sys
from typing import Dict
from src.models import DependencyGraph

class D2Visualizer:
    def __init__(self):
        self.d2_installed = self._check_d2_installation()
    
    def _check_d2_installation(self) -> bool:
        try:
            result = subprocess.run(['d2', '--version'], capture_output=True, text=True)
            return result.returncode == 0
        except FileNotFoundError:
            return False
    
    def generate_d2_code(self, graph: DependencyGraph) -> str:
        d2_lines = []
        
        d2_lines.append("direction: right")
        d2_lines.append("")
        
        for package_name, package in graph.all_packages.items():
            if package_name == graph.root_package.name:
                d2_lines.append(f"{package_name}: {{")
                d2_lines.append("  style: {")
                d2_lines.append('    stroke: "#000"')
                d2_lines.append('    stroke-width: "3"')
                d2_lines.append('    fill: "#e1f5fe"')
                d2_lines.append("  }")
                d2_lines.append("}")
            else:
                d2_lines.append(f"{package_name}")
        
        d2_lines.append("")
        
        for package_name, package in graph.all_packages.items():
            for dependency in package.dependencies:
                if dependency in graph.all_packages:
                    d2_lines.append(f"{package_name} -> {dependency}")
        
        return "\n".join(d2_lines)
    
    def save_d2_file(self, d2_code: str, filename: str) -> str:
        os.makedirs('outputs', exist_ok=True)
        d2_path = os.path.join('outputs', f'{filename}.d2')
        
        with open(d2_path, 'w', encoding='utf-8') as f:
            f.write(d2_code)
        
        return d2_path
    
    def render_svg(self, d2_path: str, filename: str) -> str:
        
        if not self.d2_installed:
            raise Exception("D2 не установлен. Установите D2: https://github.com/terrastruct/d2")
        
        svg_path = os.path.join('outputs', f'{filename}.svg')
        
        try:
            result = subprocess.run([
                'd2', d2_path, svg_path
            ], capture_output=True, text=True, check=True)
            
            return svg_path
        except subprocess.CalledProcessError as e:
            raise Exception(f"Ошибка рендеринга D2: {e.stderr}")
    
    def display_svg_info(self, svg_path: str):
        if os.path.exists(svg_path):
            print(f"SVG изображение сохранено: {svg_path}")
            print(f"Размер файла: {os.path.getsize(svg_path)} байт")
            
            try:
                import webbrowser
                webbrowser.open(svg_path)
                print("Изображение открыто в браузере")
            except Exception:
                print("Не удалось открыть изображение автоматически")
        else:
            print("Ошибка: SVG файл не создан")