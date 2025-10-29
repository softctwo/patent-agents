"""
AI驱动的专利附图绘制工具
集成Gemini大模型生成专业专利附图
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

try:
    # 尝试相对导入
    from ..schemas.drawing_schemas import (
        PatentDrawing,
        DrawingRequest,
        DrawingType,
        DrawingStyle,
        LineStyle,
        PATENT_DRAWING_STANDARDS
    )
except ImportError:
    # 如果相对导入失败，使用绝对导入
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
    from schemas.drawing_schemas import (
        PatentDrawing,
        DrawingRequest,
        DrawingType,
        DrawingStyle,
        LineStyle,
        PATENT_DRAWING_STANDARDS
    )


class AIPatentDrawingTool:
    """AI驱动的专利附图绘制工具"""

    # 符合专利审查指南的默认参数
    DEFAULT_LINE_WIDTH = 0.5
    DEFAULT_DPI = 300
    MARGIN = 80

    def __init__(self):
        """初始化绘制工具"""
        self.standards = PATENT_DRAWING_STANDARDS
        self.current_drawing = None
        self.gemini_model = None

        # 初始化Gemini模型
        self._init_gemini()

    def _init_gemini(self):
        """初始化Gemini大模型"""
        try:
            api_key = os.getenv("GOOGLE_API_KEY")
            if api_key and api_key != "your_gemini_api_key_here":
                genai.configure(api_key=api_key)
                self.gemini_model = genai.GenerativeModel('gemini-2.5-pro')
                print("✅ Gemini-2.5-Pro AI模型初始化成功（从.env文件加载）")
            else:
                print("⚠️ 未设置有效的GOOGLE_API_KEY，将使用基础绘图功能")
                print("   请在.env文件中配置您的Gemini API密钥")
        except Exception as e:
            print(f"❌ Gemini模型初始化失败: {e}")
            self.gemini_model = None

    def create_drawing(
        self,
        request: DrawingRequest,
        output_path: Optional[str] = None
    ) -> str:
        """
        使用AI生成专利附图

        Args:
            request: 绘图请求
            output_path: 输出路径（可选）

        Returns:
            附图的Base64编码字符串或文件路径
        """
        try:
            # 使用AI生成绘图方案
            drawing_plan = self._generate_drawing_plan(request)

            # 创建附图对象
            drawing = PatentDrawing(
                drawing_id=request.request_id,
                title=f"Figure {request.request_id[-1] if request.request_id else '1'}: {request.invention_title}",
                drawing_type=request.drawing_type,
                style=request.drawing_style
            )

            # 解析AI生成的绘图方案
            self._apply_ai_plan(drawing, request, drawing_plan)

            # 渲染图像
            image_data = self._render_drawing(drawing)

            # 保存或返回
            if output_path:
                with open(output_path, 'wb') as f:
                    f.write(image_data)
                return output_path
            else:
                return self._encode_base64(image_data)

        except Exception as e:
            # 如果AI生成失败，回退到基础绘图
            print(f"⚠️ AI绘图失败，使用基础绘图: {e}")
            return self._fallback_drawing(request, output_path)

    def _generate_drawing_plan(self, request: DrawingRequest) -> Dict:
        """使用Gemini AI生成绘图方案"""
        if not self.gemini_model:
            return None

        try:
            # 构建提示词
            prompt = self._build_drawing_prompt(request)

            # 调用Gemini
            response = self.gemini_model.generate_content(prompt)

            # 解析响应
            plan_text = response.text

            # 尝试解析JSON格式的响应
            try:
                # 查找JSON块
                json_start = plan_text.find('{')
                json_end = plan_text.rfind('}') + 1
                if json_start >= 0 and json_end > json_start:
                    json_str = plan_text[json_start:json_end]
                    plan = json.loads(json_str)
                    print("✅ AI绘图方案生成成功")
                    return plan
                else:
                    # 如果没有JSON，返回基础方案
                    return self._parse_ai_text_response(plan_text)
            except json.JSONDecodeError:
                # 如果解析JSON失败，尝试解析文本
                return self._parse_ai_text_response(plan_text)

        except Exception as e:
            print(f"❌ AI生成绘图方案失败: {e}")
            return None

    def _build_drawing_prompt(self, request: DrawingRequest) -> str:
        """构建绘图提示词"""
        drawing_type_map = {
            DrawingType.MECHANICAL: "mechanical structure diagram",
            DrawingType.CIRCUIT: "electrical circuit diagram",
            DrawingType.FLOWCHART: "process flowchart",
            DrawingType.SCHEMATIC: "schematic diagram",
            DrawingType.STRUCTURE: "construction diagram",
            DrawingType.ASSEMBLY: "assembly diagram"
        }

        drawing_type = drawing_type_map.get(request.drawing_type, "schematic diagram")

        prompt = f"""Generate a professional patent drawing plan for a {drawing_type}.

