import asyncio
import os

from agents import Agent, Runner, function_tool, set_tracing_disabled
from agents.extensions.models.litellm_model import LitellmModel

"""
使用 LitellmModel 直接配置 Google Gemini 模型

需要设置环境变量：
export GOOGLE_API_KEY="your_google_api_key_here"

支持的 Gemini 模型：
- gemini/gemini-2.0-flash
- gemini/gemini-pro
- gemini/gemini-1.5-pro

这种方法允许你更灵活地配置模型参数。
"""

# 禁用跟踪以简化输出
set_tracing_disabled(disabled=True)


@function_tool
def get_weather(city: str):
    """获取指定城市的天气信息"""
    print(f"[工具调用] 获取 {city} 的天气信息")
    return f"The weather in {city} is sunny."


async def main():
    # 检查是否设置了 Google API key
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("错误：请设置 GOOGLE_API_KEY 环境变量")
        print("例如：export GOOGLE_API_KEY='your_google_api_key_here'")
        print("\n获取 API key 请访问：https://aistudio.google.com/app/apikey")
        return

    # 使用 LitellmModel 配置 Google Gemini 模型
    model = LitellmModel(
        model="gemini/gemini-2.0-flash-exp",
        api_key=api_key
    )

    agent = Agent(
        name="Assistant",
        instructions="You only respond in haikus.",
        model=model,
        tools=[get_weather],
    )

    print("正在运行 Google Gemini 2.0 Flash 模型（使用 LitellmModel）...")
    print("输入：What's the weather in Tokyo?\n")

    result = await Runner.run(
        agent,
        "What's the weather in Tokyo?"
    )

    print("输出：")
    print(result.final_output)
    print("\n✅ 测试成功完成！")


if __name__ == "__main__":
    asyncio.run(main())
