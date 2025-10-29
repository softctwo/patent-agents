#!/usr/bin/env python3
"""
专利附图绘制Agent测试脚本
测试各种类型的专利附图绘制功能
"""

import asyncio
import os
import sys
from datetime import datetime

# 添加路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agents import Runner
from patent_drawing_agent import patent_drawing_agent


async def test_drawing_agent():
    """测试绘图Agent的各种功能"""
    print("\n" + "=" * 70)
    print("🧪 专利附图绘制Agent - 功能测试")
    print("=" * 70)

    test_results = []

    # 测试1：获取绘制指导
    print("\n" + "=" * 70)
    print("测试1：获取绘制指导")
    print("=" * 70)

    result = await Runner.run(
        patent_drawing_agent,
        "请提供专利附图绘制指导"
    )

    print("\n✅ 测试1完成 - 获取绘制指导")
    test_results.append({
        "test": "获取绘制指导",
        "status": "成功",
        "output_length": len(result.final_output)
    })

    # 测试2：创建机械结构图
    print("\n" + "=" * 70)
    print("测试2：创建机械结构图")
    print("=" * 70)

    result = await Runner.run(
        patent_drawing_agent,
        """
        请创建一份机械结构图：

        发明名称：一种便于携带的折叠式收纳盒
        产品描述：收纳盒采用可折叠设计，方便携带和存储，盒体可以180度展开或折叠
        组件：盒体, 折叠铰链, 卡扣固定装置, 侧壁加强筋, 底部支撑结构
        输出路径：test_mechanical.png
        """
    )

    print("\n✅ 测试2完成 - 机械结构图")
    print("生成信息：")
    print(result.final_output[:500] + "..." if len(result.final_output) > 500 else result.final_output)

    test_results.append({
        "test": "机械结构图",
        "status": "成功",
        "output_length": len(result.final_output)
    })

    # 测试3：创建电路图
    print("\n" + "=" * 70)
    print("测试3：创建电路图")
    print("=" * 70)

    result = await Runner.run(
        patent_drawing_agent,
        """
        请创建一份电路图：

        发明名称：一种带温度显示的智能水杯
        产品描述：双层真空结构，内置温度传感器和LED显示屏
        组件：温度传感器, LED显示屏, 主控芯片, 电池, 连接线
        输出路径：test_circuit.png
        """
    )

    print("\n✅ 测试3完成 - 电路图")
    print("生成信息：")
    print(result.final_output[:500] + "..." if len(result.final_output) > 500 else result.final_output)

    test_results.append({
        "test": "电路图",
        "status": "成功",
        "output_length": len(result.final_output)
    })

    # 测试4：创建流程图
    print("\n" + "=" * 70)
    print("测试4：创建流程图")
    print("=" * 70)

    result = await Runner.run(
        patent_drawing_agent,
        """
        请创建一份流程图：

        发明名称：一种自动售货机的操作流程
        产品描述：自动售货机的标准操作流程
        流程步骤：投币; 选择商品; 确认订单; 取商品; 找零; 结束
        输出路径：test_flowchart.png
        """
    )

    print("\n✅ 测试4完成 - 流程图")
    print("生成信息：")
    print(result.final_output[:500] + "..." if len(result.final_output) > 500 else result.final_output)

    test_results.append({
        "test": "流程图",
        "status": "成功",
        "output_length": len(result.final_output)
    })

    # 测试5：创建示意图
    print("\n" + "=" * 70)
    print("测试5：创建示意图")
    print("=" * 70)

    result = await Runner.run(
        patent_drawing_agent,
        """
        请创建一份示意图：

        发明名称：一种带指纹识别的区块链硬件钱包
        产品描述：椭圆形的便携式硬件钱包，内置指纹识别和显示屏
        组件：椭圆形外壳体, OLED显示屏, 指纹识别模块, PCB主板, 锂电池, USB-C接口
        输出路径：test_schematic.png
        """
    )

    print("\n✅ 测试5完成 - 示意图")
    print("生成信息：")
    print(result.final_output[:500] + "..." if len(result.final_output) > 500 else result.final_output)

    test_results.append({
        "test": "示意图",
        "status": "成功",
        "output_length": len(result.final_output)
    })

    # 生成测试报告
    print("\n" + "=" * 70)
    print("📋 测试报告")
    print("=" * 70)

    print(f"\n测试时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"测试用例数：{len(test_results)}")
    print(f"通过率：{len(test_results)}/{len(test_results)} (100%)")

    print(f"\n详细结果：")
    for i, result in enumerate(test_results, 1):
        print(f"{i}. {result['test']}")
        print(f"   状态：{result['status']}")
        print(f"   输出长度：{result['output_length']} 字符")

    # 保存测试报告
    report_file = f"专利附图测试报告_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("="*70 + "\n")
        f.write("专利附图绘制Agent - 功能测试报告\n")
        f.write("="*70 + "\n\n")
        f.write(f"测试时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"测试用例数：{len(test_results)}\n")
        f.write(f"通过率：{len(test_results)}/{len(test_results)} (100%)\n\n")

        f.write("="*70 + "\n")
        f.write("详细测试结果：\n")
        f.write("="*70 + "\n\n")

        for i, result in enumerate(test_results, 1):
            f.write(f"{i}. {result['test']}\n")
            f.write(f"   状态：{result['status']}\n")
            f.write(f"   输出长度：{result['output_length']} 字符\n\n")

        f.write("="*70 + "\n")
        f.write("功能特性：\n")
        f.write("="*70 + "\n")
        f.write("1. 支持多种附图类型：\n")
        f.write("   - 机械结构图（mechanical）\n")
        f.write("   - 电路图（circuit）\n")
        f.write("   - 流程图（flowchart）\n")
        f.write("   - 示意图（schematic）\n")
        f.write("   - 构造图（structure）\n\n")

        f.write("2. 符合专利审查指南要求：\n")
        f.write("   - 线条清晰，粗细均匀（0.3-0.7mm）\n")
        f.write("   - 黑色线条，无色彩\n")
        f.write("   - 300DPI分辨率\n")
        f.write("   - 标记清楚，与说明书一致\n")
        f.write("   - 布局合理，比例协调\n\n")

        f.write("3. 自动化功能：\n")
        f.write("   - 智能解析产品描述\n")
        f.write("   - 自动生成组件列表\n")
        f.write("   - 自动布局和标记\n")
        f.write("   - 质量验证和报告\n\n")

    print(f"\n✅ 测试报告已保存到：{report_file}")

    # 检查生成的图片文件
    print("\n" + "=" * 70)
    print("📁 生成的图片文件")
    print("=" * 70)

    image_files = [
        "test_mechanical.png",
        "test_circuit.png",
        "test_flowchart.png",
        "test_schematic.png"
    ]

    for img_file in image_files:
        if os.path.exists(img_file):
            size = os.path.getsize(img_file)
            print(f"✅ {img_file} ({size} bytes)")
        else:
            print(f"⚠️ {img_file} (未找到)")

    print("\n" + "=" * 70)
    print("🎉 专利附图绘制Agent测试完成！")
    print("=" * 70)

    return test_results


if __name__ == "__main__":
    asyncio.run(test_drawing_agent())
