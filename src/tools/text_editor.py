import os
from typing import Literal
from langchain_core.tools import tool

class TextEditor:
    """提供文件操作功能"""
    
    @staticmethod
    def view(file_path: str, start_line: int = None, end_line: int = None) -> str:
        """读取文件内容"""
        if not os.path.exists(file_path):
            return f"错误: 文件不存在: {file_path}"
        
        if os.path.isdir(file_path):
            return f"错误: 该文件路径是一个目录, 不是文件: {file_path}"

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            if start_line is None: start_line = 1
            if end_line is None: end_line = len(lines)

            start_line = max(1, start_line)
            end_line = min(len(lines), end_line)

            selected_lines = lines[start_line - 1 : end_line]

            result = []
            for i, line in enumerate(selected_lines, start=start_line):
                result.append(f"{i: 4d} | {line.rstrip()}")
                
            return "\n".join(result)
            
        except Exception as e:
            return f"错误: 读取文件失败{e}"
    
    @staticmethod
    def create(file_path: str, content: str):
        """创建新文件"""
        if os.path.exists(file_path):
            return f"错误: 文件已存在 {file_path}\n(如果要修改文件, 请使用str_replace命令)"

        try:
            directory = os.path.dirname(file_path)
            
            # 不存在则创建目录
            if directory and not os.path.exists(directory):
                os.makedirs(directory)
            
            # 'w'模式会清空原内容，但是由于是创建新文件，问题不大
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            line_count = len(content.split('\n'))

            return f"文件创建成功: {file_path}, 共 {line_count} 行"
        
        except Exception as e:
            return f"错误: 创建文件失败: {e}"
    
    @staticmethod
    def str_replace(file_path: str, old_str: str, new_str: str) -> str:
        """替换文件中字符串"""
        if not os.path.exists(file_path):
            return f"错误: 文件不存在: {file_path}"
        
        if os.path.isdir(file_path):
            return f"错误: 该文件路径是一个目录, 不是文件: {file_path}"

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if old_str not in content:
                return f"错误: 在文件中找不到要替换的内容\n(当前正在查找: {old_str[:50]})"

            # 只替换第一个
            new_content = content.replace(old_str, new_str, 1)

            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            return f"替换成功: {file_path}\n{old_str} -> {new_str}"
        except Exception as e:
            return f"错误: 替换失败: {e}"

@tool("text_editor")
def text_editor_tool(
    command: Literal["view", "create", "str_replace"],
    file_path: str,
    start_line: int = None,
    end_line: int = None,
    content: str = None,
    old_str: str = None,
    new_str: str = None,    
) -> str:
    """文本编辑工具, 用于查看, 创建, 编辑文件"""

    editor = TextEditor()

    if command == "view":
        return editor.view(file_path, start_line, end_line)
    elif command == "create":
        if content is None:
            return "错误: create需要content!"
        return editor.create(file_path, content)
    elif command == "str_replace":
        if old_str is None or new_str is None:
            return "错误: str_replace需要old_str和new_str"
        return editor.str_replace(file_path, old_str, new_str)
    else:
        return f"错误: 未知命令: {command}\n(支持的命令: view, create, str_replace)"
