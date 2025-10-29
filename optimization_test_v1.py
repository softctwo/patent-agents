"""
第一轮优化测试 - 验证指令优化效果

测试优化后的Agent是否能直接生成内容
"""

import asyncio
import os
from dotenv import load_dotenv
from datetime import datetime

# 加载环境变量
load_dotenv('/Users/zhangyanlong/workspaces/openai-agents-python/.env')

from main_agent import patent_agent
from agents import Runner


async def test_optimized_v1():
    """测试优化版本 v1"""
    print("\n" + "=" * 70)
    print("🚀 第一轮优化测试 - 验证指令优化效果")
    print("=" * 70)

    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ 未配置 API")
        return

    print(f"✓ API: {api_key[:10]}...")

    # 测试用例 1：标准专利撰写
    prompt1 = """
    请撰写一份关于智能推荐系统的发明专利申请文件。

    发明信息：
    - 名称：基于深度学习的智能推荐系统
    - 技术领域：人工智能、机器学习
    - 申请人：ABC科技公司
    - 发明人：张工程师
    """

    print("\n📝 测试 1: 标准专利撰写")
    print("-" * 70)
    result1 = await Runner.run(patent_agent, prompt1)
    analyze_result("测试 1", result1.final_output, save_prefix="v1_test1")

    # 测试用例 2：简化请求
    prompt2 = """
    写一份专利：智能推荐系统
    """

    print("\n📝 测试 2: 简化请求")
    print("-" * 70)
    result2 = await Runner.run(patent_agent, prompt2)
    analyze_result("测试 2", result2.final_output, save_prefix="v1_test2")

    # 测试用例 3：详细请求
    prompt3 = """
    专利信息：
    - 名称：区块链身份认证系统
    - 技术领域：区块链、身份认证
    - 背景：传统身份认证中心化风险高
    - 问题：安全性不足、隐私泄露
    - 方案：使用零知识证明和智能合约
    - 效果：安全性提升90%
    - 申请人：创新科技有限公司
    - 发明人：李博士

    请生成完整专利文件。
    """

    print("\n📝 测试 3: 详细请求")
    print("-" * 70)
    result3 = await Runner.run(patent_agent, prompt3)
    analyze_result("测试 3", result3.final_output, save_prefix="v1_test3")

    # 总结
    print("\n" + "=" * 70)
    print("📊 第一轮优化测试总结")
    print("=" * 70)


def analyze_result(test_name, content, save_prefix=""):
    """分析测试结果"""
    lines = content.split('\n')
    chars = len(content)

    # 检查关键章节
    sections = {
        "发明名称": any("发明名称" in line or "名称" in line or "智能推荐系统" in line or "区块链" in line for line in lines),
        "技术领域": "技术领域" in content,
        "背景技术": "背景技术" in content,
        "要解决的问题": "要解决" in content or "技术问题" in content,
        "解决方案": "解决方案" in content or "技术方案" in content,
        "有益效果": "有益效果" in content,
        "附图说明": "附图说明" in content,
        "权利要求": "权利要求" in content,
    }

    # 计算分数
    score = sum(sections.values()) / len(sections) * 100

    print(f"   字符数: {chars}")
    print(f"   行数: {len(lines)}")

    # 显示包含的章节
    print(f"\n   包含章节 ({score:.1f}%):")
    for section, has in sections.items():
        status = "✓" if has else "✗"
        print(f"     {status} {section}")

    # 质量评估
    if score >= 80:
        quality = "🎉 优秀"
    elif score >= 60:
        quality = "👍 良好"
    elif score >= 40:
        quality = "⚠️ 一般"
    else:
        quality = "❌ 较差"

    print(f"\n   质量评估: {quality}")

    # 保存结果
    timestamp = datetime.now().strftime('%H%M%S')
    filename = f"{save_prefix}_{timestamp}.txt"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"{test_name}\n")
        f.write("=" * 70 + "\n\n")
        f.write(f"评分: {score:.1f}%\n")
        f.write(f"字符数: {chars}\n")
        f.write(f"行数: {len(lines)}\n\n")
        f.write("包含章节:\n")
        for section, has in sections.items():
            f.write(f"  {'✓' if has else '✗'} {section}\n")
        f.write("\n" + "=" * 70 + "\n\n")
        f.write("完整内容:\n")
        f.write("-" * 70 + "\n")
        f.write(content)

    print(f"   💾 已保存: {filename}")

    # 显示前300字符预览
    print(f"\n   📄 内容预览:")
    print("   " + "-" * 66)
    preview = content[:300].replace('\n', '\n   ')
    print(f"   {preview}...")
    if len(content) > 300:
        print("   ...")
    print("   " + "-" * 66)

    return score


async def main():
    """主函数"""
    await test_optimized_v1()

    print("\n" + "=" * 70)
    print("✨ 第一轮优化测试完成！")
    print("检查保存的测试文件以查看详细结果")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())
