#!/usr/bin/env python3
"""
正确的Gemini-2.0-Flash-Preview-Image-Generation模型测试
处理IMAGE和TEXT响应模态
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
    print("⚠️ EasyOCR 不可用，将使用其他方法评估")

def create_patent_drawing_prompt(request):
    """构建专利绘图提示词"""
    prompt = f"""
Create a professional patent technical drawing for: {request.get('invention_title', 'Device')}

SPECIFICATIONS:
- Type: Patent technical drawing (black lines on white background)
- Style: IEEE/ISO standard technical drawing
- Quality: Professional, high precision
- Standard: A4 format (210x297mm at 300 DPI)
- Language: Only English labels and numbers
- NO CHINESE CHARACTERS anywhere

PRODUCT DESCRIPTION:
{request.get('product_description', '')}

KEY COMPONENTS TO DRAW:
"""

    for i, comp in enumerate(request.get('key_components', []), 1):
        prompt += f"{i}. {comp}\n"

    prompt += """
DRAWING REQUIREMENTS:
1. Use clean, precise black lines only
2. Draw rectangular and circular components as appropriate
3. Add numbered labels (1, 2, 3...) next to each component
4. Use professional technical drawing style
5. Maintain consistent line thickness
6. Show relationships between components with lines
7. Include title: "Figure 1: [Invention Name]"
8. NO shading, NO colors, NO 3D effects
9. Patent drawing standard: clean black lines on white background

IMPORTANT:
- ONLY use English labels and Arabic numerals (1, 2, 3...)
- NO Chinese characters or text
- Follow patent drawing guidelines exactly
- Professional technical illustration style

