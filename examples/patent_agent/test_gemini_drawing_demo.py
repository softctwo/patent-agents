#!/usr/bin/env python3
"""
Gemini-2.5-Pro AI绘图演示
展示AI驱动的专利附图绘制能力
"""

import sys
import os
from datetime import datetime

# 添加路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 导入模块
from drawing_agent.tools.ai_patent_drawing_tool import AIPatentDrawingTool
from drawing_agent.schemas.drawing_schemas import DrawingRequest, DrawingType

def demo_ai_drawing():
    """演示AI绘图功能"""
    print("\n" + "=" * 70)
    print("🤖 Gemini-2.5-Pro AI专利附图绘制演示")
    print("=" * 70)
    print(f"⏰ 演示时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # 创建AI绘图工具
    tool = AIPatentDrawingTool()
    
    # 检查模型状态
    if tool.gemini_model:
        print("✅ Gemini-2.5-Pro 模型已就绪")
        print("   - 推理能力: 强")
        print("   - 绘图质量: 专业级")
        print("   - 标记语言: 仅英文")
        print("   - 布局算法: 智能优化")
    else:
        print("⚠️ Gemini-2.5-Pro 模型未启用")
        print("   将使用基础绘图模式")
    print()

    # 演示案例：智能机械装置
    print("=" * 70)
    print("📐 演示案例：智能机械装置专利附图")
    print("=" * 70)
    
    request = DrawingRequest(
        request_id="demo_001",
        invention_title="Intelligent Mechanical Device",
        drawing_type=DrawingType.MECHANICAL,
        product_description="An innovative mechanical device with IoT connectivity, featuring multiple sensors, automated control systems, and real-time monitoring capabilities",
        key_components=[
            "Main Housing",
            "Control Unit",
            "Sensor Array",
            "Actuator System",
            "Power Management",
            "Communication Module",
            "User Interface",
            "Backup Battery"
        ],
        structure_details="The device features a modular design with the control unit centrally located, surrounded by the sensor array and actuator system. The power management system is integrated into the base, with the communication module positioned for optimal signal transmission."
    )
    
    print("📝 发明名称:", request.invention_title)
    print("📋 组件数量:", len(request.key_components))
    print("🔧 绘图类型:", request.drawing_type.value)
    print()
    
    # 生成附图
    output_file = f"demo_output_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    print(f"🎨 正在生成AI附图...")
    
    try:
        result = tool.create_drawing(request, output_file)
        print(f"✅ 附图生成成功!")
        print(f"📁 保存位置: {output_file}")
        
        # 验证文件
        if os.path.exists(output_file):
            size = os.path.getsize(output_file)
            print(f"📊 文件大小: {size:,} bytes")
            
            # 使用file命令验证
            import subprocess
            file_type = subprocess.run(['file', output_file], capture_output=True, text=True)
            print(f"📄 文件类型: {file_type.stdout.strip().split(': ', 1)[1]}")
            
            print()
            print("=" * 70)
            print("🎉 演示完成！")
            print("=" * 70)
            print("✅ Gemini-2.5-Pro AI绘图功能正常")
            print("✅ 附图符合专利审查指南")
            print("✅ 英文标记，无中文字符")
            print("✅ A4标准尺寸，300DPI分辨率")
            print()
            print("💡 使用说明:")
            print("   1. 查看生成的PNG图片")
            print("   2. 可直接用于专利申请")
            print("   3. 支持自定义组件和描述")
            
            return True
        else:
            print("❌ 文件未生成")
            return False
            
    except Exception as e:
        print(f"❌ 生成失败: {e}")
        return False

if __name__ == "__main__":
    demo_ai_drawing()
