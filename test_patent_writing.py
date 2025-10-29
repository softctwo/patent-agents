"""
测试 Gemini 专利撰写功能

专门测试专利撰写智能体
"""

import asyncio
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv('/Users/zhangyanlong/workspaces/openai-agents-python/.env')

from main_agent import patent_agent
from agents import Runner


async def test_writing():
    """测试专利撰写"""
    print("=" * 60)
    print("🔬 测试 Gemini 专利撰写功能")
    print("=" * 60)

    # 检查 API 配置
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ 错误：未设置 GOOGLE_API_KEY 环境变量")
        print("请设置：export GOOGLE_API_KEY='your_api_key'")
        return

    print(f"✓ API 密钥已配置：{api_key[:10]}...")

    prompt = """
    请为以下发明撰写一份发明专利申请文件：

    发明名称：基于深度学习的智能推荐系统
    技术领域：人工智能、机器学习、数据挖掘
    发明描述：一种基于深度学习的智能推荐系统，通过神经网络分析用户行为数据，
              包括浏览记录、点击行为、购买历史等，构建用户画像，
              并基于协同过滤和内容推荐技术，为用户提供个性化的商品推荐。
              系统采用多层神经网络架构，包括嵌入层、隐藏层和输出层，
              能够捕捉用户和物品之间的复杂非线性关系。
              通过实时学习用户反馈，不断优化推荐效果，
              显著提高用户满意度和转化率。
    申请人：张三科技有限公司
    地址：北京市海淀区中关村大街1号
    发明人：李四
    """

    print("\n📝 正在生成专利申请文件...")
    print("-" * 60)

    result = await Runner.run(patent_agent, prompt)

    # 保存结果
    output = result.final_output
    print("\n" + "=" * 60)
    print("📄 生成结果")
    print("=" * 60)
    print(output)

    # 保存到文件
    with open("patent_writing_test_result.txt", "w", encoding="utf-8") as f:
        f.write("Gemini 专利撰写测试结果\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"测试时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("输入：\n")
        f.write(prompt.strip() + "\n\n")
        f.write("=" * 60 + "\n\n")
        f.write("输出：\n")
        f.write(output)

    print("\n✅ 测试完成，结果已保存到 patent_writing_test_result.txt")


if __name__ == "__main__":
    from datetime import datetime
    asyncio.run(test_writing())
