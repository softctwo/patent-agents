#!/usr/bin/env python3
"""
Gemini-2.5-Pro快速绘图演示
一键生成智能专利附图
"""

import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from drawing_agent.tools.gemini_image_drawing_tool import create_gemini_intelligent_drawing

def main():
    print("\n" + "=" * 70)
    print("🚀 Gemini-2.5-Pro快速专利附图生成器")
    print("=" * 70)
    print()
    
    # 示例专利发明
    invention_examples = [
        {
            'name': '智能手表',
            'description': '具有健康监测、智能通知和无线充电功能的智能手表',
            'components': [
                'Watch Case',
                'Touch Screen Display',
                'Heart Rate Sensor',
                'Accelerometer',
                'Battery Pack',
                'Wireless Charging Coil',
                'Processor',
                'Memory Chip',
                'Bluetooth Module',
                'Speaker'
            ]
        },
        {
            'name': '智能家居控制器',
            'description': '集成语音识别、IoT连接和自动控制的智能家居中枢',
            'components': [
                'Main Controller',
                'Voice Recognition Module',
                'WiFi Module',
                'Zigbee Module',
                'Display Screen',
                'Power Supply',
                'Microphone Array',
                'Speaker System',
                'Memory Storage',
                'IR Transmitter'
            ]
        },
        {
            'name': '智能门锁',
            'description': '支持指纹、密码、NFC和远程控制的智能门锁系统',
            'components': [
                'Lock Body',
                'Fingerprint Scanner',
                'Keypad',
                'NFC Reader',
                'Motor Driver',
                'Battery Pack',
                'WiFi Module',
                'Bluetooth Module',
                'Status LED',
                'Emergency Key'
            ]
        }
    ]
    
    print("请选择要生成的专利附图类型：")
    for i, inv in enumerate(invention_examples, 1):
        print(f"{i}. {inv['name']}")
    
    choice = input("\n请输入选项 (1-3): ").strip()
    
    try:
        idx = int(choice) - 1
        if 0 <= idx < len(invention_examples):
            selected = invention_examples[idx]
            
            print(f"\n✅ 选择：{selected['name']}")
            print()
            
            # 创建绘图请求
            request = {
                'request_id': f'demo_{datetime.now().strftime("%Y%m%d_%H%M%S")}',
                'invention_title': f'Smart {selected["name"]} Device',
                'product_description': selected['description'],
                'key_components': selected['components'],
                'structure_details': f'The {selected["name"]} features a compact design with modular components for optimal performance and reliability.'
            }
            
            # 生成附图
            output_file = f"quick_demo_{selected['name'].replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            
            print("🎨 正在使用Gemini-2.5-Pro生成智能专利附图...")
            print("⏱️ 这可能需要几秒钟...")
            print()
            
            result = create_gemini_intelligent_drawing(request, output_file)
            
            if result and os.path.exists(result):
                size = os.path.getsize(result)
                print("=" * 70)
                print("✅ 专利附图生成成功！")
                print("=" * 70)
                print(f"📁 文件：{result}")
                print(f"📊 大小：{size:,} bytes")
                print(f"📏 规格：2480x3507像素 (A4, 300DPI)")
                print()
                print("✨ AI增强特性:")
                print("   ✓ 智能组件布局")
                print("   ✓ 专业英文标记")
                print("   ✓ 精确连接关系")
                print("   ✓ 符合专利标准")
                print()
                print("🎉 您可以打开图片查看效果！")
            else:
                print("❌ 生成失败，请重试")
        else:
            print("❌ 无效选项")
            
    except ValueError:
        print("❌ 请输入数字")
    except Exception as e:
        print(f"❌ 发生错误: {e}")

if __name__ == "__main__":
    main()

