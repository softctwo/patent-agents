#!/usr/bin/env python3
"""
检查exp模型返回的文本内容
"""

import os
import google.generativeai as genai
from datetime import datetime

# 设置API密钥
API_KEY = "AIzaSyAPnIWfYq8oGS7yAmNXdP0k8NuPB_gu5VU"
os.environ['GOOGLE_API_KEY'] = API_KEY
genai.configure(api_key=API_KEY)

def test_and_save_response():
    """测试并保存响应内容"""
    print("=" * 70)
    print("🔍 检查models/gemini-2.0-flash-exp-image-generation的响应")
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
Include title "Figure 1: Smart Blockchain Hardware Wallet".
"""

    model_name = 'models/gemini-2.0-flash-exp-image-generation'

    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": 0.2,
                "top_p": 0.9,
                "max_output_tokens": 8192,
            }
        )

        # 保存完整响应
        output_file = f"flash_exp_response_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("=" * 70 + "\n")
            f.write("models/gemini-2.0-flash-exp-image-generation 完整响应\n")
            f.write("=" * 70 + "\n\n")

            if response.candidates and response.candidates[0].content.parts:
                for i, part in enumerate(response.candidates[0].content.parts):
                    f.write(f"部分 {i+1}:\n")
                    f.write("-" * 70 + "\n")

                    if hasattr(part, 'text') and part.text:
                        f.write(part.text)
                        f.write("\n\n")
                    elif hasattr(part, 'inline_data') and part.inline_data and part.inline_data.data:
                        f.write(f"[图像数据: {len(part.inline_data.data):,} bytes]\n\n")
                    else:
                        f.write("[未知内容类型]\n\n")

        print(f"✅ 响应内容已保存到: {output_file}")

        # 显示部分内容
        if response.candidates and response.candidates[0].content.parts:
            for i, part in enumerate(response.candidates[0].content.parts):
                if hasattr(part, 'text') and part.text:
                    text = part.text
                    print(f"\n📝 部分 {i+1} 内容预览 (前1000字符):")
                    print("-" * 70)
                    print(text[:1000])
                    if len(text) > 1000:
                        print("\n... (内容已截断)")

        return output_file

    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return None

if __name__ == "__main__":
    test_and_save_response()
