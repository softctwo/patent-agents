"""
专利撰写智能体最终测试

使用优化的提示词直接调用工具函数
"""

import asyncio
import os
from dotenv import load_dotenv
from datetime import datetime

# 加载环境变量
load_dotenv('/Users/zhangyanlong/workspaces/openai-agents-python/.env')

from main_agent import patent_agent
from agents import Runner


async def test_with_tool_call():
    """测试通过Agent调用工具函数"""
    print("\n" + "=" * 70)
    print("🔧 测试：通过Agent调用write_patent_application工具")
    print("=" * 70)

    prompt = """
    请使用 write_patent_application 工具撰写专利申请文件，提供以下所有参数：

    invention_description: 基于深度学习的智能推荐系统，通过卷积神经网络分析用户行为数据，包括浏览记录、点击行为、购买历史等，构建用户画像并实现个性化商品推荐。系统采用多层神经网络架构，包括嵌入层、隐藏层和输出层，能够捕捉用户和物品之间的复杂非线性关系。

    technical_field: 人工智能、机器学习、数据挖掘、深度学习

    patent_type: invention

    background_info: 现有推荐系统主要基于协同过滤和内容过滤，存在冷启动问题、推荐准确率有限、无法捕捉用户兴趣动态变化等问题。传统方法难以处理大规模用户和物品数据。

    specific_problems: 1. 提高推荐准确率；2. 解决冷启动问题；3. 捕捉用户兴趣动态变化；4. 处理大规模数据的高效性

    solution: 采用多层神经网络架构，结合嵌入层、隐藏层和输出层。融合协同过滤和内容推荐技术，实现实时学习用户反馈，不断优化推荐效果。系统包括数据采集模块、特征提取模块、模型训练模块和推荐生成模块。

    beneficial_effects: 推荐准确率提升30%以上，有效解决冷启动问题，提升用户满意度和转化率，计算效率提升50%，系统可扩展性强。

    applicant_name: 智能科技股份有限公司

    applicant_address: 北京市海淀区中关村科技园区创新大厦A座15层

    inventor_name: 张工程师

    请确保调用工具并返回完整结果。
    """

    result = await Runner.run(patent_agent, prompt)
    return result.final_output


async def test_enhanced_prompt():
    """测试增强提示词"""
    print("\n" + "=" * 70)
    print("✨ 测试：增强提示词（无工具调用）")
    print("=" * 70)

    prompt = """
    请直接撰写一份完整的发明专利申请文件，按照以下结构：

    ## 发明名称
    基于深度学习的智能推荐系统

    ## 技术领域
    本发明涉及人工智能技术领域，具体是一种基于深度学习的智能推荐系统。

    ## 背景技术
    现有技术中，推荐系统主要基于协同过滤和内容过滤方法。协同过滤通过分析用户行为相似性进行推荐，但存在冷启动问题；内容过滤依赖物品特征匹配，难以捕捉用户兴趣的复杂变化。传统方法存在以下问题：
    1. 推荐准确率不高
    2. 无法处理冷启动场景
    3. 难以捕捉用户兴趣的动态变化
    4. 计算效率低，难以处理大规模数据

    ## 发明内容
    ### 要解决的技术问题
    本发明要解决的技术问题是：如何提高推荐系统的准确率、解决冷启动问题、捕捉用户兴趣动态变化，并实现高效的大规模数据处理。

    ### 技术解决方案
    本发明提供一种基于深度学习的智能推荐系统，包括以下步骤：
    (1) 数据采集步骤：采集用户行为数据，包括浏览记录、点击行为、购买历史等；
    (2) 特征提取步骤：使用深度神经网络提取用户和物品的特征表示；
    (3) 模型训练步骤：训练多层神经网络，包括嵌入层、隐藏层和输出层；
    (4) 推荐生成步骤：基于训练好的模型生成个性化推荐结果。

    ### 有益效果
    与现有技术相比，本发明具有以下有益效果：
    1. 推荐准确率提升30%以上；
    2. 有效解决冷启动问题；
    3. 提升用户满意度和转化率；
    4. 计算效率提升50%；
    5. 系统可扩展性强。

    ## 附图说明
    图1是本发明系统的整体架构图；
    图2是深度神经网络结构示意图；
    图3是推荐流程图。

    ## 具体实施方式
    下面结合附图详细说明本发明的具体实施方式...

    ## 权利要求书
    1. 一种基于深度学习的智能推荐系统，其特征在于，包括：
    数据采集模块，用于采集用户行为数据；
    特征提取模块，用于提取用户和物品的特征表示；
    模型训练模块，用于训练多层神经网络；
    推荐生成模块，用于生成个性化推荐结果。

    2. 根据权利要求1所述的系统，其特征在于，所述多层神经网络包括嵌入层、隐藏层和输出层。

    3. 根据权利要求1所述的系统，其特征在于，还包括实时学习模块，用于根据用户反馈动态调整模型参数。

    4. 根据权利要求1所述的系统，其特征在于，所述用户行为数据包括浏览记录、点击行为和购买历史。

    5. 根据权利要求1所述的系统，其特征在于，还包括冷启动处理模块，用于处理新用户和新物品的推荐问题。

    申请人：智能科技股份有限公司
    发明人：张工程师
    """

    result = await Runner.run(patent_agent, prompt)
    return result.final_output


