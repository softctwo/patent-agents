"""
测试新开发的专利撰写Agent

包括：实用新型专利Agent和外观设计专利Agent
进行多轮测试和优化，达到90分以上
"""

import asyncio
import os
from dotenv import load_dotenv
from datetime import datetime

# 加载环境变量
load_dotenv('/Users/zhangyanlong/workspaces/openai-agents-python/.env')

from utility_model_agent import utility_model_agent
from design_patent_agent import design_patent_agent
from agents import Runner


def analyze_result(test_name, content, expected_sections):
    """分析测试结果"""
    lines = content.split('\n')
    chars = len(content)

    # 检查关键章节
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

    # 保存结果
    timestamp = datetime.now().strftime('%H%M%S')
    filename = f"{test_name.replace(' ', '_')}_{timestamp}.txt"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"{test_name}\n")
        f.write("=" * 70 + "\n\n")
        f.write(f"评分: {score:.1f}%\n")
        f.write(f"字符数: {chars}\n")
        f.write(f"行数: {len(lines)}\n\n")
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


async def test_utility_model_v1():
    """测试实用新型Agent v1.0"""
    print("\n" + "=" * 70)
    print("🔧 测试 1: 实用新型专利Agent v1.0")
    print("=" * 70)

    prompt = """
    请撰写一份实用新型专利申请文件：

    产品名称：一种智能折叠桌
    技术领域：家具用品、办公用品
    产品结构：桌面采用可折叠设计，桌腿可伸缩调节，底部有万向轮
    申请人：创新家具有限公司
    发明人：张工程师

    特点：
    - 桌面：双层结构，可折叠收纳
    - 桌腿：不锈钢材质，高度可调（60-80cm）
    - 底盘：五星型底座，稳定性强
    - 万向轮：360度旋转，带刹车功能
    - 便捷性：折叠后体积小，便于存储
    """

    result = await Runner.run(utility_model_agent, prompt)
    expected_sections = [
        "发明名称",
        "技术领域",
        "背景技术",
        "要解决的问题",
        "技术方案",
        "有益效果",
        "附图说明",
        "权利要求",
    ]
    score = analyze_result("实用新型测试1", result.final_output, expected_sections)
    return score


async def test_utility_model_v2():
    """测试实用新型Agent v1.0 - 简化输入"""
    print("\n" + "=" * 70)
    print("🔧 测试 2: 实用新型专利Agent v1.0（简化）")
    print("=" * 70)

    prompt = """
    写一份实用新型专利：智能水杯
    结构：双层真空、温度显示、密封杯盖
    """

    result = await Runner.run(utility_model_agent, prompt)
    expected_sections = [
        "发明名称",
        "技术领域",
        "背景技术",
        "要解决的问题",
        "技术方案",
        "有益效果",
        "附图说明",
        "权利要求",
    ]
    score = analyze_result("实用新型测试2", result.final_output, expected_sections)
    return score


async def test_design_patent_v1():
    """测试外观设计Agent v1.0"""
    print("\n" + "=" * 70)
    print("🎨 测试 3: 外观设计专利Agent v1.0")
    print("=" * 70)

    prompt = """
    请撰写一份外观设计专利申请文件：

    产品名称：现代简约台灯
    设计描述：采用几何造型设计，灯罩为圆锥形，底座为圆形扁平设计
    设计特征：
    - 整体风格：现代简约、北欧风格
    - 灯罩：白色亚克力材质，圆锥形，顶部开口
    - 灯杆：黑色金属材质，伸缩式，可调节高度
    - 底座：黑色金属圆形底座，直径20cm，厚度2cm
    - 开关：触摸式开关，隐藏在底座边缘
    - 色彩：黑白经典配色
    - 尺寸：灯罩直径15cm，高度25-35cm可调
    申请人：现代家居设计公司
    设计人：王设计师
    """

    result = await Runner.run(design_patent_agent, prompt)
    expected_sections = [
        "产品名称",
        "技术领域",
        "背景技术",
        "设计内容",
        "设计效果",
        "图片说明",
        "简要说明",
    ]
    score = analyze_result("外观设计测试1", result.final_output, expected_sections)
    return score


