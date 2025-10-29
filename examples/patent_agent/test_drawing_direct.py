#!/usr/bin/env python3
"""
直接测试专利附图绘制工具
绕过Agent框架，直接测试核心绘图功能
"""

import sys
import os
from datetime import datetime

# 添加路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'drawing_agent'))

# 直接导入工具类，避免相对导入问题
from tools.patent_drawing_tool import PatentDrawingTool
from schemas.drawing_schemas import DrawingRequest, DrawingType

def test_drawing_tool():
    """直接测试绘图工具"""
    print("\n" + "=" * 70)
    print("🧪 专利附图绘制工具 - 直接测试")
    print("=" * 70)

    # 创建绘图工具实例
    tool = PatentDrawingTool()
    print("✅ 绘图工具初始化成功")

    # 测试1：机械结构图
    print("\n" + "=" * 70)
    print("测试1：机械结构图")
    print("=" * 70)

    try:
        request = DrawingRequest(
            request_id="test_001",
            invention_title="一种便于携带的折叠式收纳盒",
            drawing_type=DrawingType.MECHANICAL,
            product_description="收纳盒采用可折叠设计，方便携带和存储",
            key_components=["盒体", "折叠铰链", "卡扣固定装置", "侧壁加强筋"],
        )

        output_path = "test_mechanical.png"
        result = tool.create_drawing(request, output_path)

        print(f"✅ 机械结构图生成成功")
        print(f"保存路径：{output_path}")

        if os.path.exists(output_path):
            size = os.path.getsize(output_path)
            print(f"文件大小：{size:,} bytes")

    except Exception as e:
        print(f"❌ 机械结构图生成失败：{e}")

    # 测试2：电路图
    print("\n" + "=" * 70)
    print("测试2：电路图")
    print("=" * 70)

    try:
        request = DrawingRequest(
            request_id="test_002",
            invention_title="一种带温度显示的智能水杯",
            drawing_type=DrawingType.CIRCUIT,
            product_description="双层真空结构，内置温度传感器和LED显示屏",
            key_components=["温度传感器", "LED显示屏", "主控芯片", "电池", "连接线"],
        )

        output_path = "test_circuit.png"
        result = tool.create_drawing(request, output_path)

        print(f"✅ 电路图生成成功")
        print(f"保存路径：{output_path}")

        if os.path.exists(output_path):
            size = os.path.getsize(output_path)
            print(f"文件大小：{size:,} bytes")

    except Exception as e:
        print(f"❌ 电路图生成失败：{e}")

    # 测试3：流程图
    print("\n" + "=" * 70)
    print("测试3：流程图")
    print("=" * 70)

    try:
        request = DrawingRequest(
            request_id="test_003",
            invention_title="自动售货机的操作流程",
            drawing_type=DrawingType.FLOWCHART,
            product_description="自动售货机的标准操作流程",
            key_components=[],
            structure_details="投币; 选择商品; 确认订单; 取商品; 找零; 结束"
        )

        output_path = "test_flowchart.png"
        result = tool.create_drawing(request, output_path)

        print(f"✅ 流程图生成成功")
        print(f"保存路径：{output_path}")

        if os.path.exists(output_path):
            size = os.path.getsize(output_path)
            print(f"文件大小：{size:,} bytes")

    except Exception as e:
        print(f"❌ 流程图生成失败：{e}")

    # 测试4：示意图
    print("\n" + "=" * 70)
    print("测试4：示意图")
    print("=" * 70)

    try:
        request = DrawingRequest(
            request_id="test_004",
            invention_title="一种带指纹识别的区块链硬件钱包",
            drawing_type=DrawingType.SCHEMATIC,
            product_description="椭圆形的便携式硬件钱包，内置指纹识别和显示屏",
            key_components=["椭圆形外壳体", "OLED显示屏", "指纹识别模块", "PCB主板", "锂电池", "USB-C接口"],
        )

        output_path = "test_schematic.png"
        result = tool.create_drawing(request, output_path)

        print(f"✅ 示意图生成成功")
        print(f"保存路径：{output_path}")

        if os.path.exists(output_path):
            size = os.path.getsize(output_path)
            print(f"文件大小：{size:,} bytes")

    except Exception as e:
        print(f"❌ 示意图生成失败：{e}")

    # 测试5：构造图
    print("\n" + "=" * 70)
    print("测试5：构造图")
    print("=" * 70)

    try:
        request = DrawingRequest(
            request_id="test_005",
            invention_title="一种防滑折叠梯子",
            drawing_type=DrawingType.STRUCTURE,
            product_description="折叠梯子采用双向锁定机制，底部有可调节支撑脚",
            key_components=["梯体", "踏板", "防滑垫片", "折叠机构", "安全锁扣", "伸缩支撑杆"],
        )

        output_path = "test_structure.png"
        result = tool.create_drawing(request, output_path)

        print(f"✅ 构造图生成成功")
        print(f"保存路径：{output_path}")

        if os.path.exists(output_path):
            size = os.path.getsize(output_path)
            print(f"文件大小：{size:,} bytes")

    except Exception as e:
        print(f"❌ 构造图生成失败：{e}")

    # 检查生成的图片
    print("\n" + "=" * 70)
    print("📁 生成的图片文件")
    print("=" * 70)

    image_files = [
        "test_mechanical.png",
        "test_circuit.png",
        "test_flowchart.png",
        "test_schematic.png",
        "test_structure.png"
    ]

    generated_count = 0
    for img_file in image_files:
        if os.path.exists(img_file):
            size = os.path.getsize(img_file)
            print(f"✅ {img_file} ({size:,} bytes)")
            generated_count += 1
        else:
            print(f"❌ {img_file} (未生成)")

    print(f"\n总结：生成 {generated_count}/{len(image_files)} 个附图文件")

    # 质量验证测试
    print("\n" + "=" * 70)
    print("🔍 质量验证")
    print("=" * 70)

    if os.path.exists("test_mechanical.png"):
        try:
            validation = tool.validate_drawing
            # 这里需要先创建一个绘图对象来验证
            from schemas.drawing_schemas import PatentDrawing, DrawingElement, RectangleElement

            test_drawing = PatentDrawing(
                drawing_id="test",
                title="测试附图",
                drawing_type=DrawingType.MECHANICAL
            )
            test_drawing.elements.append(
                RectangleElement(
                    element_type="border",
                    position={"x": 50, "y": 50},
                    width=200,
                    height=150
                )
            )

            validation_result = tool.validate_drawing(test_drawing)

            print("✅ 质量验证完成")
            for key, value in validation_result.items():
                status = "✅" if value else "❌"
                print(f"  {status} {key}: {value}")

        except Exception as e:
            print(f"⚠️ 质量验证出错：{e}")

    print("\n" + "=" * 70)
    print("🎉 绘图工具测试完成！")
    print("=" * 70)

    return generated_count


if __name__ == "__main__":
    try:
        generated_count = test_drawing_tool()

        if generated_count > 0:
            print(f"\n✅ 测试成功！生成了 {generated_count} 个附图文件")
            print("\n您可以使用图片查看器打开这些PNG文件查看附图效果：")
            print("- test_mechanical.png (机械结构图)")
            print("- test_circuit.png (电路图)")
            print("- test_flowchart.png (流程图)")
            print("- test_schematic.png (示意图)")
            print("- test_structure.png (构造图)")
        else:
            print("\n❌ 测试失败：未能生成任何附图文件")

    except Exception as e:
        print(f"\n❌ 测试出错：{e}")
        import traceback
        traceback.print_exc()
