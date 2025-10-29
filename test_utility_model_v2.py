"""
测试优化后的实用新型Agent v2.0

验证优化效果，特别是"要解决的技术问题"章节
"""

import asyncio
import os
from dotenv import load_dotenv
from datetime import datetime

# 加载环境变量
load_dotenv('/Users/zhangyanlong/workspaces/openai-agents-python/.env')

from utility_model_agent import utility_model_agent
from agents import Runner


def analyze_result_v2(test_name, content):
    """分析测试结果"""
    lines = content.split('\n')
    chars = len(content)

    # 检查所有8个章节
    expected_sections = [
        "发明名称",
        "技术领域",
        "背景技术",
        "要解决的技术问题",
        "技术方案",
        "有益效果",
        "附图说明",
        "权利要求",
    ]

    found_sections = []
    missing_sections = []

    for section in expected_sections:
        if any(section in line or section in content for line in lines):
            found_sections.append(section)
        else:
            missing_sections.append(section)

    # 计算分数
    score = len(found_sections) / len(expected_sections) * 100

    # 质量评估
    if score >= 90:
        quality = "🎉 优秀"
    elif score >= 80:
        quality = "👍 良好"
    elif score >= 60:
        quality = "⚠️ 一般"
    else:
        quality = "❌ 较差"

    print(f"\n   字符数: {chars}")
    print(f"   行数: {len(lines)}")
    print(f"\n   包含章节 ({score:.1f}%):")
    for section in found_sections:
        print(f"     ✓ {section}")
    for section in missing_sections:
        print(f"     ✗ {section}")

    print(f"\n   质量评估: {quality}")

    # 特别检查"要解决的技术问题"
    has_problem = "要解决的技术问题" in content
    if has_problem:
        print(f"\n   ✅ '要解决的技术问题'章节已包含")
    else:
        print(f"\n   ❌ '要解决的技术问题'章节缺失（这是关键问题）")

    # 保存结果
    timestamp = datetime.now().strftime('%H%M%S')
    filename = f"{test_name.replace(' ', '_')}_v2_{timestamp}.txt"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"{test_name} v2.0\n")
        f.write("=" * 70 + "\n\n")
        f.write(f"评分: {score:.1f}%\n")
        f.write(f"字符数: {chars}\n")
        f.write(f"行数: {len(lines)}\n")
        f.write(f"'要解决的技术问题'章节: {'✓' if has_problem else '✗'}\n\n")
        f.write("包含章节:\n")
        for section in found_sections:
            f.write(f"  ✓ {section}\n")
        for section in missing_sections:
            f.write(f"  ✗ {section}\n")
        f.write("\n" + "=" * 70 + "\n\n")
        f.write("完整内容:\n")
        f.write("-" * 70 + "\n")
        f.write(content)

    print(f"   💾 已保存: {filename}")

    # 显示前400字符预览
    print(f"\n   📄 内容预览:")
    print("   " + "-" * 66)
    preview = content[:400].replace('\n', '\n   ')
    print(f"   {preview}...")
    if len(content) > 400:
        print("   ...")
    print("   " + "-" * 66)

    return score


async def test_utility_model_v2_detailed():
    """测试实用新型Agent v2.0 - 详细输入"""
    print("\n" + "=" * 70)
    print("🔧 测试 1: 实用新型专利Agent v2.0（详细）")
    print("=" * 70)

    prompt = """
    请撰写一份实用新型专利申请文件：

    产品名称：一种多功能折叠椅
    技术领域：家具用品
    产品结构：椅座可折叠、靠背可调节、扶手可收纳、底部有储物抽屉
    申请人：舒适家具公司
    发明人：李工程师

    特点：
    - 椅座：双层结构，可向上折叠
    - 靠背：5档角度调节（90-135度）
    - 扶手：可向下收纳，节省空间
    - 储物：底部抽屉可放小物品
    - 材质：高强度铝合金框架
    - 尺寸：展开60x60x80-100cm，折叠60x20x80cm
    """

    result = await Runner.run(utility_model_agent, prompt)
    score = analyze_result_v2("实用新型v2.0_详细", result.final_output)
    return score


async def test_utility_model_v2_simple():
    """测试实用新型Agent v2.0 - 简化输入"""
    print("\n" + "=" * 70)
    print("🔧 测试 2: 实用新型专利Agent v2.0（简化）")
    print("=" * 70)

    prompt = """
    写一份实用新型专利：新型鞋架
    结构：多层可伸缩、可折叠
    """

    result = await Runner.run(utility_model_agent, prompt)
    score = analyze_result_v2("实用新型v2.0_简化", result.final_output)
    return score


async def test_utility_model_v2_mid():
    """测试实用新型Agent v2.0 - 中等输入"""
    print("\n" + "=" * 70)
    print("🔧 测试 3: 实用新型专利Agent v2.0（中等）")
    print("=" * 70)

    prompt = """
    请写实用新型专利：

    产品：智能晾衣架
    领域：家居用品
    结构：伸缩杆、升降机构、防风夹、LED灯
    公司：智能家居公司
    发明人：张工

    说明：
    - 杆长可伸缩（1.2-2.4米）
    - 高度可升降（离地2.2-2.8米）
    - 夹子有防风设计
    - 底部LED照明
    """

    result = await Runner.run(utility_model_agent, prompt)
    score = analyze_result_v2("实用新型v2.0_中等", result.final_output)
    return score


async def main():
    """主测试函数"""
    print("\n" + "=" * 70)
    print("🔬 实用新型专利Agent v2.0优化验证测试")
    print("=" * 70)

    # 检查 API
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ 未配置 GOOGLE_API_KEY")
        return

    print(f"✓ API 密钥: {api_key[:10]}...")
    print(f"✓ Agent v2.0: 已加载优化版本")

    # 运行测试
    scores = []

    try:
        print("\n⏳ 正在进行测试...")

        score1 = await test_utility_model_v2_detailed()
        scores.append(("详细输入", score1))

        score2 = await test_utility_model_v2_simple()
        scores.append(("简化输入", score2))

        score3 = await test_utility_model_v2_mid()
        scores.append(("中等输入", score3))

    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()

    # 生成总结
    print("\n" + "=" * 70)
    print("📊 v2.0优化验证测试总结")
    print("=" * 70)

    if scores:
        print(f"\n测试结果:")
        for name, score in scores:
            status = "✅" if score >= 90 else "⚠️" if score >= 80 else "❌"
            print(f"  {status} {name}: {score:.1f}%")

        avg_score = sum(s for _, s in scores) / len(scores)
        print(f"\n📈 平均分: {avg_score:.1f}%")

        if avg_score >= 90:
            print("🎉 优秀！v2.0优化成功！已达成90分目标！")
        elif avg_score >= 85:
            print("👍 良好！v2.0有显著提升，接近90分目标！")
        else:
            print(f"⚠️ 还需要进一步优化，距离90分还差 {90 - avg_score:.1f}分")

        # 保存总结报告
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        with open(f"v2.0优化验证报告_{timestamp}.txt", "w", encoding="utf-8") as f:
            f.write("实用新型Agent v2.0优化验证报告\n")
            f.write("=" * 70 + "\n\n")
            f.write(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("测试结果:\n")
            for name, score in scores:
                f.write(f"  {name}: {score:.1f}%\n")
            f.write(f"\n平均分: {avg_score:.1f}%\n")
            f.write("\n结论:\n")
            if avg_score >= 90:
                f.write("v2.0优化成功，已达成90分目标！\n")
            else:
                f.write(f"需要进一步优化，差距: {90 - avg_score:.1f}分\n")

    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())
