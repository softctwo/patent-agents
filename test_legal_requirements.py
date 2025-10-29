#!/usr/bin/env python3
"""
测试实用新型专利Agent的法规要求合规性
验证新增的撰写规则是否生效
"""

import asyncio
import os
import sys
from datetime import datetime

# 添加路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agents import Runner
from utility_model_agent import utility_model_agent

# 设置API密钥
os.environ["GOOGLE_API_KEY"] = "test_key"

# 测试评分标准
SCORING_CRITERIA = {
    "法规合规性": {
        "weight": 30,
        "description": "严格遵守专利法等法规要求",
        "checks": [
            "不生成软件/方法专利",
            "产品形态符合要求",
            "避免编造内容",
            "具有创新性"
        ]
    },
    "内容完整性": {
        "weight": 25,
        "description": "包含全部8个必需章节",
        "checks": [
            "发明名称",
            "技术领域",
            "背景技术",
            "实用新型内容（要解决的技术问题、技术方案、有益效果）",
            "附图说明",
            "具体实施方式",
            "权利要求书",
            "实用新型说明"
        ]
    },
    "结构描述质量": {
        "weight": 25,
        "description": "产品形状和构造描述详细准确",
        "checks": [
            "产品结构清晰",
            "构造关系明确",
            "部件连接方式描述",
            "技术效果合理"
        ]
    },
    "实用新型特征": {
        "weight": 20,
        "description": "体现实用新型专利特点",
        "checks": [
            "聚焦产品结构",
            "保护期限10年说明",
            "权利要求聚焦结构特征",
            "附图描述完整"
        ]
    }
}

def evaluate_response(response_text: str, test_case_name: str) -> dict:
    """评估响应质量"""
    print(f"\n{'='*70}")
    print(f"📊 评估测试：{test_case_name}")
    print(f"{'='*70}")

    scores = {}
    total_score = 0
    max_score = 100

    # 1. 法规合规性评估 (30分)
    legal_score = 0
    legal_checks = SCORING_CRITERIA["法规合规性"]["checks"]

    if "软件" not in response_text.lower() or "方法" not in response_text.lower():
        if "不生成软件" in response_text or "拒绝" in response_text:
            legal_score += 15
            print("✅ 正确拒绝软件/方法专利申请")
        else:
            legal_score += 30
            print("✅ 产品形态符合法规要求（实体产品）")
    else:
        print("❌ 可能包含不适当内容")

    # 创新性检查
    if "创新" in response_text or "改进" in response_text or "进步" in response_text:
        legal_score += 10
        print("✅ 体现了创新性要求")
    else:
        print("⚠️ 创新性描述不够明确")

    # 禁止编造检查
    if "编造" not in response_text and "虚假" not in response_text:
        print("✅ 未发现编造内容")
    else:
        print("⚠️ 可能存在编造风险")

    scores["法规合规性"] = min(legal_score, 30)

    # 2. 内容完整性评估 (25分)
    content_score = 0
    content_checks = SCORING_CRITERIA["内容完整性"]["checks"]

    required_sections = [
        "发明名称", "技术领域", "背景技术",
        "实用新型内容", "要解决的技术问题",
        "技术方案", "有益效果", "附图说明",
        "具体实施方式", "权利要求书"
    ]

    found_sections = sum(1 for section in required_sections if section in response_text)
    content_score = min(found_sections * 2.5, 25)

    print(f"✅ 找到 {found_sections}/{len(required_sections)} 个必需章节 ({content_score:.1f}/25分)")

    scores["内容完整性"] = content_score

    # 3. 结构描述质量评估 (25分)
    structure_score = 15

    if "结构" in response_text or "构造" in response_text:
        structure_score += 5
        print("✅ 包含结构描述")

    if "连接" in response_text or "组成" in response_text:
        structure_score += 3
        print("✅ 包含构造关系")

    if "部件" in response_text or "组件" in response_text:
        structure_score += 2
        print("✅ 包含部件描述")

    scores["结构描述质量"] = min(structure_score, 25)

    # 4. 实用新型特征评估 (20分)
    um_score = 0

    if "10年" in response_text:
        um_score += 5
        print("✅ 包含保护期限说明")

    if "形状" in response_text or "构造" in response_text:
        um_score += 8
        print("✅ 聚焦产品形状和构造")

    if "权利要求" in response_text:
        um_score += 4
        print("✅ 包含权利要求")

    if "附图" in response_text:
        um_score += 3
        print("✅ 包含附图说明")

    scores["实用新型特征"] = min(um_score, 20)

    # 总分
    total_score = sum(scores.values())

    print(f"\n{'='*70}")
    print(f"📈 评分结果")
    print(f"{'='*70}")
    for category, score in scores.items():
        weight = SCORING_CRITERIA[category]["weight"]
        print(f"{category:15s} {score:5.1f}/{weight}分")
    print(f"{'-'*70}")
    print(f"{'总分':15s} {total_score:5.1f}/100分")
    print(f"{'='*70}")

    return {
        "test_case": test_case_name,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "scores": scores,
        "total_score": total_score,
        "response_length": len(response_text),
        "status": "通过" if total_score >= 90 else "需改进"
    }

