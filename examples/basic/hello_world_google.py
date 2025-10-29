import asyncio
import os

from agents import Agent, Runner, set_tracing_disabled

"""
使用 Google Gemini 模型运行 hello_world 示例

需要设置环境变量：
export GOOGLE_API_KEY="your_google_api_key_here"

支持的 Gemini 模型：
- gemini/gemini-2.0-flash
- gemini/gemini-pro
- gemini/gemini-1.5-pro

更多模型信息请参考：https://docs.litellm.ai/docs/providers
"""

# 禁用跟踪以简化输出
set_tracing_disabled(disabled=True)


async def main():
    # 检查是否设置了 Google API key
    if not os.getenv("GOOGLE_API_KEY"):
        print("错误：请设置 GOOGLE_API_KEY 环境变量")
        print("例如：export GOOGLE_API_KEY='your_google_api_key_here'")
        print("\n获取 API key 请访问：https://aistudio.google.com/app/apikey")
        return

    # 使用 LitellmModel 配置 Google Gemini 模型
    from agents.extensions.models.litellm_model import LitellmModel

    model = LitellmModel(
        model="gemini/gemini-2.0-flash-exp",
        api_key=os.getenv("GOOGLE_API_KEY")
    )

    agent = Agent(
        name="Assistant",
        instructions="You only respond in haikus.",
        model=model,
    )

    print("正在运行 Google Gemini 2.0 Flash 模型...")
    print("输入：Tell me about recursion in programming.\n")

    result = await Runner.run(agent, "Tell me about recursion in programming.")

    print("输出：")
    print(result.final_output)
    print("\n✅ 测试成功完成！")


if __name__ == "__main__":
    asyncio.run(main())
