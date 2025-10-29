"""
直接测试专利撰写工具函数

使用更简单的方式测试
"""

import asyncio
import os
from dotenv import load_dotenv
from datetime import datetime

# 加载环境变量
load_dotenv('/Users/zhangyanlong/workspaces/openai-agents-python/.env')

from main_agent import write_patent_application, patent_agent
from agents import Runner


async def test_tools_directly():
    """直接测试工具函数"""
    print("=" * 60)
    print("🔬 直接测试专利撰写工具函数")
    print("=" * 60)

    # 检查 API 配置
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ 错误：未设置 GOOGLE_API_KEY 环境变量")
        return

    print(f"✓ API 密钥已配置：{api_key[:10]}...")

    # 使用 agent 调用工具
    prompt = """
    请使用 write_patent_application 工具撰写一份专利申请文件，提供以下参数：
    - invention_description: 基于深度学习的智能推荐系统，通过神经网络分析用户行为数据，实现个性化推荐
    - technical_field: 人工智能、机器学习、数据挖掘
    - patent_type: invention
    - applicant_name: 张三科技有限公司
    - applicant_address: 北京市海淀区中关村大街1号
    - inventor_name: 李四
    """

    print("\n📝 正在调用工具...")
    print("-" * 60)

    result = await Runner.run(patent_agent, prompt)

    # 保存结果
    output = result.final_output
    print("\n" + "=" * 60)
    print("📄 工具执行结果")
    print("=" * 60)
    print(output)

    # 保存到文件
    with open("patent_tools_test_result.txt", "w", encoding="utf-8") as f:
        f.write("Gemini 专利撰写工具直接测试结果\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"测试时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"API 密钥：{api_key[:10]}...\n\n")
        f.write("请求：\n")
        f.write("-" * 60 + "\n")
        f.write(prompt.strip() + "\n\n")
        f.write("=" * 60 + "\n\n")
        f.write("响应：\n")
        f.write("-" * 60 + "\n")
        f.write(output)
        f.write("\n\n" + "=" * 60 + "\n")

    print(f"\n✅ 测试完成，结果已保存到：patent_tools_test_result.txt")


async def test_simple_question():
    """测试简单问题"""
    print("\n" + "=" * 60)
    print("🔬 测试简单问题")
    print("=" * 60)

    prompt = "你好，请简单介绍一下你的功能。"

    result = await Runner.run(patent_agent, prompt)
    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(test_simple_question())
    asyncio.run(test_tools_directly())
