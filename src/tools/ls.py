import os
from langchain_core.tools import tool

@tool("ls")
def ls_tool(path: str) -> str:
    """
    在指定目录下执行`ls`
    """

    if not os.path.exists(path):
        return f"路径{path}不存在!"

    if not os.path.isdir(path):
        return f"{path} 不是一个目录!"
    
    try:
        items = []
        for item in os.listdir(path):
            item_path = os.path.join(path, item)

            # 区分文件和目录
            if os.path.isdir(item_path):
                items.append(f"{item}/")  # 目录
            else:
                items.append(item)
        
        items.sort()

        if items:
            return "\n".join(items)
        else:
            return "目录为空"
    except Exception as e:
        return f"错误, {e}"
