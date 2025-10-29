"""
测试 Gemini 集成的专利 Agent

运行各种测试以验证功能
"""

import asyncio
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv('/Users/zhangyanlong/workspaces/openai-agents-python/.env')

from main_agent import patent_agent
from agents import Runner


async def test_patent_writing():
    """测试专利撰写功能"""
    print("\n" + "=" * 60)
    print("测试 1: 专利撰写功能")
    print("=" * 60)

    prompt = """
    请为以下发明撰写一份发明专利申请文件：

    发明名称：基于人工智能的智能推荐系统
    技术领域：人工智能、机器学习、数据挖掘
    发明描述：一种基于深度学习的智能推荐系统，通过神经网络分析用户行为数据，
              包括浏览记录、点击行为、购买历史等，构建用户画像，
              并基于协同过滤和内容推荐技术，为用户提供个性化的商品推荐。
              系统采用多层神经网络架构，能够捕捉用户和物品之间的复杂非线性关系。
              通过实时学习用户反馈，不断优化推荐效果。
    申请人：张三科技有限公司
    发明人：李四
    """

    result = await Runner.run(patent_agent, prompt)
    print(result.final_output[:500] + "...")
    print("\n✓ 专利撰写测试完成")


async def test_patent_review():
    """测试专利审查功能"""
    print("\n" + "=" * 60)
    print("测试 2: 专利审查功能")
    print("=" * 60)

    application_text = """
    发明名称：一种方法
    技术领域：人工智能
    背景技术：现有技术存在问题。
    发明内容：本发明提供一种解决方案。
    """

    prompt = f"""
    请审查以下专利申请文件，指出存在的问题：
    {application_text}
    """

    result = await Runner.run(patent_agent, prompt)
    print(result.final_output[:500] + "...")
    print("\n✓ 专利审查测试完成")


async def test_patent_search():
    """测试专利检索功能"""
    print("\n" + "=" * 60)
    print("测试 3: 专利检索功能")
    print("=" * 60)

    prompt = """
    请检索与以下技术相关的专利：
    关键词：人工智能, 推荐系统, 协同过滤
    申请人：清华大学
    """

    result = await Runner.run(patent_agent, prompt)
    print(result.final_output[:500] + "...")
    print("\n✓ 专利检索测试完成")


async def test_figure_review():
    """测试附图审查功能"""
    print("\n" + "=" * 60)
    print("测试 4: 附图审查功能")
    print("=" * 60)

    prompt = """
    请审查以下专利附图（模拟）：
    - 附图1：系统架构图（PNG格式，300 DPI，2.5MB）
    - 附图2：算法流程图（PNG格式，300 DPI，2.0MB）
    - 附图3：用户界面示意图（PNG格式，300 DPI，3.0MB）

    说明：系统架构图展示了整体架构，算法流程图展示了处理流程。
    """

    result = await Runner.run(patent_agent, prompt)
    print(result.final_output[:500] + "...")
    print("\n✓ 附图审查测试完成")


async def test_rule_configuration():
    """测试规则配置功能"""
    print("\n" + "=" * 60)
    print("测试 5: 规则配置功能")
    print("=" * 60)

    prompt = "请显示当前所有可用的审查规则"

    result = await Runner.run(patent_agent, prompt)
    print(result.final_output)
    print("\n✓ 规则配置测试完成")


async def test_comprehensive_workflow():
    """测试完整工作流"""
    print("\n" + "=" * 60)
    print("测试 6: 完整工作流")
    print("=" * 60)

    prompt = """
    我想申请一个关于"基于区块链的分布式身份认证系统"的发明专利。
    请帮我完成以下工作流程：

    1. 首先撰写一份完整的专利申请文件
    2. 对撰写完成的申请文件进行预审
    3. 检索相关的现有技术，了解技术背景

    技术领域：区块链、身份认证、分布式系统
    发明描述：该系统基于区块链技术构建去中心化的身份认证机制，
              通过智能合约管理用户身份信息，使用零知识证明保护隐私，
              支持跨域身份互认，具备高安全性和可扩展性。
    """

    result = await Runner.run(patent_agent, prompt)
    print(result.final_output[:800] + "...")
    print("\n✓ 完整工作流测试完成")


async def main():
    """主测试函数"""
    print("\n" + "=" * 60)
    print("🔬 Gemini 驱动的专利 Agent 测试")
    print("=" * 60)

    # 检查 API 配置
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ 错误：未设置 GOOGLE_API_KEY 环境变量")
        print("请设置：export GOOGLE_API_KEY='your_api_key'")
        return

    print(f"✓ API 密钥已配置：{api_key[:10]}...")

    # 运行所有测试
    tests = [
        test_patent_writing,
        test_patent_review,
        test_patent_search,
        test_figure_review,
        test_rule_configuration,
        test_comprehensive_workflow,
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            await test()
            passed += 1
        except Exception as e:
            print(f"\n❌ 测试失败：{e}")
            failed += 1

    # 测试总结
    print("\n" + "=" * 60)
    print("📊 测试总结")
    print("=" * 60)
    print(f"✓ 通过：{passed}")
    print(f"✗ 失败：{failed}")
    print(f"总计：{passed + failed}")
    print(f"成功率：{passed / (passed + failed) * 100:.1f}%")

    if failed == 0:
        print("\n🎉 所有测试通过！")
    else:
        print(f"\n⚠️ {failed} 个测试失败")

    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
