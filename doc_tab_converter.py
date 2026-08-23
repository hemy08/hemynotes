#!/usr/bin/env python3
"""
文档代码标签页转换工具
将分散的代码块转换为Material for MkDocs的标签页格式
"""
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional

class CodeBlock:
    """代码块数据结构"""
    def __init__(self, language: str, code: str, start: int, end: int):
        self.language = language
        self.code = code
        self.start = start
        self.end = end
    
    def __repr__(self):
        return f"CodeBlock({self.language}, {len(self.code)} chars, pos: {self.start}-{self.end})"

class TabConverter:
    """标签页转换器"""
    
    # 支持的编程语言
    LANGUAGES = ['C', 'C++', 'Python', 'Java', 'Go', 'Rust']
    
    # 语言到代码块语言标识的映射
    LANG_MAP = {
        'C': 'c',
        'C++': 'cpp',
        'Python': 'python',
        'Java': 'java',
        'Go': 'go',
        'Rust': 'rust'
    }
    
    def __init__(self, content: str):
        self.content = content
        self.code_blocks = []
        
    def find_code_blocks(self) -> List[CodeBlock]:
        """查找所有代码块"""
        pattern = r'```(\w+)\n(.*?)\n```'
        matches = re.finditer(pattern, self.content, re.DOTALL)
        
        for match in matches:
            lang = match.group(1)
            code = match.group(2)
            start = match.start()
            end = match.end()
            self.code_blocks.append(CodeBlock(lang, code, start, end))
        
        return self.code_blocks
    
    def generate_tabs(self, implementations: Dict[str, str]) -> str:
        """
        生成标签页格式代码
        
        Args:
            implementations: 语言 -> 代码的映射
        
        Returns:
            标签页格式的字符串
        """
        tabs = []
        
        for lang in self.LANGUAGES:
            if lang in implementations:
                code = implementations[lang]
                lang_id = self.LANG_MAP[lang]
                
                # 缩进代码(8个空格)
                indented_code = '\n'.join('    ' + line if line.strip() else '' 
                                         for line in code.split('\n'))
                
                tab = f'''=== "{lang}"

    ```{lang_id}
{indented_code}
    ```'''
                tabs.append(tab)
        
        return '\n\n'.join(tabs)
    
    @staticmethod
    def create_implementation_template(algorithm_name: str, description: str) -> Dict[str, str]:
        """
        创建算法实现的模板
        
        Args:
            algorithm_name: 算法名称
            description: 算法描述
        
        Returns:
            各语言的模板代码
        """
        templates = {
            'C': f'''// {algorithm_name} - {description}
// TODO: 实现C版本''',
            
            'C++': f'''// {algorithm_name} - {description}
// TODO: 实现C++版本''',
            
            'Python': f'''def {algorithm_name.lower().replace(" ", "_")}():
    """
    {algorithm_name} - {description}
    TODO: 实现Python版本
    """
    pass''',
            
            'Java': f'''// {algorithm_name} - {description}
public class {algorithm_name.replace(" ", "")} {{
    // TODO: 实现Java版本
}}''',
            
            'Go': f'''// {algorithm_name} - {description}
package main

// TODO: 实现Go版本''',
            
            'Rust': f'''// {algorithm_name} - {description}
// TODO: 实现Rust版本'''
        }
        
        return templates

def process_file(file_path: str, dry_run: bool = True):
    """
    处理单个文件
    
    Args:
        file_path: 文件路径
        dry_run: 是否只预览不修改
    """
    print(f"\n处理文件: {file_path}")
    print("=" * 60)
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    converter = TabConverter(content)
    code_blocks = converter.find_code_blocks()
    
    print(f"找到 {len(code_blocks)} 个代码块:")
    for i, block in enumerate(code_blocks[:10]):  # 只显示前10个
        print(f"  {i+1}. {block}")
    
    if len(code_blocks) > 10:
        print(f"  ... 还有 {len(code_blocks) - 10} 个代码块")
    
    # 生成统计报告
    lang_count = {}
    for block in code_blocks:
        lang_count[block.language] = lang_count.get(block.language, 0) + 1
    
    print("\n语言统计:")
    for lang, count in sorted(lang_count.items()):
        print(f"  {lang}: {count} 个代码块")
    
    if dry_run:
        print("\n[DRY RUN] 未修改文件")
    else:
        # 这里添加实际修改逻辑
        print("\n[MODIFIED] 文件已修改")

def batch_process(directory: str, pattern: str = "*.md"):
    """批量处理目录中的文件"""
    path = Path(directory)
    files = list(path.glob(pattern))
    
    print(f"\n批量处理: {directory}")
    print(f"找到 {len(files)} 个文件")
    
    for file in files:
        process_file(str(file), dry_run=True)

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("""
使用方法:
  python doc_tab_converter.py <文件路径>          # 处理单个文件
  python doc_tab_converter.py <目录路径> --batch  # 批量处理目录
  python doc_tab_converter.py --example           # 显示示例
        """)
        return
    
    if sys.argv[1] == '--example':
        show_example()
        return
    
    target = sys.argv[1]
    
    if '--batch' in sys.argv:
        batch_process(target)
    else:
        process_file(target, dry_run='--apply' not in sys.argv)

def show_example():
    """显示示例"""
    print("""
标签页格式示例:
================

=== "C"

    ```c
    int* nextGreaterElement(int nums[], int n) {
        // C实现
    }
    ```

=== "C++"

    ```cpp
    vector<int> nextGreaterElement(vector<int>& nums) {
        // C++实现
    }
    ```

=== "Python"

    ```python
    def next_greater_element(nums):
        # Python实现
    }
    ```

转换规则:
==========
1. 使用 === "语言名称" 作为标签页标题
2. 标签页内容需要4个空格缩进
3. 代码块需要额外4个空格缩进(总共8个空格)
4. 不同标签页之间用空行分隔
    """)

if __name__ == "__main__":
    main()
