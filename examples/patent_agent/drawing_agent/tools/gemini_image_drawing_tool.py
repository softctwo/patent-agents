"""
基于Gemini-2.5-Pro的智能专利附图生成工具
使用文本模型生成详细的绘图方案，然后用代码渲染
"""

import os
import math
import json
from typing import List, Dict, Tuple, Optional
from PIL import Image, ImageDraw, ImageFont
import google.generativeai as genai
from dotenv import load_dotenv

# 加载.env文件中的环境变量
load_dotenv()


class GeminiIntelligentDrawingTool:
    """基于Gemini-2.5-Pro的智能专利附图生成工具"""

    DEFAULT_DPI = 300
    MARGIN = 80

    def __init__(self):
        """初始化绘制工具"""
        self.gemini_model = None
        self._init_model()

    def _init_model(self):
        """初始化Gemini模型"""
        try:
            api_key = os.getenv("GOOGLE_API_KEY")
            if api_key and api_key != "your_gemini_api_key_here":
                genai.configure(api_key=api_key)
                self.gemini_model = genai.GenerativeModel('gemini-2.5-pro')
                print("✅ Gemini-2.5-Pro模型初始化成功")
            else:
                print("⚠️ 未设置有效的GOOGLE_API_KEY")
        except Exception as e:
            print(f"❌ 模型初始化失败: {e}")
            self.gemini_model = None

    def create_intelligent_drawing(
        self,
        request,
        output_path: Optional[str] = None
    ) -> str:
        """
        使用Gemini生成智能绘图方案，然后渲染为图像

        Args:
            request: 绘图请求
            output_path: 输出路径（可选）

        Returns:
            附图的文件路径
        """
        try:
            if not self.gemini_model:
                print("❌ Gemini模型未初始化")
                return None

            print("\n" + "=" * 70)
            print("🧠 Gemini-2.5-Pro 智能专利附图生成")
            print("=" * 70)

            # 第一步：生成详细绘图方案
            print("🧠 步骤1: Gemini生成智能绘图方案...")
            
            plan_prompt = f"""
Generate a detailed patent drawing plan for: {request.get('invention_title', 'Device')}

Requirements:
1. Provide exact positions for each component (as percentages of drawing area: 0.0 to 1.0)
2. Provide component sizes (width/height as percentages: 0.0 to 1.0)
3. Specify component types: "rectangle" or "circle"
4. List connections between components with numbered IDs
5. All labels must be in English only

Product Description:
{request.get('product_description', '')}

Components: {', '.join(request.get('key_components', []))}

Structure Details:
{request.get('structure_details', '')}

Output in this EXACT JSON format:
{{
    "title": "Figure 1: [Invention Name]",
    "components": [
        {{
            "id": 1,
            "name": "Component Name",
            "x": 0.2,
            "y": 0.3,
            "width": 0.15,
            "height": 0.1,
            "type": "rectangle"
        }}
    ],
    "connections": [
        {{"from": 1, "to": 2}}
    ],
    "notes": "Additional technical notes"
}}

IMPORTANT:
- ONLY use English labels and Arabic numerals (1, 2, 3...)
- NO Chinese characters
- Provide precise coordinates and sizes
- Keep responses concise and technical
"""
            
            plan_response = self.gemini_model.generate_content(plan_prompt)
            plan_text = plan_response.text
            
            print("✅ 绘图方案生成完成")
            print(f"📝 方案内容:\n{plan_text[:200]}...")
            print()
            
            # 第二步：解析JSON并渲染
            print("🎨 步骤2: 渲染智能绘图...")
            
            # 解析JSON
            import re
            json_match = re.search(r'\{.*\}', plan_text, re.DOTALL)
            if json_match:
                plan_json = json.loads(json_match.group())
                output_file = self._render_drawing_from_plan(plan_json, request, output_path)
                return output_file
            else:
                print("❌ 无法解析绘图方案")
                return None

        except Exception as e:
            print(f"❌ 生成过程中发生错误: {e}")
            import traceback
            traceback.print_exc()
            return None

    def _render_drawing_from_plan(
        self,
        plan: dict,
        request: dict,
        output_path: Optional[str] = None
    ) -> str:
        """从Gemini生成的方案渲染绘图"""
        
        # 设置输出文件
        if not output_path:
            output_path = f"gemini_intelligent_{request.get('request_id', 'drawing')}.png"
        
        # 创建图像
        width_px = 2480  # A4 300DPI
        height_px = 3507  # A4 300DPI
        image = Image.new('RGB', (width_px, height_px), 'white')
        draw = ImageDraw.Draw(image)
        
        # 添加标题
        title = plan.get('title', f"Figure 1: {request.get('invention_title', 'Device')}")
        try:
            # 尝试加载字体
            font = ImageFont.truetype("arial.ttf", 60)
        except:
            font = ImageFont.load_default()
        
        # 绘制标题
        title_y = 50
        draw.text((width_px // 2, title_y), title, fill='black', font=font, anchor='mt')
        
        # 绘制边框
        margin = 80
        border_margin = 100
        draw.rectangle(
            [border_margin, title_y + 50, width_px - border_margin, height_px - margin],
            outline='black',
            width=2
        )
        
        # 绘制组件
        for comp in plan.get('components', []):
            x = int(comp.get('x', 0.5) * width_px)
            y = int(comp.get('y', 0.5) * height_px)
            w = int(comp.get('width', 0.1) * width_px)
            h = int(comp.get('height', 0.1) * height_px)
            comp_type = comp.get('type', 'rectangle')
            
            if comp_type == 'circle':
                r = min(w, h) // 2
                bbox = [x - r, y - r, x + r, y + r]
                draw.ellipse(bbox, outline='black', width=2)
            else:
                draw.rectangle(
                    [x - w//2, y - h//2, x + w//2, y + h//2],
                    outline='black',
                    width=2
                )
            
            # 添加组件标签
            label_id = comp.get('id', 0)
            try:
                label_font = ImageFont.truetype("arial.ttf", 40)
            except:
                label_font = ImageFont.load_default()
            
            # 标签位置（组件右上角）
            label_x = x + w//2 + 20
            label_y = y - h//2 - 10
            draw.text((label_x, label_y), str(label_id), fill='black', font=label_font)
        
        # 绘制连接线
        for conn in plan.get('connections', []):
            from_id = conn.get('from')
            to_id = conn.get('to')
            
            # 找到组件位置
            from_comp = next((c for c in plan.get('components', []) if c.get('id') == from_id), None)
            to_comp = next((c for c in plan.get('components', []) if c.get('id') == to_id), None)
            
            if from_comp and to_comp:
                from_x = int(from_comp.get('x', 0.5) * width_px)
                from_y = int(from_comp.get('y', 0.5) * height_px)
                to_x = int(to_comp.get('x', 0.5) * width_px)
                to_y = int(to_comp.get('y', 0.5) * height_px)
                
                draw.line([(from_x, from_y), (to_x, to_y)], fill='black', width=1)
        
        # 保存图像
        image.save(output_path, 'PNG', dpi=(300, 300))
        
        print(f"✅ 智能附图生成成功")
        print(f"📁 保存路径: {output_path}")
        print(f"📊 文件大小: {os.path.getsize(output_path):,} bytes")
        
        return output_path


# 便捷函数
def create_gemini_intelligent_drawing(request, output_path="gemini_intelligent_drawing.png"):
    """创建Gemini智能绘图的便捷函数"""
    tool = GeminiIntelligentDrawingTool()
    return tool.create_intelligent_drawing(request, output_path)

