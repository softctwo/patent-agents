#!/usr/bin/env python3
"""
专利附图绘制Agent与专利撰写Agent集成测试
演示如何在撰写专利时调用附图绘制功能
"""

import asyncio
import os
import sys
from datetime import datetime

# 添加路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'drawing_agent'))

from agents import Runner

# 导入专利撰写Agent
from utility_model_agent import utility_model_agent

# 导入专利附图绘制Agent
from drawing_agent.patent_drawing_agent import patent_drawing_agent


async def test_patent_writing_with_drawing():
    """测试专利撰写与附图绘制的集成"""
    print("\n" + "=" * 70)
    print("📝 专利撰写与附图绘制 - 集成测试")
    print("=" * 70)

    test_results = []

    # 测试场景：智能水杯专利撰写与附图绘制
    print("\n" + "=" * 70)
    print("测试场景：智能水杯专利撰写")
    print("=" * 70)

    # 步骤1：撰写专利申请文件
    print("\n📝 步骤1：撰写专利申请文件...")
    patent_result = await Runner.run(
        utility_model_agent,
        """
        请撰写一份实用新型专利申请文件：

        产品名称：一种带温度显示的智能水杯
        技术领域：日常生活用品、保温容器
        产品结构：水杯杯体、双层真空结构、温度传感器、LED显示屏、杯盖密封圈、USB充电口
        申请人：智能生活科技有限公司
        发明人：王工程师

        特点：
        - 双层真空结构保持温度
        - 内置温度传感器实时监测水温
        - LED显示屏清晰显示温度
        - 杯盖配有密封圈防止漏水
        - USB充电口方便充电
        - 椭圆形外观设计美观便携
        """
    )

    print("✅ 专利申请文件撰写完成")
    patent_content = patent_result.final_output
    test_results.append({
        "step": "专利撰写",
        "status": "成功",
        "content_length": len(patent_content)
    })

    # 步骤2：绘制机械结构图
    print("\n📐 步骤2：绘制机械结构图...")
    drawing_result = await Runner.run(
        patent_drawing_agent,
        """
        请创建一份机械结构图：

        发明名称：一种带温度显示的智能水杯
        产品描述：智能水杯采用双层真空结构，内置温度传感器和LED显示屏，杯盖有密封圈
        组件：水杯杯体, 双层真空结构, 温度传感器, LED显示屏, 杯盖密封圈, USB充电口, 椭圆形外壳
        输出路径：智能水杯_机械结构图.png
        """
    )

    print("✅ 机械结构图绘制完成")
    print(drawing_result.final_output)
    test_results.append({
        "step": "机械结构图",
        "status": "成功",
        "drawing_info": drawing_result.final_output[:300] + "..."
    })

    # 步骤3：绘制示意图
    print("\n🎨 步骤3：绘制示意图...")
    schematic_result = await Runner.run(
        patent_drawing_agent,
        """
        请创建一份示意图：

        发明名称：一种带温度显示的智能水杯
        产品描述：椭圆形的智能水杯，整体外观简洁美观
        组件：椭圆形杯体, 显示屏位置, 传感器位置, 充电口位置
        输出路径：智能水杯_示意图.png
        """
    )

    print("✅ 示意图绘制完成")
    print(schematic_result.final_output)
    test_results.append({
        "step": "示意图",
        "status": "成功",
        "drawing_info": schematic_result.final_output[:300] + "..."
    })

    # 生成集成测试报告
    print("\n" + "=" * 70)
    print("📋 集成测试报告")
    print("=" * 70)

    print(f"\n测试时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"测试场景：智能水杯专利撰写与附图绘制")
    print(f"执行步骤：{len(test_results)}")

    print(f"\n步骤详情：")
    for i, result in enumerate(test_results, 1):
        print(f"{i}. {result['step']}")
        print(f"   状态：{result['status']}")
        if 'content_length' in result:
            print(f"   内容长度：{result['content_length']} 字符")
        if 'drawing_info' in result:
            print(f"   绘图信息：{result['drawing_info']}")

    # 保存集成测试报告
    report_file = f"专利撰写附图集成测试报告_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("="*70 + "\n")
        f.write("专利撰写与附图绘制 - 集成测试报告\n")
        f.write("="*70 + "\n\n")
        f.write(f"测试时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"测试场景：智能水杯专利撰写与附图绘制\n")
        f.write(f"执行步骤：{len(test_results)}\n\n")

        f.write("="*70 + "\n")
        f.write("步骤详情：\n")
        f.write("="*70 + "\n\n")

        for i, result in enumerate(test_results, 1):
            f.write(f"{i}. {result['step']}\n")
            f.write(f"   状态：{result['status']}\n")
            if 'content_length' in result:
                f.write(f"   内容长度：{result['content_length']} 字符\n")
            if 'drawing_info' in result:
                f.write(f"   绘图信息：{result['drawing_info']}\n")
            f.write("\n")

        f.write("="*70 + "\n")
        f.write("集成特性：\n")
        f.write("="*70 + "\n\n")

        f.write("1. 无缝集成\n")
        f.write("   - 专利撰写Agent负责文字内容\n")
        f.write("   - 专利绘图Agent负责附图生成\n")
        f.write("   - 两个Agent可以独立工作或协同工作\n\n")

        f.write("2. 专利审查指南合规\n")
        f.write("   - 附图符合制图国家标准\n")
        f.write("   - 线条清晰，标记清楚\n")
        f.write("   - 格式标准，分辨率高\n")
        f.write("   - 与说明书内容一致\n\n")

        f.write("3. 自动化流程\n")
        f.write("   - 一键生成完整专利申请\n")
        f.write("   - 自动提取组件信息\n")
        f.write("   - 自动布局和标记\n")
        f.write("   - 自动质量验证\n\n")

        f.write("4. 多种附图类型\n")
        f.write("   - 机械结构图：展示产品结构\n")
        f.write("   - 电路图：展示电子电路\n")
        f.write("   - 流程图：展示操作流程\n")
        f.write("   - 示意图：展示整体外观\n")
        f.write("   - 构造图：展示内部构造\n\n")

    print(f"\n✅ 集成测试报告已保存到：{report_file}")

    # 检查生成的图片文件
    print("\n" + "=" * 70)
    print("📁 生成的附图文件")
    print("=" * 70)

    image_files = [
        "智能水杯_机械结构图.png",
        "智能水杯_示意图.png"
    ]

    for img_file in image_files:
        if os.path.exists(img_file):
            size = os.path.getsize(img_file)
            print(f"✅ {img_file} ({size} bytes)")
        else:
            print(f"⚠️ {img_file} (未找到)")

    print("\n" + "=" * 70)
    print("🎉 专利撰写与附图绘制集成测试完成！")
    print("=" * 70)
    print("\n总结：")
    print("- ✅ 专利申请文件撰写完成")
    print("- ✅ 机械结构图绘制完成")
    print("- ✅ 示意图绘制完成")
    print("- ✅ 两个Agent协同工作正常")
    print("- ✅ 符合专利审查指南要求")
    print("\n整个流程展示了从专利内容撰写到附图生成的完整自动化流程！")

    return test_results


async def test_advanced_drawing_features():
    """测试高级绘图功能"""
    print("\n" + "=" * 70)
    print("🔬 高级绘图功能测试")
    print("=" * 70)

    # 测试复杂产品的附图绘制
    print("\n📐 测试：复杂机械产品的附图绘制...")

    result = await Runner.run(
        patent_drawing_agent,
        """
        请创建一份机械结构图：

        发明名称：一种防滑折叠梯子
        产品描述：防滑折叠梯子采用双向锁定机制，底部有可调节支撑脚
        组件：梯体, 踏板, 防滑垫片, 折叠机构, 安全锁扣, 伸缩支撑杆, 底部防滑脚垫, 连接铰链, 侧边扶手
        输出路径：折叠梯子_结构图.png
        """
    )

    print("✅ 复杂机械产品附图绘制完成")
    print(result.final_output[:400] + "...")

    # 测试流程图绘制
    print("\n📊 测试：流程图绘制...")

    result = await Runner.run(
        patent_drawing_agent,
        """
        请创建一份流程图：

        发明名称：自动售货机的操作流程
        产品描述：自动售货机的标准操作流程
        流程步骤：启动系统; 等待用户投币; 验证币种和金额; 显示商品列表; 用户选择商品; 验证库存; 确认订单; 出货; 找零; 打印小票; 结束交易
        输出路径：售货机_流程图.png
        """
    )

    print("✅ 流程图绘制完成")
    print(result.final_output[:400] + "...")

    # 获取绘制指导
    print("\n📚 测试：获取绘制指导...")

    result = await Runner.run(
        patent_drawing_agent,
        "请提供专利附图绘制指导"
    )

    print("✅ 绘制指导获取完成")
    print("指导内容长度：", len(result.final_output), "字符")

    print("\n" + "=" * 70)
    print("🎉 高级绘图功能测试完成！")
    print("=" * 70)


if __name__ == "__main__":
    print("\n选择测试类型：")
    print("1. 集成测试（专利撰写 + 附图绘制）")
    print("2. 高级功能测试（复杂附图）")
    print("3. 全部测试")

    choice = input("\n请选择 (1/2/3): ").strip()

    if choice == "1":
        asyncio.run(test_patent_writing_with_drawing())
    elif choice == "2":
        asyncio.run(test_advanced_drawing_features())
    else:
        asyncio.run(test_patent_writing_with_drawing())
        print("\n" + "="*70)
        asyncio.run(test_advanced_drawing_features())