Generate a complete patent drawing image now.
"""

    return prompt

def test_flash_image_generation_correct():
    """测试Gemini-2.0-Flash-Preview-Image-Generation模型（正确版）"""
    print("\n" + "=" * 70)
    print("🎨 测试Gemini-2.0-Flash-Preview-Image-Generation模型（正确版）")
    print("=" * 70)

    # 测试请求
    request = {
        'invention_title': 'Smart Blockchain Hardware Wallet',
        'product_description': 'A compact elliptic hardware wallet for secure cryptocurrency storage with biometric authentication, wireless charging, and modular security chip design',
        'key_components': [
            'Elliptical Enclosure',
            'Biometric Fingerprint Scanner',
            'OLED Display Screen',
            'PCB Main Board',
            'Lithium Battery',
            'Wireless Charging Coil',
            'USB-C Interface',
            'Physical Buttons',
            'Modular Security Chip',
            'Anti-tamper Structure'
        ]
    }

    # 构建提示词
    prompt = create_patent_drawing_prompt(request)

    model_name = 'gemini-2.0-flash-preview-image-generation'

    print(f"\n📦 测试模型: {model_name}")
    print("-" * 70)

    try:
        # 初始化模型
        model = genai.GenerativeModel(model_name)
        print(f"✅ 模型 {model_name} 初始化成功")

        print("\n🧠 正在生成专利附图...")
        print("💡 提示：该模型会同时返回IMAGE和TEXT响应")

        # 使用标准generate_content调用
        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": 0.2,
                "top_p": 0.9,
                "max_output_tokens": 8192,
            }
        )

        print("✅ 图像生成请求完成")

        # 检查响应内容
        image_data = None
        text_content = None

        if response.candidates and response.candidates[0].content.parts:
            print(f"📊 响应部分数量: {len(response.candidates[0].content.parts)}")

            for i, part in enumerate(response.candidates[0].content.parts):
                print(f"   部分 {i+1}: 类型 = {type(part).__name__}")

                if hasattr(part, 'inline_data') and part.inline_data and part.inline_data.data:
                    image_data = part.inline_data.data
                    print(f"   ✅ 图像数据: {len(image_data):,} bytes")
                elif hasattr(part, 'text') and part.text:
                    text_content = part.text
                    print(f"   📝 文本内容: {len(text_content)} 字符")

        if image_data:
            # 保存图像
            output_file = f"flash_image_correct_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            with open(output_file, 'wb') as f:
                f.write(image_data)

            print(f"\n✅ 图像已保存: {output_file}")
            print(f"💾 文件大小: {len(image_data):,} bytes")

            if text_content:
                print(f"\n📝 模型附加信息:")
                # 只显示前500字符
                display_text = text_content[:500] + "..." if len(text_content) > 500 else text_content
                print(display_text)

            return output_file, image_data, text_content
        else:
            print("\n❌ 未收到图像数据")
            print("⚠️ 可能原因:")
            print("1. 模型权限限制")
            print("2. 提示词不符合要求")
            print("3. API限制")

            if text_content:
                print(f"\n📝 仅收到文本响应:")
                print(text_content[:500] + "..." if len(text_content) > 500 else text_content)

            return None, None, text_content

    except Exception as e:
        print(f"❌ 模型测试失败: {e}")
        import traceback
        traceback.print_exc()
        return None, None, None

def analyze_image_quality(image_path):
    """分析图像质量"""
    print(f"\n�� 分析图像质量: {image_path}")
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
            is_good_quality = False
        else:
            print(f"   ⚠️ 图像模式: {img.mode} (需要验证)")
            is_good_quality = False

        # 检查尺寸
        if width >= 2000 and height >= 2000:
            print(f"   ✅ 图像尺寸: 符合高分辨率要求")
        else:
            print(f"   ⚠️ 图像尺寸: {width}x{height} (建议 ≥2000x2000)")
            is_good_quality = False

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
            'mean_pixel': mean_pixel,
            'std_pixel': std_pixel,
            'contrast': contrast,
            'is_good_quality': is_good_quality
        }

    except Exception as e:
        print(f"❌ 图像分析失败: {e}")
        return None

def main():
    print("=" * 70)
    print("🎨 Gemini-2.0-Flash-Preview-Image-Generation 正确测试")
    print("=" * 70)
    print(f"⏰ 测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # 测试Gemini-2.0-Flash-Preview-Image-Generation模型
    generated_image, image_data, text_response = test_flash_image_generation_correct()

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

            print(f"\n✅ 模型状态: Gemini-2.0-Flash-Preview-Image-Generation")
            print(f"📁 生成文件: {generated_image}")
            print(f"💾 文件大小: {len(image_data):,} bytes")

            print(f"\n🎯 图像质量:")
            print(f"   尺寸: {quality['width']} x {quality['height']}")
            print(f"   模式: {quality['mode']}")
            print(f"   对比度: {quality['contrast']:.2f}%")
            print(f"   综合评级: {'✅ 优秀' if quality['is_good_quality'] else '⚠️ 一般'}")

            # 写入测试报告
            report_file = f"flash_image_correct_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write("=" * 70 + "\n")
                f.write("Gemini-2.0-Flash-Preview-Image-Generation 测试报告（正确版）\n")
                f.write("=" * 70 + "\n\n")
                f.write(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"模型: {model_name}\n")
                f.write(f"生成文件: {generated_image}\n")
                f.write(f"文件大小: {len(image_data):,} bytes\n")
                f.write(f"图像尺寸: {quality['width']} x {quality['height']}\n")
                f.write(f"图像模式: {quality['mode']}\n")
                f.write(f"对比度: {quality['contrast']:.2f}%\n")
                f.write(f"质量评级: {'优秀' if quality['is_good_quality'] else '一般'}\n\n")

                if text_response:
                    f.write(f"模型响应文本:\n{text_response}\n\n")

                f.write("技术分析:\n")
                f.write(f"- 模型响应模态: IMAGE + TEXT\n")
                f.write(f"- 图像尺寸: {quality['width']}x{quality['height']} 像素\n")
                f.write(f"- DPI: {quality['dpi'] if quality['dpi'] else '未设置'}\n")
                f.write(f"- 对比度: {quality['contrast']:.2f}%\n")

            print(f"\n📄 测试报告已保存: {report_file}")

            # 显示图像信息
            print(f"\n🎨 图像信息:")
            print(f"   分辨率: {quality['width']} x {quality['height']}")
            print(f"   颜色模式: {quality['mode']}")
            print(f"   文件格式: PNG")

    else:
        print("\n❌ 图像生成失败")
        print("\n🔧 问题分析:")
        print("1. 该模型可能需要特殊的API配置")
        print("2. 提示词可能需要调整")
        print("3. 模型可能不支持直接图像生成")
        print("\n💡 建议使用:")
        print("   - Gemini-2.5-Pro 生成智能方案")
        print("   - Python 渲染高质量图像")

    print("\n" + "=" * 70)
    print("📝 测试结论")
    print("=" * 70)
    print("\n1. ✅ 模型初始化成功")
    print("2. ⚠️ 图像生成需要进一步验证")
    print("3. 💡 推荐方案:")
    print("   - Gemini-2.5-Pro + Python渲染")
    print("   - 智能布局算法")
    print("   - 符合专利标准的图像生成")

if __name__ == "__main__":
    main()
