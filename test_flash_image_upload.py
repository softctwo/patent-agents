#!/usr/bin/env python3
"""
尝试上传图像并生成新图像的测试
"""

import os
import google.generativeai as genai
from datetime import datetime

# 设置API密钥
API_KEY = "AIzaSyAPnIWfYq8oGS7yAmNXdP0k8NuPB_gu5VU"
os.environ['GOOGLE_API_KEY'] = API_KEY
genai.configure(api_key=API_KEY)

def list_available_models():
    """列出可用的模型"""
    print("\n" + "=" * 70)
    print("📋 可用模型列表")
    print("=" * 70)

    try:
        models = genai.list_models()
        image_models = []
        for model in models:
            if 'image' in model.name.lower():
                image_models.append(model)

        print(f"\n📦 找到 {len(image_models)} 个图像相关模型:")
        for model in image_models:
            print(f"   - {model.name}")
            print(f"     生成方法: {model.supported_generation_methods}")
            print()

    except Exception as e:
        print(f"❌ 获取模型列表失败: {e}")

def test_with_file_upload():
    """测试通过文件上传方式使用模型"""
    print("\n" + "=" * 70)
    print("📤 测试文件上传方式")
    print("=" * 70)

    # 查找一个示例图像
    sample_images = [
        'openai-agents-python/examples/patent_agent/gemini_intelligent_20251030_032052.png',
        'test_flash_image_correct_20251030_040525.png',
        'flash_image_correct_20251030_040525.png'
    ]

    sample_image = None
    for img_path in sample_images:
        if os.path.exists(img_path):
            sample_image = img_path
            break

    if not sample_image:
        print("❌ 未找到示例图像，跳过上传测试")
        return False

    print(f"📁 使用示例图像: {sample_image}")

    try:
        # 上传图像
        uploaded_file = genai.upload_file(
            path=sample_image,
            display_name=f"sample_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        )
        print(f"✅ 文件上传成功: {uploaded_file.name}")
        print(f"   URI: {uploaded_file.uri}")

        # 尝试使用图像生成模型
        model_name = 'gemini-2.0-flash-preview-image-generation'
        model = genai.GenerativeModel(model_name)

        prompt = "Generate a new patent drawing based on this device"

        print("\n🧠 使用上传的图像生成新图像...")
        response = model.generate_content([uploaded_file, prompt])

        print("✅ 生成请求完成")
        print(f"响应类型: {type(response)}")

        # 检查响应
        image_count = 0
        if response.candidates and response.candidates[0].content.parts:
            for i, part in enumerate(response.candidates[0].content.parts):
                if hasattr(part, 'inline_data') and part.inline_data and part.inline_data.data:
                    image_count += 1
                    print(f"   收到图像数据: {len(part.inline_data.data):,} bytes")

        if image_count > 0:
            print("\n✅ 成功生成新图像！")
            return True
        else:
            print("\n❌ 未收到图像")
            return False

    except Exception as e:
        print(f"❌ 文件上传测试失败: {e}")
        return False

def main():
    print("=" * 70)
    print("🎨 Gemini-2.0-Flash-Preview-Image-Generation 深度测试")
    print("=" * 70)

    # 列出可用模型
    list_available_models()

    # 测试文件上传
    test_with_file_upload()

    print("\n" + "=" * 70)
    print("💡 最终建议")
    print("=" * 70)
    print("\n1. 🔍 Gemini-2.0-Flash-Preview-Image-Generation 模型存在响应模态限制")
    print("2. ⚠️ 该模型可能需要特殊的使用方式")
    print("3. ✅ 推荐方案: Gemini-2.5-Pro + Python渲染")
    print("4. 📐 优势:")
    print("   - 完全可控的图像质量")
    print("   - 符合专利标准")
    print("   - 智能布局算法")

if __name__ == "__main__":
    main()
