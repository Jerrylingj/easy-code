import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent

from tools import ls_tool, text_editor_tool

load_dotenv()

def main():
    print("=" * 60)
    print("Easy Code - a code agent")
    print("=" * 60)
    print()

    # 读取 api_key
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        print("API Key 未设置")
        return

    # 初始化
    model = ChatOpenAI(
        model="deepseek-chat",
        api_key=api_key,
        base_url="https://api.deepseek.com",
        temperature=0,
    )
    print("模型初始化成功! \n")

    # 工具列表
    tools = [ls_tool, text_editor_tool]
    agent = create_agent(model, tools) # 创建一个ReAct Agent
    print(f"工具初始化成功! \n")

    # 对话循环
    print("输入 [quit] 或 [exit] , 结束对话")
    print("-" * 60)
    print()

    while True:
        user_input = input("你: ")

        if (user_input.lower() in ['quit', 'exit']):
            print("再见!")
            break

        # 过滤空值
        if not user_input.strip():
            continue

        # 调用模型
        try:
            print("\nAgent: ", end="", flush=True)
            
            # # 流式输出
            # for chunk in model.stream(user_input):
            #     print(chunk.content, end="", flush=True)
            
            # 使用非流式方便调试
            response = agent.invoke({"messages": [{"role": "user", "content": user_input}]}) 
            # 提取 messages
            messages = response.get("messages", [])
            
            """调试"""
            print("-" * 50)
            print("\r[消息日志(调试用)]: \n")
            for i, message in enumerate(messages, 1):
                role = message.get("role") if isinstance(message, dict) else getattr(message, "type", "?")
                content = message.get("content", "") if isinstance(message, dict) else getattr(message, "content", "")
                print(f" {i}. [{role}]: {content}")
            print("-" * 50)
            
            if messages:
                # TODO: 提取 tool_call 等信息展示思考过程
                last_message = messages[-1] # tool_call也包含在messages中，只有最后一条信息才是最终AI的回复
                print(f"\rAgent: {last_message.content}")
            
            print("\n")  # 换行
        except Exception as e:
            print(f"\n错误: {e}")
            print()

if __name__ == "__main__":
    main()