Requirements:
- Patent examination guideline compliant
- Professional technical drawing style
- Black lines on white background, no colors
- Clear component markers (Arabic numerals only, NO CHINESE)
- 300 DPI resolution
- IEEE/ISO technical drawing standards

Invention Details:
- Title: {request.invention_title}
- Type: {request.drawing_type}
- Description: {request.product_description}
- Components: {', '.join(request.key_components) if request.key_components else 'Not specified'}
- Structure: {request.structure_details if request.structure_details else 'Not specified'}

Please provide a detailed drawing plan in JSON format with the following structure:
{{
    "title": "Figure 1: [English Title]",
    "components": [
        {{
            "id": "1",
            "name": "Component Name (English only)",
            "type": "rectangle|circle|ellipse|polygon",
            "position": {{"x": 0.3, "y": 0.4, "unit": "relative"}},
            "size": {{"width": 0.15, "height": 0.1, "unit": "relative"}},
            "description": "Brief description (English)"
        }}
    ],
    "connections": [
        {{
            "from": "1",
            "to": "2",
            "type": "line|arrow"
        }}
    ],
    "layout": {{
        "style": "grid|circular|hierarchical",
        "orientation": "portrait|landscape"
    }}
}}

IMPORTANT:
- All text must be in English ONLY
- Component names must be in English
- Use Arabic numerals (1, 2, 3...) for markers
- NO CHINESE CHARACTERS anywhere
- Professional technical terminology
- Focus on clarity and precision"""

        return prompt

    def _parse_ai_text_response(self, response_text: str) -> Dict:
        """解析AI的文本响应为绘图方案"""
        plan = {
            "title": "Figure 1: Patent Drawing",
            "components": [],
            "connections": [],
            "layout": {
                "style": "grid",
                "orientation": "portrait"
            }
        }

        # 提取组件信息
        lines = response_text.split('\n')
        current_component = None

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # 查找组件标记
            if line and line[0].isdigit() and '.' in line:
                parts = line.split('.', 1)
                if len(parts) >= 2:
                    comp_num = parts[0].strip()
                    comp_name = parts[1].strip()

                    # 随机位置生成（避免重叠）
                    import random
                    x = 0.2 + (int(comp_num) % 3) * 0.25 + random.uniform(-0.05, 0.05)
                    y = 0.3 + (int(comp_num) // 3) * 0.25 + random.uniform(-0.05, 0.05)

                    plan["components"].append({
                        "id": comp_num,
                        "name": comp_name,
                        "type": "rectangle",
                        "position": {"x": x, "y": y, "unit": "relative"},
                        "size": {"width": 0.15, "height": 0.1, "unit": "relative"},
                        "description": comp_name
                    })

        return plan

    def _apply_ai_plan(self, drawing: PatentDrawing, request: DrawingRequest, plan: Dict):
        """应用AI生成的绘图方案"""
        if not plan:
            return

        # 添加边框
        self._add_border(drawing)

        # 添加英文标题
        if "title" in plan:
            self._add_english_title(drawing, plan["title"])

        # 绘制组件
        if "components" in plan:
            for comp in plan["components"]:
                self._add_ai_component(drawing, comp)

        # 绘制连接
        if "connections" in plan and "components" in plan:
            self._add_ai_connections(drawing, plan["connections"], plan["components"])

    def _add_english_title(self, drawing: PatentDrawing, title: str):
        """添加英文标题"""
        from ..schemas.drawing_schemas import TextElement
        drawing.elements.append(
            TextElement(
                element_type="title",
                position={"x": drawing.width / 2, "y": self.MARGIN / 2},
                text=title,
                font_size=18,
                font_family="Arial"
            )
        )

    def _add_ai_component(self, drawing: PatentDrawing, comp: Dict):
        """添加AI生成的组件"""
        from ..schemas.drawing_schemas import (
            RectangleElement,
            CircleElement,
            TextElement
        )

        pos = comp.get("position", {"x": 0.3, "y": 0.4})
        size = comp.get("size", {"width": 0.15, "height": 0.1})

        x = pos["x"] * drawing.width
        y = pos["y"] * drawing.height
        w = size["width"] * drawing.width
        h = size["height"] * drawing.height

        comp_type = comp.get("type", "rectangle")
        comp_id = comp.get("id", "1")
        comp_name = comp.get("name", "Component")

        # 绘制组件形状
        if comp_type == "circle":
            r = min(w, h) / 2
            drawing.elements.append(
                CircleElement(
                    element_type="component",
                    position={"x": x + w/2, "y": y + h/2},
                    radius=r
                )
            )
        else:  # rectangle or default
            drawing.elements.append(
                RectangleElement(
                    element_type="component",
                    position={"x": x, "y": y},
                    width=w,
                    height=h
                )
            )

        # 添加数字标记（英文）
        drawing.elements.append(
            TextElement(
                element_type="reference_marker",
                position={"x": x + 5, "y": y + 5},
                text=str(comp_id),
                font_size=12,
                font_family="Arial"
            )
        )

        # 添加英文组件名称
        name = comp_name[:15]  # 限制长度
        drawing.elements.append(
            TextElement(
                element_type="component_name",
                position={"x": x + w/2 - 30, "y": y + h/2 - 8},
                text=name,
                font_size=10,
                font_family="Arial"
            )
        )

        # 记录参考标记
        drawing.reference_markers[str(comp_id)] = comp_name

    def _add_ai_connections(self, drawing: PatentDrawing, connections: List, components: List):
        """添加AI生成的连接线"""
        from ..schemas.drawing_schemas import LineElement

        # 创建组件位置索引
        comp_positions = {}
        for comp in components:
            comp_id = comp.get("id")
            pos = comp.get("position", {})
            size = comp.get("size", {})
            x = pos.get("x", 0.3) * drawing.width + size.get("width", 0) * drawing.width / 2
            y = pos.get("y", 0.3) * drawing.height + size.get("height", 0) * drawing.height / 2
            comp_positions[str(comp_id)] = (x, y)

        # 绘制连接线
        for conn in connections:
            from_id = str(conn.get("from"))
            to_id = str(conn.get("to"))

            if from_id in comp_positions and to_id in comp_positions:
                start = comp_positions[from_id]
                end = comp_positions[to_id]

                drawing.elements.append(
                    LineElement(
                        element_type="connection",
                        position={"x": start[0], "y": start[1]},
                        start_point={"x": start[0], "y": start[1]},
                        end_point={"x": end[0], "y": end[1]},
                        line_style=LineStyle.SOLID,
                        line_width=1.0
                    )
                )

    def _fallback_drawing(self, request: DrawingRequest, output_path: Optional[str] = None) -> str:
        """基础绘图（回退方案）"""
        from .patent_drawing_tool import PatentDrawingTool
        fallback_tool = PatentDrawingTool()
        return fallback_tool.create_drawing(request, output_path)

    def _add_border(self, drawing: PatentDrawing):
        """添加边框"""
        from ..schemas.drawing_schemas import RectangleElement
        drawing.elements.append(
            RectangleElement(
                element_type="border",
                position={"x": self.MARGIN, "y": self.MARGIN + 60},
                width=drawing.width - 2 * self.MARGIN,
                height=drawing.height - 2 * self.MARGIN - 60
            )
        )

    def _render_drawing(self, drawing: PatentDrawing) -> bytes:
        """渲染附图为图像"""
        width_px = int(drawing.width * self.DEFAULT_DPI / 25.4)
        height_px = int(drawing.height * self.DEFAULT_DPI / 25.4)

        image = Image.new('RGB', (width_px, height_px), 'white')
        draw = ImageDraw.Draw(image)

        # 绘制所有元素
        for element in drawing.elements:
            self._draw_element(draw, element, width_px, height_px)

        # 保存为字节流
        buffer = io.BytesIO()
        image.save(buffer, format='PNG', dpi=(self.DEFAULT_DPI, self.DEFAULT_DPI))
        return buffer.getvalue()

    def _draw_element(
        self,
        draw: ImageDraw.Draw,
        element,
        width_px: int,
        height_px: int
    ):
        """绘制单个元素"""
        stroke_width = self.DEFAULT_LINE_WIDTH * 3  # 转换为像素
        scale_x = width_px / 210  # 基于A4宽度
        scale_y = height_px / 297  # 基于A4高度

        def scale(pos):
            return pos["x"] * scale_x, pos["y"] * scale_y

        if element.element_type == "border":
            x, y = scale(element.position)
            w = int(element.width * scale_x)
            h = int(element.height * scale_y)
            x = int(x)
            y = int(y)

            draw.rectangle(
                [x, y, x + w, y + h],
                outline='black',
                width=stroke_width
            )

        elif element.element_type == "component":
            if hasattr(element, 'width') and hasattr(element, 'height'):
                # 矩形
                x, y = scale(element.position)
                w = int(element.width * scale_x)
                h = int(element.height * scale_y)
                x = int(x)
                y = int(y)

                draw.rectangle(
                    [x, y, x + w, y + h],
                    outline='black',
                    width=stroke_width
                )
            elif hasattr(element, 'radius'):
                # 圆形
                cx, cy = scale(element.position)
                r = int(element.radius * (scale_x + scale_y) / 2)
                cx = int(cx)
                cy = int(cy)

                bbox = [cx - r, cy - r, cx + r, cy + r]
                draw.ellipse(bbox, outline='black', width=stroke_width)

        elif element.element_type == "connection":
            start = scale(element.start_point)
            end = scale(element.end_point)
            start = (int(start[0]), int(start[1]))
            end = (int(end[0]), int(end[1]))
            draw.line([start, end], fill='black', width=stroke_width//2)

        elif element.element_type == "title":
            x, y = scale(element.position)
            self._draw_text(draw, element.text, x, y, element.font_size * 2.5, bold=True)

        elif element.element_type in ["reference_marker", "component_name"]:
            x, y = scale(element.position)
            self._draw_text(draw, element.text, x, y, element.font_size)

    def _draw_text(
        self,
        draw: ImageDraw.Draw,
        text: str,
        x: float,
        y: float,
        font_size: float,
        bold: bool = False
    ):
        """绘制文本（仅英文）"""
        try:
            # 确保文本是英文
            text = str(text)

            # 使用默认字体
            font = ImageFont.load_default()

            # 绘制文本（仅黑色）
            draw.text((x, y), text, fill='black', font=font)

        except Exception as e:
            print(f"⚠️ 文本绘制错误: {e}")

    def _encode_base64(self, image_data: bytes) -> str:
        """编码为Base64"""
        import base64
        return base64.b64encode(image_data).decode('utf-8')
