#!/usr/bin/env python3
"""
使用models/前缀的Gemini-2.0-Flash-Preview-Image-Generation测试
"""

import os
import sys
import google.generativeai as genai
from datetime import datetime
from PIL import Image
import numpy as np

# 设置API密钥
API_KEY = "AIzaSyAPnIWfYq8oGS7yAmNXdP0k8NuPB_gu5VU"
os.environ['GOOGLE_API_KEY'] = API_KEY
genai.configure(api_key=API_KEY)

# 尝试导入OCR库
try:
    import easyocr
    OCR_AVAILABLE = True
    print("✅ EasyOCR 可用")
except ImportError:
    OCR_AVAILABLE = False
    print("⚠️ EasyOCR 不可用")

def test_flash_with_models_prefix():
    """使用models/前缀测试"""
    print("\n" + "=" * 70)
    print("🎨 测试Gemini-2.0-Flash-Preview-Image-Generation（使用models/前缀）")
    print("=" * 70)

    prompt = """
Create a professional patent technical drawing of a Smart Blockchain Hardware Wallet.

The drawing should include:
1. Elliptical Enclosure
2. Biometric Fingerprint Scanner
3. OLED Display Screen
4. PCB Main Board
5. Lithium Battery
6. Wireless Charging Coil
7. USB-C Interface
8. Physical Buttons
9. Modular Security Chip
10. Anti-tamper Structure

Use professional patent drawing style with clean black lines on white background.
Include numbered labels for each component.
"""

    # 尝试不同的模型名称
    model_names = [
        'models/gemini-2.0-flash-preview-image-generation',
        'gemini-2.0-flash-preview-image-generation',
        'gemini-2.0-flash-preview-image-generation-exp-02-05',
    ]

    for model_name in model_names:
        print(f"\n📦 尝试模型: {model_name}")
        print("-" * 70)

        try:
            model = genai.GenerativeModel(model_name)
            print(f"✅ 模型 {model_name} 初始化成功")

            print("\n🧠 正在生成图像...")
            response = model.generate_content(
                prompt,
                generation_config={
                    "temperature": 0.2,
                    "top_p": 0.9,
                }
            )

            print("✅ 请求完成")
            print(f"响应类型: {type(response)}")

            # 检查响应内容
            image_count = 0
            text_count = 0

            if response.candidates and response.candidates[0].content.parts:
                print(f"📊 响应部分数量: {len(response.candidates[0].content.parts)}")

                for i, part in enumerate(response.candidates[0].content.parts):
                    if hasattr(part, 'inline_data') and part.inline_data and part.inline_data.data:
                        image_count += 1
                        print(f"   部分 {i+1}: 图像数据 ({len(part.inline_data.data):,} bytes)")
                    elif hasattr(part, 'text') and part.text:
                        text_count += 1
                        print(f"   部分 {i+1}: 文本内容 ({len(part.text)} 字符)")

            print(f"\n📈 响应统计:")
            print(f"   图像部分: {image_count}")
            print(f"   文本部分: {text_count}")

            if image_count > 0:
                print(f"\n✅ 成功生成图像！")
                return True

        except Exception as e:
            print(f"❌ 模型测试失败: {e}")
            continue

    return False

def main():
    print("=" * 70)
    print("🎨 Gemini-2.0-Flash-Preview-Image-Generation 模型前缀测试")
    print("=" * 70)

    success = test_flash_with_models_prefix()

    if success:
        print("\n🎉 测试成功！")
    else:
        print("\n❌ 所有模型尝试失败")
        print("\n💡 建议:")
        print("1. 检查Google AI API权限")
        print("2. 验证模型名称")
        print("3. 使用Gemini-2.5-Pro + Python渲染方案")

if __name__ == "__main__":
    main()
