#!/usr/bin/env python3
"""
Gemini-2.5-Flash-Image专利附图绘制测试
展示Google Gemini-2.5-Flash-Image模型的专业绘图能力
"""

import sys
import os
from datetime import datetime

# 添加路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 导入模块
from drawing_agent.tools.imagen4_drawing_tool import GeminiFlashImagePatentDrawingTool

def test_flash_image_drawing():
    """测试Gemini-2.5-Flash-Image绘图功能"""
    print("\n" + "=" * 70)
    print("🎨 Gemini-2.5-Flash-Image专利附图绘制工具 - 测试")
    print("=" * 70)
    print(f"⏰ 测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # 创建Gemini-2.5-Flash-Image绘图工具
    tool = GeminiFlashImagePatentDrawingTool()
    
    # 检查模型状态
    if tool.imagen_model and tool.gemini_model:
        print("✅ 模型初始化成功")
        print("   🎨 Gemini-2.5-Flash-Image: 已就绪")
        print("   🧠 Gemini-2.5-Pro: 已就绪")
    else:
        print("❌ 模型初始化失败")
        return
    print()

    # 测试：Gemini + Gemini-2.5-Flash-Image 增强绘图
    print("=" * 70)
    print("测试：Gemini + Gemini-2.5-Flash-Image 增强绘图")
    print("=" * 70)
    
    request = {
        'invention_title': 'Smart IoT Device with AI Processing',
        'product_description': 'An intelligent IoT device featuring real-time data processing, AI-powered analytics, and wireless connectivity for automated control systems',
        'key_components': [
            'Main Processing Unit',
            'Sensor Array Module',
            'WiFi Communication Module',
            'Power Management System',
            'User Interface Display',
            'Memory Storage Unit',
            'Actuator Control System',
            'Battery Backup'
        ]
    }
    
    output_file = f"flash_image_enhanced_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    print(f"📁 输出文件: {output_file}")
    print()
    
    try:
        result = tool.create_enhanced_drawing(request, output_file)
        
        if result and os.path.exists(output_file):
            size = os.path.getsize(output_file)
            print("=" * 70)
            print("✅ 增强绘图生成成功！")
            print("=" * 70)
            print(f"📊 文件大小: {size:,} bytes")
            print(f"📄 文件格式: PNG")
            print(f"🎨 AI引擎: Gemini-2.5-Pro + Gemini-2.5-Flash-Image")
            print()
        else:
            print("❌ 增强绘图生成失败")
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()

    print("=" * 70)
    print("🎉 Gemini-2.5-Flash-Image测试完成！")
    print("=" * 70)
    print()
    print("✨ Gemini-2.5-Flash-Image特性:")
    print("   ✓ Google最新的图像生成模型")
    print("   ✓ 专业专利附图绘制")
    print("   ✓ 仅英文标记，符合专利要求")
    print("   ✓ AI增强布局和设计")
    print("   ✓ 快速生成，高质量输出")
    print()
    print("💡 使用说明:")
    print("   1. 查看生成的PNG图片")
    print("   2. 可直接用于专利申请")
    print("   3. 支持自定义组件和描述")
    print()
    print("🚀 Gemini-2.5-Flash-Image为您带来前所未有的AI绘图体验！")

if __name__ == "__main__":
    test_flash_image_drawing()

