"""
专利撰写和审查系统演示

展示如何使用专利 agent 完成各种任务
"""

import asyncio
from agents import Runner

from main_agent import patent_agent


async def demo_patent_drafting():
    """演示专利撰写功能"""
    print("=" * 60)
    print("演示1：专利撰写")
    print("=" * 60)

    prompt = """
    请为我撰写一份发明专利申请文件，要求如下：
    - 发明名称：基于深度学习的智能推荐系统
    - 技术领域：人工智能、机器学习、数据挖掘
    - 发明描述：该系统通过深度学习算法分析用户行为数据，
      包括浏览记录、点击行为、购买历史等，构建用户画像，
      并基于协同过滤和内容推荐技术，为用户提供个性化的商品推荐。
      系统采用多层神经网络架构，包括嵌入层、隐藏层和输出层，
      能够捕捉用户和物品之间的复杂非线性关系。
      通过实时学习用户反馈，不断优化推荐效果，
      显著提高用户满意度和转化率。
    - 申请人：张三科技有限公司
    - 地址：北京市海淀区中关村大街1号
    - 发明人：李四
    """

    result = await Runner.run(patent_agent, prompt)
    print(result.final_output)
    print("\n" + "=" * 60 + "\n")


async def demo_patent_search():
    """演示专利检索功能"""
    print("=" * 60)
    print("演示2：专利检索")
    print("=" * 60)

    prompt = """
    请检索与以下技术相关的专利：
    关键词：人工智能, 推荐系统, 协同过滤
    申请人：阿里巴巴
    """

    result = await Runner.run(patent_agent, prompt)
    print(result.final_output)
    print("\n" + "=" * 60 + "\n")


async def demo_patent_review():
    """演示专利预审功能"""
    print("=" * 60)
    print("演示3：专利预审")
    print("=" * 60)

    # 模拟一个不完整的专利申请
    incomplete_application = """
    专利申请文件

    发明名称：一种智能方法

    申请人：某公司

    发明人：王五

    技术领域：本发明涉及人工智能。

    背景技术：现有技术存在问题。

    发明内容：本发明提供一种解决方案。
    """

    prompt = f"""
    请审查以下专利申请文件，指出存在的问题：
    {incomplete_application}
    """

    result = await Runner.run(patent_agent, prompt)
    print(result.final_output)
    print("\n" + "=" * 60 + "\n")


async def demo_figure_review():
    """演示附图审查功能"""
    print("=" * 60)
    print("演示4：附图审查")
    print("=" * 60)

    prompt = """
    请审查以下专利附图（模拟）：
    - 附图1：系统架构图（PNG格式，300 DPI，2.5MB）
    - 附图2：算法流程图（PNG格式，300 DPI，2.0MB）
    - 附图3：用户界面示意图（PNG格式，300 DPI，3.0MB）

    说明：系统架构图展示了整体架构，算法流程图展示了处理流程，
    用户界面示意图展示了交互界面。
    """

    result = await Runner.run(patent_agent, prompt)
    print(result.final_output)
    print("\n" + "=" * 60 + "\n")


async def demo_rule_configuration():
    """演示规则配置功能"""
    print("=" * 60)
    print("演示5：审查规则配置")
    print("=" * 60)

    prompt = """
    请显示当前所有可用的审查规则，包括预审规则和附图审查规则。
    """

    result = await Runner.run(patent_agent, prompt)
    print(result.final_output)
    print("\n" + "=" * 60 + "\n")


async def demo_comprehensive_workflow():
    """演示完整工作流"""
    print("=" * 60)
    print("演示6：完整专利工作流")
    print("=" * 60)

    prompt = """
    我想申请一个关于"基于区块链的分布式身份认证系统"的发明专利。
    请帮我完成以下工作流程：

    1. 首先撰写一份完整的专利申请文件
    2. 对撰写完成的申请文件进行预审
    3. 检索相关的现有技术，了解技术背景
    4. 附图有3张：系统架构图、区块链结构图、认证流程图

    技术领域：区块链、身份认证、分布式系统

    发明描述：该系统基于区块链技术构建去中心化的身份认证机制，
    通过智能合约管理用户身份信息，使用零知识证明保护隐私，
    支持跨域身份互认，具备高安全性和可扩展性。
    """

    result = await Runner.run(patent_agent, prompt)
    print(result.final_output)
    print("\n" + "=" * 60 + "\n")


async def main():
    """主演示函数"""
    print("\n" + "=" * 60)
    print("专利撰写和审查系统演示")
    print("=" * 60)
    print("\n本演示将展示专利 agent 的各项功能：\n")
    print("1. 专利撰写")
    print("2. 专利检索")
    print("3. 专利预审")
    print("4. 附图审查")
    print("5. 规则配置")
    print("6. 完整工作流")
    print("\n" + "=" * 60 + "\n")

    # 运行所有演示
    try:
        await demo_patent_drafting()
    except Exception as e:
        print(f"演示1出错：{e}\n")

    try:
        await demo_patent_search()
    except Exception as e:
        print(f"演示2出错：{e}\n")

    try:
        await demo_patent_review()
    except Exception as e:
        print(f"演示3出错：{e}\n")

    try:
        await demo_figure_review()
    except Exception as e:
        print(f"演示4出错：{e}\n")

    try:
        await demo_rule_configuration()
    except Exception as e:
        print(f"演示5出错：{e}\n")

    try:
        await demo_comprehensive_workflow()
    except Exception as e:
        print(f"演示6出错：{e}\n")

    print("\n" + "=" * 60)
    print("演示结束")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
