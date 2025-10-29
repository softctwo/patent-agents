#!/usr/bin/env python3
"""
静态检查：验证实用新型专利Agent的法规要求
不依赖API密钥，直接检查指令文本
"""

import re

def check_agent_instructions():
    """检查Agent指令中是否包含所有必要的法规要求"""
    print("\n" + "="*70)
    print("🔍 实用新型专利Agent - 法规要求静态检查")
    print("="*70)

    # 读取Agent文件
    try:
        with open('utility_model_agent.py', 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print("❌ 未找到 utility_model_agent.py 文件")
        return False

    # 检查项目
    checks = {
        "法律法规要求部分": {
            "pattern": r"【法律法规要求】",
            "required": True,
            "description": "是否存在专门的法律法规要求章节"
        },
        "专利法遵守": {
            "pattern": r"专利法.*实施细则.*专利审查指南",
            "required": True,
            "description": "是否提及遵守专利法及其实施细则、审查指南"
        },
        "禁止编造要求": {
            "pattern": r"🚫.*禁止编造|不得编造",
            "required": True,
            "description": "是否有明确的禁止编造要求"
        },
        "创新性要求": {
            "pattern": r"🔬.*创新性要求|与现有技术相比.*创新.*进步",
            "required": True,
            "description": "是否包含创新性和进步性要求"
        },
        "产品形态要求": {
            "pattern": r"📦.*产品形态要求|不能是软件.*不能是方法",
            "required": True,
            "description": "是否明确禁止软件、方法专利"
        },
        "装置物件产品": {
            "pattern": r"具体的装置.*物件.*产品",
            "required": True,
            "description": "是否要求产品是具体的装置物件"
        },
        "微观结构禁止": {
            "pattern": r"不能是微观结构|分子.*原子",
            "required": True,
            "description": "是否禁止微观结构"
        },
        "不定型产品禁止": {
            "pattern": r"不能是不定型产品|气体.*液体.*粉状",
            "required": True,
            "description": "是否禁止不定型产品"
        },
        "不稳定结构禁止": {
            "pattern": r"不能是不稳定结构|临时性.*偶然性",
            "required": True,
            "description": "是否禁止不稳定结构"
        },
        "实体产品要求": {
            "pattern": r"实体.*可见.*可触摸",
            "required": True,
            "description": "是否要求产品是实体、可见、可触摸的"
        },
        "结构稳定性": {
            "pattern": r"🏗️.*结构明确性|稳定.*持久.*可实现",
            "required": True,
            "description": "是否强调结构的稳定性和持久性"
        }
    }

    print("\n检查结果：")
    print("="*70)

    passed = 0
    failed = 0

    for check_name, check_info in checks.items():
        pattern = check_info["pattern"]
        required = check_info["required"]
        description = check_info["description"]

        # 搜索匹配
        matches = re.findall(pattern, content, re.IGNORECASE | re.DOTALL)

        if matches:
            print(f"✅ {check_name}")
            print(f"   {description}")
            print(f"   匹配内容：{matches[0][:50]}...")
            passed += 1
        else:
            print(f"❌ {check_name} - 未找到")
            print(f"   {description}")
            failed += 1

        print()

    print("="*70)
    print(f"检查统计：")
    print(f"  通过：{passed}/{len(checks)}")
    print(f"  失败：{failed}/{len(checks)}")
    print(f"  通过率：{(passed/len(checks)*100):.1f}%")
    print("="*70)

    # 生成详细报告
    report_file = f"法规要求静态检查报告.txt"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("="*70 + "\n")
        f.write("实用新型专利Agent - 法规要求静态检查报告\n")
        f.write("="*70 + "\n\n")

        f.write("检查时间：2025-10-30 02:00:00\n")
        f.write(f"检查项目数：{len(checks)}\n")
        f.write(f"通过数：{passed}\n")
        f.write(f"失败数：{failed}\n")
        f.write(f"通过率：{(passed/len(checks)*100):.1f}%\n\n")

        f.write("="*70 + "\n")
        f.write("详细检查结果：\n")
        f.write("="*70 + "\n\n")

        for i, (check_name, check_info) in enumerate(checks.items(), 1):
            pattern = check_info["pattern"]
            description = check_info["description"]

            matches = re.findall(pattern, content, re.IGNORECASE | re.DOTALL)

            f.write(f"{i}. {check_name}\n")
            f.write(f"   描述：{description}\n")
            f.write(f"   匹配模式：{pattern}\n")

            if matches:
                f.write(f"   状态：✅ 通过\n")
                f.write(f"   匹配内容：{matches[0][:100]}...\n\n")
            else:
                f.write(f"   状态：❌ 失败\n")
                f.write(f"   建议：需要在Agent指令中添加此要求\n\n")

        f.write("="*70 + "\n")
        f.write("新增法规要求汇总：\n")
        f.write("="*70 + "\n\n")

        f.write("1. 遵守法律法规\n")
        f.write("   - 专利法\n")
        f.write("   - 专利法实施细则\n")
        f.write("   - 专利审查指南\n\n")

        f.write("2. 禁止编造\n")
        f.write("   - 不编造产品名称、结构、技术效果\n")
        f.write("   - 不编造现有技术问题\n")
        f.write("   - 不编造技术方案和有益效果\n\n")

        f.write("3. 创新性要求\n")
        f.write("   - 与现有技术相比有实际创新和进步\n")
        f.write("   - 结构改进具有实质性特点\n")
        f.write("   - 技术方案不能是显而易见的简单组合\n\n")

        f.write("4. 产品形态要求\n")
        f.write("   - 必须是具体的装置、物件、产品\n")
        f.write("   - 不能是软件、程序、算法\n")
        f.write("   - 不能是方法、工艺、步骤\n")
        f.write("   - 不能是微观结构（分子、原子级别）\n")
        f.write("   - 不能是不定型产品（气体、液体、粉状等）\n")
        f.write("   - 不能是不稳定结构（临时性、偶然性结构）\n\n")

        f.write("5. 结构明确性\n")
        f.write("   - 产品的形状要明确、具体、可描述\n")
        f.write("   - 构造关系要清晰、稳定、持久\n")
        f.write("   - 各部件连接方式要牢固可靠\n")
        f.write("   - 整体结构要完整、可实现\n")

    print(f"\n✅ 详细报告已保存到：{report_file}")

    return passed == len(checks)

def verify_instructions_structure():
    """验证指令结构的完整性"""
    print("\n" + "="*70)
    print("📋 指令结构完整性检查")
    print("="*70)

    try:
        with open('utility_model_agent.py', 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        return False

    # 提取instructions部分
    instructions_match = re.search(r'instructions="""(.*?)"""', content, re.DOTALL)
    if not instructions_match:
        print("❌ 未找到instructions部分")
        return False

    instructions = instructions_match.group(1)

    # 检查章节结构
    sections = [
        "【核心规则】",
        "【法律法规要求】",
        "【实用新型标准格式】",
        "【重点强调】",
        "【撰写要求】",
        "【禁止行为】",
        "【必须行为】"
    ]

    print("\n章节检查：")
    print("-"*70)

    found_sections = []
    missing_sections = []

    for section in sections:
        if section in instructions:
            print(f"✅ {section}")
            found_sections.append(section)
        else:
            print(f"❌ 缺失：{section}")
            missing_sections.append(section)

    print("-"*70)
    print(f"发现章节：{len(found_sections)}/{len(sections)}")
    print(f"缺失章节：{len(missing_sections)}")

    if missing_sections:
        print("\n⚠️ 建议添加以下章节：")
        for section in missing_sections:
            print(f"  - {section}")

    return len(missing_sections) == 0

def check_prohibited_content():
    """检查禁止内容部分"""
    print("\n" + "="*70)
    print("🚫 禁止内容检查")
    print("="*70)

    try:
        with open('utility_model_agent.py', 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        return False

    prohibitions = [
        ("❌ 不要生成软件、方法相关的专利", "软件|方法专利"),
        ("❌ 不要生成微观结构或不稳定结构", "微观结构|不稳定结构"),
        ("❌ 不要编造技术内容", "编造")
    ]

    found_prohibitions = 0

    print("\n禁止条款：")
    print("-"*70)

    for description, pattern in prohibitions:
        if re.search(pattern, content, re.IGNORECASE):
            print(f"✅ {description}")
            found_prohibitions += 1
        else:
            print(f"❌ 缺失：{description}")

    print("-"*70)
    print(f"发现禁止条款：{found_prohibitions}/{len(prohibitions)}")

    return found_prohibitions == len(prohibitions)

if __name__ == "__main__":
    print("\n" + "="*70)
    print("🧪 实用新型专利Agent - 法规要求验证工具")
    print("="*70)

    # 运行所有检查
    check1 = check_agent_instructions()
    check2 = verify_instructions_structure()
    check3 = check_prohibited_content()

    # 综合评估
    print("\n" + "="*70)
    print("📊 综合评估结果")
    print("="*70)

    total_checks = 3
    passed_checks = sum([check1, check2, check3])

    print(f"法规要求检查：{'✅ 通过' if check1 else '❌ 失败'}")
    print(f"指令结构检查：{'✅ 通过' if check2 else '❌ 失败'}")
    print(f"禁止内容检查：{'✅ 通过' if check3 else '❌ 失败'}")
    print("-"*70)
    print(f"总体状态：{'✅ 验证通过' if passed_checks == total_checks else '❌ 需要改进'}")
    print(f"完成度：{passed_checks}/{total_checks} ({(passed_checks/total_checks*100):.1f}%)")

    if passed_checks == total_checks:
        print("\n🎉 所有法规要求已成功添加到Agent指令中！")
    else:
        print("\n⚠️ 部分检查未通过，建议补充相关内容")

    print("="*70 + "\n")
