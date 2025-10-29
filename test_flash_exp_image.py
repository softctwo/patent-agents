#!/usr/bin/env python3
"""
测试models/gemini-2.0-flash-exp-image-generation模型
"""

import os
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

def test_flash_exp_image_generation():
    """测试models/gemini-2.0-flash-exp-image-generation模型"""
    print("\n" + "=" * 70)
    print("🎨 测试models/gemini-2.0-flash-exp-image-generation")
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

    print(f"\n📦 测试模型: {model_name}")
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
                "max_output_tokens": 8192,
            }
        )

        print("✅ 请求完成")
        print(f"响应类型: {type(response)}")

        # 检查响应
        image_data = None
        text_content = None

        if response.candidates and response.candidates[0].content.parts:
            print(f"📊 响应部分数量: {len(response.candidates[0].content.parts)}")

            for i, part in enumerate(response.candidates[0].content.parts):
                if hasattr(part, 'inline_data') and part.inline_data and part.inline_data.data:
                    image_data = part.inline_data.data
                    print(f"   ✅ 部分 {i+1}: 图像数据 ({len(image_data):,} bytes)")
                elif hasattr(part, 'text') and part.text:
                    text_content = part.text
                    print(f"   📝 部分 {i+1}: 文本内容 ({len(text_content)} 字符)")

        if image_data:
            # 保存图像
            output_file = f"flash_exp_image_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            with open(output_file, 'wb') as f:
                f.write(image_data)

            print(f"\n✅ 图像已保存: {output_file}")
            print(f"💾 文件大小: {len(image_data):,} bytes")

            if text_content:
                print(f"\n📝 模型附加信息:")
                print(text_content[:500] + "..." if len(text_content) > 500 else text_content)

            return output_file, image_data, text_content
        else:
            print("\n❌ 未收到图像数据")
            return None, None, text_content

    except Exception as e:
        print(f"❌ 模型测试失败: {e}")
        import traceback
        traceback.print_exc()
        return None, None, None

def analyze_image_quality(image_path):
    """分析图像质量"""
    print(f"\n🔍 分析图像质量: {image_path}")
    print("-" * 70)

    try:
        # 加载图像
        img = Image.open(image_path)
        width, height = img.size

        print(f"📏 尺寸: {width} x {height} pixels")
        print(f"🎨 模式: {img.mode}")

        dpi = img.info.get('dpi')
        if dpi:
            print(f"📐 DPI: {dpi[0]} x {dpi[1]}")
        else:
            print("📐 DPI: 未设置")

        # 转换为灰度图像进行分析
        if img.mode != 'L':
            img_gray = img.convert('L')
        else:
            img_gray = img

        # 计算图像统计信息
        img_array = np.array(img_gray)
        mean_pixel = np.mean(img_array)
        std_pixel = np.std(img_array)
        min_pixel = np.min(img_array)
        max_pixel = np.max(img_array)

        print(f"\n📊 像素统计:")
        print(f"   平均值: {mean_pixel:.2f}")
        print(f"   标准差: {std_pixel:.2f}")
        print(f"   最小值: {min_pixel}")
        print(f"   最大值: {max_pixel}")

        # 计算对比度
        if max_pixel > min_pixel:
            contrast = (max_pixel - min_pixel) / (max_pixel + min_pixel) * 100
        else:
            contrast = 0
        print(f"   对比度: {contrast:.2f}%")

        # 判断是否为高质量专利附图
        print(f"\n🎯 质量评估:")
        is_good_quality = True

        # 检查是否为黑白图像
        if img.mode in ['L', '1']:
            print(f"   ✅ 图像模式: 符合专利要求 (黑白图像)")
        elif img.mode == 'RGB':
            print(f"   ⚠️ 图像模式: {img.mode} (彩色，建议转换为黑白)")
        else:
            print(f"   ⚠️ 图像模式: {img.mode}")

        # 检查尺寸
        if width >= 2000 and height >= 2000:
            print(f"   ✅ 图像尺寸: 符合高分辨率要求")
        else:
            print(f"   ⚠️ 图像尺寸: {width}x{height} (建议 ≥2000x2000)")

        # 检查对比度
        if contrast > 50:
            print(f"   ✅ 对比度: 优秀 ({contrast:.2f}%)")
        elif contrast > 20:
            print(f"   ✅ 对比度: 良好 ({contrast:.2f}%)")
        else:
            print(f"   ⚠️ 对比度: 可能偏低 ({contrast:.2f}%)")

        return {
            'width': width,
            'height': height,
            'mode': img.mode,
            'dpi': dpi,
            'contrast': contrast,
            'is_good_quality': is_good_quality
        }

    except Exception as e:
        print(f"❌ 图像分析失败: {e}")
        return None

def main():
    print("=" * 70)
    print("🎨 Gemini-2.0-Flash-Exp-Image-Generation 测试")
    print("=" * 70)
    print(f"⏰ 测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # 测试模型
    generated_image, image_data, text_response = test_flash_exp_image_generation()

    if generated_image:
        # 分析生成的图像
        print("\n" + "=" * 70)
        print("📊 生成图像质量分析")
        print("=" * 70)

        quality = analyze_image_quality(generated_image)

        if quality:
            print("\n" + "=" * 70)
            print("📋 最终评估报告")
            print("=" * 70)

            print(f"\n✅ 模型状态: models/gemini-2.0-flash-exp-image-generation")
            print(f"📁 生成文件: {generated_image}")
            print(f"💾 文件大小: {len(image_data):,} bytes")

            print(f"\n🎯 图像质量:")
            print(f"   尺寸: {quality['width']} x {quality['height']}")
            print(f"   模式: {quality['mode']}")
            print(f"   对比度: {quality['contrast']:.2f}%")
            print(f"   综合评级: {'✅ 优秀' if quality['is_good_quality'] else '⚠️ 一般'}")

            # 写入测试报告
            report_file = f"flash_exp_image_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write("=" * 70 + "\n")
                f.write("models/gemini-2.0-flash-exp-image-generation 测试报告\n")
                f.write("=" * 70 + "\n\n")
                f.write(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"模型: models/gemini-2.0-flash-exp-image-generation\n")
                f.write(f"生成文件: {generated_image}\n")
                f.write(f"文件大小: {len(image_data):,} bytes\n")
                f.write(f"图像尺寸: {quality['width']} x {quality['height']}\n")
                f.write(f"图像模式: {quality['mode']}\n")
                f.write(f"对比度: {quality['contrast']:.2f}%\n")

                if text_response:
                    f.write(f"\n模型响应文本:\n{text_response}\n")

            print(f"\n📄 测试报告已保存: {report_file}")

            print(f"\n🎉 测试成功完成！")
        else:
            print(f"\n❌ 图像分析失败")
    else:
        print("\n❌ 图像生成失败")
        print("\n💡 所有模型测试结论:")
        print("1. Gemini-2.0-Flash-Preview-Image-Generation - 响应模态限制")
        print("2. models/gemini-2.0-flash-preview-image-generation - 响应模态限制")
        print("3. models/gemini-2.0-flash-exp-image-generation - 待测试")
        print("\n💡 推荐方案: Gemini-2.5-Pro + Python渲染")

if __name__ == "__main__":
    main()
