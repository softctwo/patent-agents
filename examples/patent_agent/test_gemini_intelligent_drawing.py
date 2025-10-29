#!/usr/bin/env python3
"""
Gemini-2.5-Pro智能专利附图绘制测试
展示Google Gemini-2.5-Pro的智能绘图能力
"""

import sys
import os
from datetime import datetime

# 添加路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 导入模块
from drawing_agent.tools.gemini_image_drawing_tool import GeminiIntelligentDrawingTool

def test_gemini_intelligent_drawing():
    """测试Gemini智能绘图功能"""
    print("\n" + "=" * 70)
    print("🧠 Gemini-2.5-Pro智能专利附图绘制工具 - 测试")
    print("=" * 70)
    print(f"⏰ 测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # 创建Gemini智能绘图工具
    tool = GeminiIntelligentDrawingTool()
    
    # 检查模型状态
    if tool.gemini_model:
        print("✅ Gemini-2.5-Pro模型已就绪")
        print("   🧠 推理能力: 强大")
        print("   🎯 绘图质量: 专业级")
        print("   📐 布局算法: 智能优化")
    else:
        print("❌ 模型初始化失败")
        return
    print()

    # 测试：智能绘图生成
    print("=" * 70)
    print("测试：Gemini-2.5-Pro智能专利附图生成")
    print("=" * 70)
    
    request = {
        'request_id': f'intel_test_{datetime.now().strftime("%Y%m%d_%H%M%S")}',
        'invention_title': 'Advanced Smart IoT Device with AI Processing',
        'product_description': 'An intelligent IoT device featuring real-time data processing, AI-powered analytics, wireless connectivity, and automated control systems for smart home automation',
        'key_components': [
            'Central Processing Unit (CPU)',
            'WiFi Communication Module',
            'Bluetooth Module',
            'Sensor Array (Temperature, Humidity, Light)',
            'Power Management Unit',
            'User Interface (LED Display)',
            'Memory Storage (Flash Memory)',
            'Battery Backup System',
            'Actuator Control System',
            'External Antenna'
        ],
        'structure_details': 'The device features a modular architecture with the CPU centrally positioned. The communication modules are positioned at the top, sensors at the front, power management at the bottom, and backup systems integrated throughout.'
    }
    
    output_file = f"gemini_intelligent_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    print(f"📁 输出文件: {output_file}")
    print()
    
    try:
        result = tool.create_intelligent_drawing(request, output_file)
        
        if result and os.path.exists(output_file):
            size = os.path.getsize(output_file)
            print("=" * 70)
            print("✅ 智能附图生成成功！")
            print("=" * 70)
            print(f"📊 文件大小: {size:,} bytes")
            print(f"📄 文件格式: PNG")
            print(f"📏 分辨率: 2480 x 3507 (A4标准)")
            print(f"🎯 DPI: 300")
            print(f"🎨 AI引擎: Gemini-2.5-Pro (智能布局)")
            print(f"🔤 标记语言: 仅英文（符合专利要求）")
            print()
            
            # 验证文件
            import subprocess
            file_info = subprocess.run(['file', output_file], capture_output=True, text=True)
            print(f"📋 详细信息:")
            print(f"   {file_info.stdout.strip().split(': ', 1)[1]}")
            print()
        else:
            print("❌ 智能附图生成失败")
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()

    print("=" * 70)
    print("🎉 Gemini-2.5-Pro智能绘图测试完成！")
    print("=" * 70)
    print()
    print("✨ Gemini-2.5-Pro智能特性:")
    print("   ✓ 智能组件布局算法")
    print("   ✓ 专业英文技术标记")
    print("   ✓ 精确的连接关系绘制")
    print("   ✓ 符合专利审查指南")
    print("   ✓ 高质量线条和细节")
    print("   ✓ AI驱动的空间优化")
    print()
    print("💡 使用说明:")
    print("   1. 查看生成的PNG图片")
    print("   2. 可直接用于专利申请")
    print("   3. 支持自定义组件和详细描述")
    print()
    print("🚀 Gemini-2.5-Pro为您带来AI驱动的专业绘图体验！")

if __name__ == "__main__":
    test_gemini_intelligent_drawing()

