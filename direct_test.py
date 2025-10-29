"""
直接测试专利撰写 - 不询问，直接生成

使用明确的指令要求模型直接生成内容
"""

import asyncio
import os
from dotenv import load_dotenv
from datetime import datetime

# 加载环境变量
load_dotenv('/Users/zhangyanlong/workspaces/openai-agents-python/.env')

from main_agent import patent_agent
from agents import Runner


async def test_direct_generation():
    """测试直接生成（不询问）"""
    print("\n" + "=" * 70)
    print("🎯 测试：直接生成专利内容（明确指令）")
    print("=" * 70)

    prompt = """
    重要：请不要询问任何问题，直接生成一份完整的专利申请文件。

    基于以下信息生成专利：

    发明名称：智能推荐系统
    技术领域：人工智能
    申请人：ABC公司
    发明人：张三

    现有技术问题：推荐准确率低、冷启动问题
    解决方案：使用深度学习分析用户行为
    有益效果：准确率提升30%

    请直接生成包含以下章节的完整专利文件：
    1. 发明名称
    2. 技术领域
    3. 背景技术
    4. 发明内容
    5. 附图说明
    6. 具体实施方式
    7. 权利要求书

    不要询问任何信息，直接开始撰写！
    """

    result = await Runner.run(patent_agent, prompt)
    return result.final_output


async def test_force_content():
    """测试强制生成内容"""
    print("\n" + "=" * 70)
    print("💪 测试：强制生成专利内容")
    print("=" * 70)

    prompt = """
    任务：现在就开始撰写专利申请文件，不要问任何问题！

    我已经提供了所有必要信息：
    - 发明：智能推荐系统
    - 领域：人工智能
    - 公司：ABC公司
    - 发明人：张三

    开始撰写专利文件，包括：
    1. 发明名称：智能推荐系统
    2. 技术领域：本发明涉及人工智能技术领域
    3. 背景技术：现有推荐系统存在...（请补充）
    4. 发明内容：要解决...（请补充）
    5. 权利要求：请写5项权利要求

    立即开始，不要停顿！
    """

    result = await Runner.run(patent_agent, prompt)
    return result.final_output


async def test_step_by_step_fixed():
    """测试分步并提供所有信息"""
    print("\n" + "=" * 70)
    print("📋 测试：分步+完整信息")
    print("=" * 70)

    prompt = """
    我将提供完整信息，请直接撰写第一步：发明名称、技术领域和背景技术。

    【完整信息】
    发明名称：基于深度学习的智能推荐系统
    技术领域：人工智能、机器学习、数据挖掘
    申请人：智能科技股份有限公司
    地址：北京市海淀区中关村大街1号
    发明人：李工程师
    国籍：中国

    背景技术：
    现有推荐系统主要基于协同过滤和内容过滤方法。
    协同过滤通过分析用户行为相似性进行推荐，但存在冷启动问题；
    内容过滤依赖物品特征匹配，难以捕捉用户兴趣的复杂变化。
    传统方法存在推荐准确率不高、无法处理冷启动场景等问题。

    请直接开始撰写，不要再问任何问题！
    """

    result = await Runner.run(patent_agent, prompt)
    return result.final_output


async def test_gemini_direct():
    """测试 Gemini 直接能力"""
    print("\n" + "=" * 70)
    print("✨ 测试：直接使用 Gemini 生成")
    print("=" * 70)

    # 使用更简单的prompt
    prompt = """
    写一份专利申请文件的示例，包括发明名称、技术领域、背景技术、发明内容、权利要求。
    主题：智能推荐系统
    """

    result = await Runner.run(patent_agent, prompt)
    return result.final_output


async def analyze_test(name, content):
    """分析测试结果"""
    print(f"\n📊 {name} 分析:")
    print("-" * 70)

    lines = content.split('\n')
    chars = len(content)

    # 详细分析
    has_title = any("发明名称" in line or "名称" in line for line in lines)
    has_field = "技术领域" in content
    has_bg = "背景技术" in content
    has_content = "发明内容" in content or "要解决" in content
    has_claims = "权利要求" in content
    has_effects = "有益效果" in content

    print(f"字符数: {chars}")
    print(f"行数: {len(lines)}")
    print(f"\n包含章节:")
    print(f"  {'✓' if has_title else '✗'} 发明名称")
    print(f"  {'✓' if has_field else '✗'} 技术领域")
    print(f"  {'✓' if has_bg else '✗'} 背景技术")
    print(f"  {'✓' if has_content else '✗'} 发明内容")
    print(f"  {'✓' if has_claims else '✗'} 权利要求")
    print(f"  {'✓' if has_effects else '✗'} 有益效果")

    sections = [has_title, has_field, has_bg, has_content, has_claims]
    score = sum(sections) / len(sections) * 100
    print(f"\n质量评分: {score:.1f}%")

    # 保存结果
    timestamp = datetime.now().strftime('%H%M%S')
    filename = f"direct_test_{timestamp}.txt"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"{name}\n")
        f.write("=" * 70 + "\n\n")
        f.write(content)

    print(f"💾 已保存: {filename}")

    # 显示前300字符
    print(f"\n📄 内容预览:")
    print("  " + "-" * 66)
    preview = content[:300].replace('\n', '\n  ')
    print(f"  {preview}...")
    print("  " + "-" * 66)

    return {
        "name": name,
        "chars": chars,
        "score": score,
        "sections": {
            "发明名称": has_title,
            "技术领域": has_field,
            "背景技术": has_bg,
            "发明内容": has_content,
            "权利要求": has_claims,
            "有益效果": has_effects,
        }
    }


async def main():
    """主测试"""
    print("\n" + "=" * 70)
    print("🔬 专利撰写智能体 - 直接生成测试")
    print("=" * 70)

    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ 未配置 API")
        return

    print(f"✓ API: {api_key[:10]}...")

    tests = [
        ("直接生成", test_direct_generation),
        ("强制内容", test_force_content),
        ("完整信息", test_step_by_step_fixed),
        ("简单示例", test_gemini_direct),
    ]

    results = []

    for name, test in tests:
        print(f"\n⏳ 正在测试: {name}...")
        try:
            content = await test()
            result = await analyze_test(name, content)
            results.append(result)
        except Exception as e:
            print(f"❌ 失败: {e}")
            results.append({"name": name, "error": str(e)})

    # 总结
    print("\n" + "=" * 70)
    print("🏁 测试总结")
    print("=" * 70)

    successful = [r for r in results if "error" not in r]

    if successful:
        avg = sum(r["score"] for r in successful) / len(successful)
        print(f"✅ 成功: {len(successful)}/{len(results)}")
        print(f"📊 平均分: {avg:.1f}%")

        best = max(successful, key=lambda x: x["score"])
        print(f"🏆 最佳: {best['name']} ({best['score']:.1f}%)")

        print(f"\n📋 详细评分:")
        for r in successful:
            print(f"  {r['name']:<20} {r['score']:>6.1f}%")

    # 结论
    print("\n" + "=" * 70)
    if avg >= 80:
        print("🎉 优秀！智能体表现良好")
    elif avg >= 60:
        print("👍 良好！基本可用")
    elif avg >= 40:
        print("⚠️ 一般，需要改进")
    else:
        print("❌ 较差，需大幅优化")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())