async def test_step_by_step():
    """测试分步撰写"""
    print("\n" + "=" * 70)
    print("📋 测试：分步撰写专利")
    print("=" * 70)

    prompt = """
    我需要你分步骤帮我撰写一份专利申请文件。

    第一步：请先写出发明名称、技术领域和背景技术部分。

    发明信息：
    - 名称：智能制造中的质量检测系统
    - 技术领域：智能制造、计算机视觉
    - 申请人：工业科技有限公司
    - 发明人：李工程师

    请开始第一步的撰写。
    """

    result = await Runner.run(patent_agent, prompt)
    return result.final_output


async def analyze_and_save(test_name, content, test_num):
    """分析并保存结果"""
    print(f"\n📊 测试 {test_num} 分析:")
    print("-" * 70)

    lines = content.split('\n')
    chars = len(content)
    words = len(content.split())

    print(f"   总行数: {len(lines)}")
    print(f"   总字符数: {chars}")
    print(f"   总词数: {words}")

    # 检查关键内容
    content_checks = {
        "发明名称": any("发明名称" in line or "名称" in line for line in lines),
        "技术领域": "技术领域" in content,
        "背景技术": "背景技术" in content,
        "发明内容": "发明内容" in content or "要解决的技术问题" in content,
        "有益效果": "有益效果" in content or "有益效果" in content,
        "权利要求": "权利要求" in content,
        "附图说明": "附图说明" in content,
    }

    print(f"\n   包含内容:")
    for item, exists in content_checks.items():
        status = "✓" if exists else "✗"
        print(f"     {status} {item}")

    # 质量评分
    score = sum(content_checks.values()) / len(content_checks) * 100
    print(f"\n   质量评分: {score:.1f}%")

    # 保存单个测试结果
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"test_result_{test_num}_{timestamp}.txt"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"测试 {test_num}: {test_name}\n")
        f.write("=" * 70 + "\n\n")
        f.write(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"字符数: {chars}\n")
        f.write(f"行数: {len(lines)}\n")
        f.write(f"评分: {score:.1f}%\n\n")
        f.write("完整内容:\n")
        f.write("-" * 70 + "\n")
        f.write(content)

    print(f"   💾 已保存到: {filename}")

    return {
        "name": test_name,
        "chars": chars,
        "lines": len(lines),
        "score": score,
        "checks": content_checks
    }


async def main():
    """主测试函数"""
    print("\n" + "=" * 70)
    print("🎯 专利撰写智能体最终测试")
    print("=" * 70)

    # 检查 API
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ 未配置 API 密钥")
        return

    print(f"✓ API 密钥: {api_key[:10]}...")

    # 运行测试
    tests = [
        ("工具函数调用", test_with_tool_call),
        ("增强提示词", test_enhanced_prompt),
        ("分步撰写", test_step_by_step),
    ]

    results = []
    test_num = 0

    for test_name, test_func in tests:
        test_num += 1
        try:
            print(f"\n⏳ 正在运行: {test_name}...")
            content = await test_func()
            result = await analyze_and_save(test_name, content, test_num)
            results.append(result)

            # 显示前200字符作为预览
            print(f"\n   📄 内容预览:")
            print("   " + "-" * 66)
            preview = content[:200].replace('\n', '\n   ')
            print(f"   {preview}...")
            print("   " + "-" * 66)

        except Exception as e:
            print(f"❌ {test_name} 失败: {e}")
            results.append({
                "name": test_name,
                "error": str(e)
            })

    # 生成最终报告
    print("\n" + "=" * 70)
    print("📈 最终测试报告")
    print("=" * 70)

    successful_tests = [r for r in results if "error" not in r]
    print(f"\n✅ 成功测试: {len(successful_tests)}/{len(results)}")

    if successful_tests:
        avg_score = sum(r["score"] for r in successful_tests) / len(successful_tests)
        print(f"📊 平均评分: {avg_score:.1f}%")

        print(f"\n🏆 最佳测试:")
        best = max(successful_tests, key=lambda x: x["score"])
        print(f"   {best['name']}: {best['score']:.1f}%")

    # 详细结果表
    print(f"\n📋 详细结果:")
    print("-" * 70)
    print(f"{'测试名称':<20} {'评分':<10} {'字符数':<10} {'行数':<8}")
    print("-" * 70)
    for r in successful_tests:
        print(f"{r['name']:<20} {r['score']:<10.1f} {r['chars']:<10} {r['lines']:<8}")

    print("\n" + "=" * 70)
    if avg_score >= 80:
        print("🎉 优秀！专利撰写智能体表现良好！")
    elif avg_score >= 60:
        print("👍 良好！专利撰写智能体基本可用")
    else:
        print("⚠️ 需要改进！专利撰写智能体需要优化")

    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())
