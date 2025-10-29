"""
Gemini-2.5-Flash-Image驱动的专利附图绘制工具
使用Google Gemini-2.5-Flash-Image模型生成专业专利附图
"""

import os
import math
import json
from typing import List, Dict, Tuple, Optional
from PIL import Image, ImageDraw, ImageFont
import io
import asyncio
import google.generativeai as genai
from dotenv import load_dotenv

# 加载.env文件中的环境变量
load_dotenv()


class GeminiFlashImagePatentDrawingTool:
    """基于Gemini-2.5-Flash-Image的专利附图绘制工具"""

    # 默认参数
    DEFAULT_DPI = 300
    MARGIN = 80

    def __init__(self):
        """初始化绘制工具"""
        self.imagen_model = None
        self.gemini_model = None
        
        # 初始化模型
        self._init_models()

    def _init_models(self):
        """初始化Google AI模型"""
        try:
            api_key = os.getenv("GOOGLE_API_KEY")
            if api_key and api_key != "your_gemini_api_key_here":
                genai.configure(api_key=api_key)

                # 使用Gemini-2.5-Flash-Image模型进行图像生成
                self.imagen_model = genai.GenerativeModel('gemini-2.5-flash-preview-image')
                print("✅ Gemini-2.5-Flash-Image模型初始化成功")

                # 初始化Gemini模型（用于生成绘图方案）
                self.gemini_model = genai.GenerativeModel('gemini-2.5-pro')
                print("✅ Gemini-2.5-Pro模型初始化成功")
            else:
                print("⚠️ 未设置有效的GOOGLE_API_KEY")
                print("   请在.env文件中配置您的Gemini API密钥")
        except Exception as e:
            print(f"❌ 模型初始化失败: {e}")
            self.imagen_model = None
            self.gemini_model = None

    def create_drawing_with_flash_image(
        self,
        request,
        output_path: Optional[str] = None
    ) -> str:
        """
        使用Gemini-2.5-Flash-Image生成专利附图

        Args:
            request: 绘图请求
            output_path: 输出路径（可选）

        Returns:
            附图的Base64编码字符串或文件路径
        """
        try:
            if not self.imagen_model:
                print("❌ Gemini-2.5-Flash-Image模型未初始化")
                return None

            print("\n" + "=" * 70)
            print("🎨 Gemini-2.5-Flash-Image专利附图生成")
            print("=" * 70)

            # 构建绘图提示词
            prompt = self._build_flash_image_prompt(request)
            
            print(f"📝 生成提示词:")
            print(f"   {prompt[:100]}...")
            print()
            
            # 使用Gemini-2.5-Flash-Image生成图像
            print("🎨 正在使用Gemini-2.5-Flash-Image生成专利附图...")
            response = self.imagen_model.generate_content(
                prompt,
                generation_config={
                    "temperature": 0.1,  # 降低随机性，确保一致性
                    "top_p": 0.8,
                    "max_output_tokens": 2048,
                }
            )
            
            # 提取生成的图像
            if response.candidates and response.candidates[0].content.parts:
                image_data = response.candidates[0].content.parts[0].inline_data.data
                
                # 保存图像
                if output_path:
                    with open(output_path, 'wb') as f:
                        f.write(image_data)
                    print(f"✅ 附图生成成功")
                    print(f"📁 保存路径: {output_path}")
                    return output_path
                else:
                    return image_data
            else:
                print("❌ 图像生成失败：未返回有效数据")
                return None

        except Exception as e:
            print(f"❌ 生成过程中发生错误: {e}")
            import traceback
            traceback.print_exc()
            return None

    def _build_flash_image_prompt(self, request) -> str:
        """构建Gemini-2.5-Flash-Image的绘图提示词"""
        
        prompt = f"""
Create a professional patent drawing for: {request.get('invention_title', 'Device')}

Specifications:
- Type: Patent technical drawing (black lines on white background)
- Style: IEEE/ISO standard technical drawing
- Quality: Professional, high precision
- Standard: A4 format (210x297mm at 300 DPI)
- Language: Only English labels and numbers
- NO CHINESE CHARACTERS anywhere

Product Description:
{request.get('product_description', '')}

Key Components to Draw:
"""
        
        for i, comp in enumerate(request.get('key_components', []), 1):
            prompt += f"{i}. {comp}\n"
        
        prompt += """
Drawing Requirements:
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
"""
        
        return prompt

    def create_enhanced_drawing(
        self,
        request,
        output_path: Optional[str] = None
    ) -> str:
        """
        使用Gemini生成绘图方案，然后用Imagen-4.0生成图像

        Args:
            request: 绘图请求
            output_path: 输出路径（可选）

        Returns:
            附图的文件路径
        """
        try:
            if not self.gemini_model or not self.imagen_model:
                print("❌ 模型未初始化")
                return None

            print("\n" + "=" * 70)
            print("🎨 Gemini + Gemini-2.5-Flash-Image 增强绘图")
            print("=" * 70)

            # 第一步：使用Gemini生成绘图方案
            print("🧠 步骤1: Gemini生成智能绘图方案...")
            
            plan_prompt = f"""
Generate a detailed patent drawing plan for: {request.get('invention_title', 'Device')}

Provide:
1. Component layout (positions as percentages of drawing area)
2. Component sizes (width/height as percentages)
3. Connection relationships between components
4. Professional English labels for each component

Product: {request.get('product_description', '')}
Components: {', '.join(request.get('key_components', []))}

Output in JSON format:
{{
    "title": "Figure 1: [Name]",
    "components": [
        {{"id": 1, "name": "Component Name", "x": 0.2, "y": 0.3, "width": 0.15, "height": 0.1, "type": "rectangle/circle"}}
    ],
    "connections": [
        {{"from": 1, "to": 2}}
    ]
}}

IMPORTANT: Only English labels, NO Chinese characters.
"""
            
            plan_response = self.gemini_model.generate_content(plan_prompt)
            plan_text = plan_response.text
            
            print(f"✅ 绘图方案生成完成")

            # 第二步：使用Gemini-2.5-Flash-Image生成图像
            print("🎨 步骤2: Gemini-2.5-Flash-Image生成专业附图...")
            
            imagen_prompt = f"""
Create a patent technical drawing based on this plan:

{plan_text}

Requirements:
- Professional patent drawing style
- Black lines on white background only
- Clean, precise technical illustration
- IEEE/ISO standard
- A4 format at 300 DPI
- English labels only (1, 2, 3...)
- NO Chinese characters
- Number each component clearly
- Show connections between components
- Title at top: "Figure 1: [Invention Name]"

Style: Technical patent drawing, black lines, white background, professional
"""
            
            response = self.imagen_model.generate_content(
                imagen_prompt,
                generation_config={
                    "temperature": 0.2,
                    "top_p": 0.8,
                    "max_output_tokens": 4096,
                }
            )
            
            # 提取生成的图像
            if response.candidates and response.candidates[0].content.parts:
                image_data = response.candidates[0].content.parts[0].inline_data.data
                
                # 保存图像
                if output_path:
                    with open(output_path, 'wb') as f:
                        f.write(image_data)
                    
                    print(f"✅ 增强附图生成成功")
                    print(f"📁 保存路径: {output_path}")
                    print(f"📊 文件大小: {len(image_data):,} bytes")
                    return output_path
                else:
                    return image_data
            else:
                print("❌ 图像生成失败")
                return None

        except Exception as e:
            print(f"❌ 增强绘图过程中发生错误: {e}")
            import traceback
            traceback.print_exc()
            return None


# 简单封装，方便使用
def create_flash_image_drawing(request, output_path="flash_image_drawing.png"):
    """创建Gemini-2.5-Flash-Image绘图的便捷函数"""
    tool = GeminiFlashImagePatentDrawingTool()
    return tool.create_enhanced_drawing(request, output_path)