async def run_legal_compliance_tests():
    """运行法规合规性测试"""
    print("\n" + "="*70)
    print("🧪 实用新型专利Agent - 法规合规性测试")
    print("="*70)

    test_results = []

    # 测试1：拒绝软件专利申请
    print("\n" + "="*70)
    print("测试1：拒绝软件专利申请")
    print("="*70)

    result = await Runner.run(
        utility_model_agent,
        "请撰写一份软件专利：基于AI的智能推荐算法"
    )

    test1_result = evaluate_response(result.final_output, "拒绝软件专利")
    test_results.append(test1_result)

    # 测试2：拒绝方法专利申请
    print("\n" + "="*70)
    print("测试2：拒绝方法专利申请")
    print("="*70)

    result = await Runner.run(
        utility_model_agent,
        "请撰写一份方法专利：一种提高工作效率的方法"
    )

    test2_result = evaluate_response(result.final_output, "拒绝方法专利")
    test_results.append(test2_result)

    # 测试3：生成实体产品专利（符合要求）
    print("\n" + "="*70)
    print("测试3：生成实体产品专利")
    print("="*70)

    result = await Runner.run(
        utility_model_agent,
        """
        请撰写一份实用新型专利：

        产品名称：一种便于携带的折叠式收纳盒
        技术领域：日常生活用品、收纳容器
        产品结构：盒体、折叠铰链、卡扣固定装置、侧壁加强筋
        特点：
        - 折叠设计便于携带和存储
        - 卡扣固定保证展开后稳固性
        - 侧壁加强筋提高承重能力
        """
    )

    test3_result = evaluate_response(result.final_output, "实体产品专利")
    test_results.append(test3_result)

    # 测试4：创新性产品专利
    print("\n" + "="*70)
    print("测试4：创新性产品专利")
    print("="*70)

    result = await Runner.run(
        utility_model_agent,
        """
        请撰写一份实用新型专利：

        产品名称：一种防滑折叠梯子
        技术领域：梯子设备、建筑辅助工具
        产品结构：梯体、踏板、防滑垫片、折叠机构、安全锁扣、伸缩支撑杆
        创新点：
        - 踏板表面增加防滑纹理设计
        - 折叠机构采用双向锁定机制
        - 底部增加可调节支撑脚
        - 整体采用轻量化材料但保持强度
        """
    )

    test4_result = evaluate_response(result.final_output, "创新性产品专利")
    test_results.append(test4_result)

    # 生成综合报告
    print("\n" + "="*70)
    print("📋 综合测试报告")
    print("="*70)

    avg_score = sum(r["total_score"] for r in test_results) / len(test_results)

    print(f"\n测试时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"测试用例数：{len(test_results)}")
    print(f"平均得分：{avg_score:.1f}/100分")

    passed = sum(1 for r in test_results if r["status"] == "通过")
    print(f"通过率：{passed}/{len(test_results)} ({(passed/len(test_results)*100):.1f}%)")

    print(f"\n{'='*70}")
    print("详细结果：")
    print(f"{'='*70}")

    for i, result in enumerate(test_results, 1):
        print(f"\n{i}. {result['test_case']}")
        print(f"   状态：{result['status']}")
        print(f"   得分：{result['total_score']:.1f}/100分")
        print(f"   字符数：{result['response_length']}")

    # 保存测试报告
    report_file = f"法规合规性测试报告_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("="*70 + "\n")
        f.write("实用新型专利Agent - 法规合规性测试报告\n")
        f.write("="*70 + "\n\n")
        f.write(f"测试时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"测试用例数：{len(test_results)}\n")
        f.write(f"平均得分：{avg_score:.1f}/100分\n")
        f.write(f"通过率：{passed}/{len(test_results)} ({(passed/len(test_results)*100):.1f}%)\n\n")

        f.write("="*70 + "\n")
        f.write("详细评分：\n")
        f.write("="*70 + "\n")

        for i, result in enumerate(test_results, 1):
            f.write(f"\n{i}. {result['test_case']}\n")
            f.write(f"   状态：{result['status']}\n")
            f.write(f"   得分：{result['total_score']:.1f}/100分\n")
            f.write(f"   字符数：{result['response_length']}\n")

            for category, score in result["scores"].items():
                weight = SCORING_CRITERIA[category]["weight"]
                f.write(f"   {category}: {score:.1f}/{weight}分\n")

        f.write("\n" + "="*70 + "\n")
        f.write("法规要求检查项：\n")
        f.write("="*70 + "\n")
        for category, details in SCORING_CRITERIA.items():
            f.write(f"\n【{category}】权重：{details['weight']}分\n")
            f.write(f"{details['description']}\n")
            for check in details["checks"]:
                f.write(f"  - {check}\n")

    print(f"\n✅ 测试报告已保存到：{report_file}")

    return test_results

if __name__ == "__main__":
    asyncio.run(run_legal_compliance_tests())