async def test_design_patent_v2():
    """测试外观设计Agent v1.0 - 简化输入"""
    print("\n" + "=" * 70)
    print("🎨 测试 4: 外观设计专利Agent v1.0（简化）")
    print("=" * 70)

    prompt = """
    写一份外观设计专利：智能音箱
    设计：圆柱形外观，顶部有LED灯环
    """

    result = await Runner.run(design_patent_agent, prompt)
    expected_sections = [
        "产品名称",
        "技术领域",
        "背景技术",
        "设计内容",
        "设计效果",
        "图片说明",
        "简要说明",
    ]
    score = analyze_result("外观设计测试2", result.final_output, expected_sections)
    return score


async def test_guidance():
    """测试指导功能"""
    print("\n" + "=" * 70)
    print("📚 测试 5: 获取撰写指导")
    print("=" * 70)

    # 测试实用新型指导
    print("\n🔧 实用新型指导:")
    result1 = await Runner.run(
        utility_model_agent,
        "请提供实用新型专利撰写指导"
    )
    print(result1.final_output[:300] + "...")

    # 测试外观设计指导
    print("\n🎨 外观设计指导:")
    result2 = await Runner.run(
        design_patent_agent,
        "请提供外观设计专利撰写指导"
    )
    print(result2.final_output[:300] + "...")


async def main():
    """主测试函数"""
    print("\n" + "=" * 70)
    print("🔬 新专利撰写Agent综合测试")
    print("=" * 70)

    # 检查 API
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ 未配置 GOOGLE_API_KEY")
        return

    print(f"✓ API 密钥: {api_key[:10]}...")
    print(f"✓ 实用新型 Agent: 已加载")
    print(f"✓ 外观设计 Agent: 已加载")

    # 运行测试
    scores = []

    try:
        print("\n⏳ 正在进行测试...")
        score1 = await test_utility_model_v1()
        scores.append(("实用新型测试1", score1))

        score2 = await test_utility_model_v2()
        scores.append(("实用新型测试2", score2))

        score3 = await test_design_patent_v1()
        scores.append(("外观设计测试1", score3))

        score4 = await test_design_patent_v2()
        scores.append(("外观设计测试2", score4))

        # 测试指导功能
        await test_guidance()

    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()

    # 生成总结
    print("\n" + "=" * 70)
    print("📊 第一轮测试总结")
    print("=" * 70)

    if scores:
        print(f"\n测试结果:")
        for name, score in scores:
            status = "✅" if score >= 60 else "❌"
            print(f"  {status} {name}: {score:.1f}%")

        avg_score = sum(s for _, s in scores) / len(scores)
        print(f"\n📈 平均分: {avg_score:.1f}%")

        if avg_score >= 90:
            print("🎉 优秀！已达到90分目标！")
        elif avg_score >= 80:
            print("👍 良好！接近90分目标！")
        else:
            print(f"⚠️ 需要改进！距离90分还差 {90 - avg_score:.1f}分")

        # 保存总结报告
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        with open(f"第一轮测试报告_{timestamp}.txt", "w", encoding="utf-8") as f:
            f.write("新专利撰写Agent第一轮测试报告\n")
            f.write("=" * 70 + "\n\n")
            f.write(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("测试结果:\n")
            for name, score in scores:
                f.write(f"  {name}: {score:.1f}%\n")
            f.write(f"\n平均分: {avg_score:.1f}%\n")
            f.write("\n结论和建议:\n")
            if avg_score >= 90:
                f.write("已达成目标，无需进一步优化\n")
            else:
                f.write(f"需要进一步优化，差距: {90 - avg_score:.1f}分\n")
                f.write("建议:\n")
                f.write("1. 优化Agent指令\n")
                f.write("2. 改进提示词工程\n")
                f.write("3. 增加示例引导\n")
                f.write("4. 强化格式要求\n")

    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())
