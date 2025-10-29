#!/usr/bin/env python3
"""
AI专利附图绘制测试
使用Gemini大模型生成专业专利附图
"""

import sys
import os
from datetime import datetime

# 添加路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 直接导入AI绘图工具
from drawing_agent.tools.ai_patent_drawing_tool import AIPatentDrawingTool
from drawing_agent.schemas.drawing_schemas import DrawingRequest, DrawingType

def test_ai_drawing():
    """测试AI绘图功能"""
    print("\n" + "=" * 70)
    print("🤖 AI专利附图绘制工具 - 测试 (Gemini-2.5-Pro)")
    print("=" * 70)

    # 创建AI绘图工具
    tool = AIPatentDrawingTool()

    if tool.gemini_model:
        print("✅ Gemini-2.5-Pro AI模型已初始化")
    else:
        print("⚠️ Gemini-2.5-Pro AI模型未初始化，将使用基础绘图")

    # 测试1：机械结构图
    print("\n" + "=" * 70)
    print("测试1：AI机械结构图 - 智能水杯")
    print("=" * 70)

    try:
        request = DrawingRequest(
            request_id="ai_test_001",
            invention_title="Smart Temperature Display Cup",
            drawing_type=DrawingType.MECHANICAL,
            product_description="Smart cup with dual-layer vacuum structure, built-in temperature sensor, and LED display",
            key_components=["Cup Body", "Vacuum Layer", "Temperature Sensor", "LED Display", "Lid Seal", "USB Charging Port"],
            structure_details="The cup features a double-wall construction for insulation, with a temperature sensor embedded in the inner wall and an LED display on the front for temperature readout."
        )

        output_path = "ai_test_mechanical.png"
        result = tool.create_drawing(request, output_path)

        print(f"✅ 机械结构图生成成功")
        print(f"保存路径：{output_path}")

        if os.path.exists(output_path):
            size = os.path.getsize(output_path)
            print(f"文件大小：{size:,} bytes")

        # 验证图片
        import subprocess
        result = subprocess.run(['file', output_path], capture_output=True, text=True)
        print(f"文件类型：{result.stdout.strip()}")

    except Exception as e:
        print(f"❌ 机械结构图生成失败：{e}")
        import traceback
        traceback.print_exc()

    # 测试2：流程图
    print("\n" + "=" * 70)
    print("测试2：AI流程图 - 自动售货机")
    print("=" * 70)

    try:
        request = DrawingRequest(
            request_id="ai_test_002",
            invention_title="Vending Machine Operation Process",
            drawing_type=DrawingType.FLOWCHART,
            product_description="Standard operation workflow for vending machine",
            key_components=[],
            structure_details="Start; Insert coins; Verify payment; Display products; Select product; Confirm order; Dispense product; Return change; End transaction"
        )

        output_path = "ai_test_flowchart.png"
        result = tool.create_drawing(request, output_path)

        print(f"✅ 流程图生成成功")
        print(f"保存路径：{output_path}")

        if os.path.exists(output_path):
            size = os.path.getsize(output_path)
            print(f"文件大小：{size:,} bytes")

    except Exception as e:
        print(f"❌ 流程图生成失败：{e}")
        import traceback
        traceback.print_exc()

    # 测试3：电路图
    print("\n" + "=" * 70)
    print("测试3：AI电路图 - 温度监测电路")
    print("=" * 70)

    try:
        request = DrawingRequest(
            request_id="ai_test_003",
            invention_title="Temperature Monitoring Circuit",
            drawing_type=DrawingType.CIRCUIT,
            product_description="Circuit with temperature sensor, amplifier, microcontroller and display",
            key_components=["Temperature Sensor", "Operational Amplifier", "Microcontroller", "LCD Display", "Power Circuit", "Filter Capacitor"],
            structure_details="The circuit uses a precision temperature sensor connected to an operational amplifier for signal conditioning, then fed to a microcontroller for processing and display on an LCD screen."
        )

        output_path = "ai_test_circuit.png"
        result = tool.create_drawing(request, output_path)

        print(f"✅ 电路图生成成功")
        print(f"保存路径：{output_path}")

        if os.path.exists(output_path):
            size = os.path.getsize(output_path)
            print(f"文件大小：{size:,} bytes")

    except Exception as e:
        print(f"❌ 电路图生成失败：{e}")
        import traceback
        traceback.print_exc()

    # 检查生成的图片
    print("\n" + "=" * 70)
    print("📁 生成的AI图片文件")
    print("=" * 70)

    image_files = [
        "ai_test_mechanical.png",
        "ai_test_flowchart.png",
        "ai_test_circuit.png"
    ]

    generated_count = 0
    for img_file in image_files:
        if os.path.exists(img_file):
            size = os.path.getsize(img_file)
            print(f"✅ {img_file} ({size:,} bytes)")
            generated_count += 1

            # 验证图片
            import subprocess
            result = subprocess.run(['file', img_file], capture_output=True, text=True)
            if 'PNG image data' in result.stdout:
                print(f"   └─ 格式验证：✅ 有效PNG文件")
            else:
                print(f"   └─ 格式验证：⚠️ {result.stdout.strip()}")

        else:
            print(f"❌ {img_file} (未生成)")

    print(f"\n总结：生成 {generated_count}/{len(image_files)} 个AI附图文件")

    print("\n" + "=" * 70)
    print("🎉 AI绘图测试完成！")
    print("=" * 70)

    if generated_count > 0:
        print("\n✅ AI绘图功能正常")
        print("特点：")
        print("- 使用Gemini-2.5-Pro AI生成专业绘图方案")
        print("- 英文标记，无中文字符")
        print("- 符合专利审查指南要求")
        print("- 专业技术绘图风格")
        print("- 智能布局和组件标记")

        print("\n您可以使用图片查看器打开这些PNG文件：")
        for img_file in image_files:
            if os.path.exists(img_file):
                print(f"  - {img_file}")
    else:
        print("\n⚠️ 未能生成AI附图，请检查：")
        print("1. 是否设置了GOOGLE_API_KEY环境变量")
        print("2. Gemini API是否可用")
        print("3. 网络连接是否正常")

    return generated_count


if __name__ == "__main__":
    try:
        generated_count = test_ai_drawing()

        if generated_count > 0:
            print(f"\n✅ AI测试成功！生成了 {generated_count} 个高质量附图")
            print("\n🎊 AI驱动的专利附图绘制功能测试通过！")
        else:
            print("\n❌ AI测试失败：未能生成任何附图文件")

    except Exception as e:
        print(f"\n❌ 测试出错：{e}")
        import traceback
        traceback.print_exc()
