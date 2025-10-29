"""
专利撰写智能体综合测试

全面测试专利撰写功能的各种场景
"""

import asyncio
import os
from dotenv import load_dotenv
from datetime import datetime

# 加载环境变量
load_dotenv('/Users/zhangyanlong/workspaces/openai-agents-python/.env')

from main_agent import patent_agent, write_patent_application
from agents import Runner


async def test_basic_patent_writing():
    """测试基础专利撰写"""
    print("\n" + "=" * 70)
    print("📝 测试 1: 基础专利撰写")
    print("=" * 70)

    prompt = """
    请撰写一份发明专利申请文件，提供以下信息：

    发明名称：基于人工智能的智能推荐系统
    技术领域：人工智能、机器学习
    发明描述：使用深度学习技术分析用户行为，实现个性化推荐
    申请人：ABC科技公司
    """

    result = await Runner.run(patent_agent, prompt)
    return result.final_output


async def test_detailed_patent_writing():
    """测试详细专利撰写"""
    print("\n" + "=" * 70)
    print("📝 测试 2: 详细专利撰写")
    print("=" * 70)

    prompt = """
    请撰写一份完整的发明专利申请文件，包含以下详细内容：

    【基本信息】
    - 发明名称：一种基于区块链的分布式身份认证系统
    - 技术领域：区块链、身份认证、分布式系统
    - 申请人：创新科技有限公司
    - 地址：北京市朝阳区
    - 发明人：王工程师

    【技术方案】
    该系统通过区块链技术实现去中心化身份认证，包括：
    1. 智能合约管理身份信息
    2. 零知识证明保护隐私
    3. 跨域身份互认机制
    4. 分布式存储架构

    【要解决的问题】
    - 传统身份认证中心化风险高
    - 隐私保护不足
    - 跨平台身份不互通
    - 单点故障问题

    【技术效果】
    - 安全性提升90%
    - 隐私保护加强
    - 跨域互认效率提升80%

    请按标准格式生成完整申请文件。
    """

    result = await Runner.run(patent_agent, prompt)
    return result.final_output


async def test_tool_directly():
    """直接测试工具函数"""
    print("\n" + "=" * 70)
    print("🔧 测试 3: 直接调用工具函数")
    print("=" * 70)

    result = write_patent_application(
        invention_description="基于深度学习的图像识别系统，通过卷积神经网络实现高精度图像分类",
        technical_field="计算机视觉、深度学习、图像处理",
        patent_type="invention",
        applicant_name="AI创新公司",
        applicant_address="上海市浦东新区",
        inventor_name="张博士"
    )
    return result


async def test_with_background():
    """测试带背景信息的撰写"""
    print("\n" + "=" * 70)
    print("📚 测试 4: 带背景信息的专利撰写")
    print("=" * 70)

    prompt = """
    请撰写专利申请文件：

    发明名称：智能制造中的质量检测系统
    技术领域：智能制造、计算机视觉

    背景技术：
    传统制造行业依赖人工质检，效率低、成本高、易出错。
    现有自动检测系统准确率不足，无法应对复杂场景。

    要解决的问题：
    1. 提高检测准确率
    2. 降低人工成本
    3. 实时检测反馈
    4. 适应多种产品

    解决方案：
    采用深度学习算法，结合机器视觉技术，实现自动化质检。
    包括图像采集、预处理、特征提取、缺陷识别、结果输出等模块。

    有益效果：
    - 检测准确率提升至99.5%
    - 效率提升10倍
    - 成本降低60%
    """

    result = await Runner.run(patent_agent, prompt)
    return result.final_output


async def analyze_result(test_name, content):
    """分析测试结果"""
    print(f"\n📊 {test_name} 分析:")
    print("-" * 70)

    # 基本统计
    lines = content.split('\n')
    chars = len(content)
    words = len(content.split())

    print(f"   总行数: {len(lines)}")
    print(f"   总字符数: {chars}")
    print(f"   总词数: {words}")

    # 检查关键章节
    sections = {
        "发明名称": "发明名称" in content or "名称" in content,
        "技术领域": "技术领域" in content,
        "背景技术": "背景技术" in content,
        "发明内容": "发明内容" in content or "发明内容" in content,
        "附图说明": "附图说明" in content,
        "权利要求": "权利要求" in content,
    }

    print(f"\n   包含章节:")
    for section, exists in sections.items():
        status = "✓" if exists else "✗"
        print(f"     {status} {section}")

    # 评分
    score = sum(sections.values()) / len(sections) * 100
    print(f"\n   完整度评分: {score:.1f}%")

    return {
        "lines": len(lines),
        "chars": chars,
        "words": words,
        "sections": sections,
        "score": score
    }


async def main():
    """主测试函数"""
    print("\n" + "=" * 70)
    print("🔬 专利撰写智能体综合测试")
    print("=" * 70)

    # 检查 API
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ 未配置 API 密钥")
        return

    print(f"✓ API 密钥: {api_key[:10]}...")

    # 收集所有结果
    results = {}

    # 运行测试
    tests = [
        ("基础撰写", test_basic_patent_writing),
        ("详细撰写", test_detailed_patent_writing),
        ("工具函数", test_tool_directly),
        ("背景信息", test_with_background),
    ]

    for test_name, test_func in tests:
        try:
            print(f"\n⏳ 正在运行: {test_name}...")
            content = await test_func()
            results[test_name] = content
            await analyze_result(test_name, content)
        except Exception as e:
            print(f"❌ {test_name} 失败: {e}")
            results[test_name] = f"ERROR: {e}"

    # 生成综合报告
    print("\n" + "=" * 70)
    print("📈 综合测试报告")
    print("=" * 70)

    # 保存详细结果
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    report_file = f"patent_writing_test_report_{timestamp}.txt"

    with open(report_file, "w", encoding="utf-8") as f:
        f.write("专利撰写智能体测试报告\n")
        f.write("=" * 70 + "\n\n")
        f.write(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"API 密钥: {api_key[:10]}...\n")
        f.write(f"模型: Google Gemini 2.0 Flash\n\n")

        for test_name, content in results.items():
            f.write("\n" + "=" * 70 + "\n")
            f.write(f"测试: {test_name}\n")
            f.write("=" * 70 + "\n\n")
            f.write(str(content))
            f.write("\n\n")

    print(f"\n✅ 详细报告已保存到: {report_file}")

    # 总体评估
    print("\n" + "=" * 70)
    print("🎯 总体评估")
    print("=" * 70)

    success_count = sum(1 for r in results.values() if not str(r).startswith("ERROR"))
    total_count = len(results)

    print(f"测试通过: {success_count}/{total_count}")
    print(f"成功率: {success_count/total_count*100:.1f}%")

    if success_count == total_count:
        print("\n🎉 所有测试通过！专利撰写智能体运行正常。")
    else:
        print(f"\n⚠️ {total_count - success_count} 个测试失败")

    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())
