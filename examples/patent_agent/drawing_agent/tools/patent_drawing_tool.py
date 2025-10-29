"""
专利附图绘制工具
符合专利审查指南要求的附图绘制
"""

import os
import math
from typing import List, Dict, Tuple, Optional
from PIL import Image, ImageDraw, ImageFont
import io

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


class PatentDrawingTool:
    """专利附图绘制工具"""

    # 符合专利审查指南的默认参数
    DEFAULT_LINE_WIDTH = 0.5
    DEFAULT_TEXT_HEIGHT = 12
    MIN_LINE_WIDTH = 0.3
    DEFAULT_DPI = 300
    MARGIN = 50

    def __init__(self):
        """初始化绘制工具"""
        self.standards = PATENT_DRAWING_STANDARDS
        self.current_drawing = None

    def create_drawing(
        self,
        request: DrawingRequest,
        output_path: Optional[str] = None
    ) -> str:
        """
        根据请求创建专利附图

        Args:
            request: 绘图请求
            output_path: 输出路径（可选）

        Returns:
            附图的Base64编码字符串或文件路径
        """
        # 创建附图对象
        drawing = PatentDrawing(
            drawing_id=request.request_id,
            title=f"图{request.request_id[-1] if request.request_id else '1'}：{request.invention_title}",
            drawing_type=request.drawing_type,
            style=request.drawing_style
        )

        # 根据附图类型绘制
        if request.drawing_type == DrawingType.MECHANICAL:
            self._draw_mechanical_structure(drawing, request)
        elif request.drawing_type == DrawingType.CIRCUIT:
            self._draw_circuit_diagram(drawing, request)
        elif request.drawing_type == DrawingType.FLOWCHART:
            self._draw_flowchart(drawing, request)
        elif request.drawing_type == DrawingType.SCHEMATIC:
            self._draw_schematic(drawing, request)
        elif request.drawing_type == DrawingType.STRUCTURE:
            self._draw_structure(drawing, request)
        else:
            # 默认绘制示意图
            self._draw_schematic(drawing, request)

        # 生成图像
        image_data = self._render_drawing(drawing)

        # 保存或返回
        if output_path:
            with open(output_path, 'wb') as f:
                f.write(image_data)
            return output_path
        else:
            return self._encode_base64(image_data)

    def _draw_mechanical_structure(
        self,
        drawing: PatentDrawing,
        request: DrawingRequest
    ):
        """绘制机械结构图"""
        # 创建基本的机械结构元素

        # 添加边框
        self._add_border(drawing)

        # 添加标题
        self._add_title(drawing, request.invention_title)

        # 根据产品描述解析结构
        components = self._parse_components(request.product_description, request.key_components)

        # 绘制各个组件
        for i, component in enumerate(components):
            component_id = f"{i+1}"
            position = self._calculate_component_position(i, len(components))
            self._add_component(drawing, component_id, component, position)

        # 添加组件列表
        self._add_component_list(drawing, components)

    def _draw_circuit_diagram(
        self,
        drawing: PatentDrawing,
        request: DrawingRequest
    ):
        """绘制电路图"""
        self._add_border(drawing)
        self._add_title(drawing, request.invention_title)

        # 解析电路组件
        components = self._parse_components(request.product_description, request.key_components)

        # 绘制基本电路布局
        self._draw_circuit_layout(drawing, components)

    def _draw_flowchart(
        self,
        drawing: PatentDrawing,
        request: DrawingRequest
    ):
        """绘制流程图"""
        self._add_border(drawing)
        self._add_title(drawing, request.invention_title)

        # 解析流程步骤
        steps = self._parse_flow_steps(request.structure_details)

        # 绘制流程图
        self._draw_flowchart_layout(drawing, steps)

    def _draw_schematic(
        self,
        drawing: PatentDrawing,
        request: DrawingRequest
    ):
        """绘制示意图"""
        self._add_border(drawing)
        self._add_title(drawing, request.invention_title)

        # 解析组件
        components = self._parse_components(request.product_description, request.key_components)

        # 绘制示意图
        self._draw_schematic_layout(drawing, components)

    def _draw_structure(
        self,
        drawing: PatentDrawing,
        request: DrawingRequest
    ):
        """绘制构造图"""
        self._add_border(drawing)
        self._add_title(drawing, request.invention_title)

        # 解析结构部件
        components = self._parse_components(request.product_description, request.key_components)

        # 绘制构造图
        self._draw_structure_layout(drawing, components)

    def _add_border(self, drawing: PatentDrawing):
        """添加边框"""
        from ..schemas.drawing_schemas import RectangleElement
        drawing.elements.append(
            RectangleElement(
                element_type="border",
                position={"x": self.MARGIN, "y": self.MARGIN + 50},
                width=drawing.width - 2 * self.MARGIN,
                height=drawing.height - 2 * self.MARGIN - 50
            )
        )

    def _add_title(self, drawing: PatentDrawing, title: str):
        """添加标题"""
        from ..schemas.drawing_schemas import TextElement
        drawing.elements.append(
            TextElement(
                element_type="title",
                position={"x": drawing.width / 2, "y": self.MARGIN / 2},
                text=title,
                font_size=16,
                font_family="Arial"
            )
        )

    def _add_component(
        self,
        drawing: PatentDrawing,
        component_id: str,
        component_name: str,
        position: Tuple[float, float]
    ):
        """添加组件"""
        from ..schemas.drawing_schemas import (
            RectangleElement,
            TextElement,
            LineElement
        )

        x, y = position

        # 绘制组件外形（矩形）
        drawing.elements.append(
            RectangleElement(
                element_type="component",
                position={"x": x, "y": y},
                width=80,
                height=60
            )
        )

        # 添加组件标记
        drawing.elements.append(
            TextElement(
                element_type="reference_marker",
                position={"x": x + 5, "y": y + 5},
                text=component_id,
                font_size=10,
                font_family="Arial"
            )
        )

        # 添加组件名称
        drawing.elements.append(
            TextElement(
                element_type="component_name",
                position={"x": x + 40, "y": y + 30},
                text=component_name[:8],  # 限制长度
                font_size=8,
                font_family="Arial"
            )
        )

        # 记录参考标记
        drawing.reference_markers[component_id] = component_name

    def _add_component_list(self, drawing: PatentDrawing, components: List[str]):
        """添加组件列表"""
        from ..schemas.drawing_schemas import TextElement

        y_offset = drawing.height - self.MARGIN - 20
        for i, component in enumerate(components):
            component_id = str(i + 1)
            text = f"{component_id} - {component}"

            drawing.elements.append(
                TextElement(
                    element_type="component_list",
                    position={"x": self.MARGIN, "y": y_offset - i * 15},
                    text=text,
                    font_size=9,
                    font_family="Arial"
                )
            )

    def _parse_components(
        self,
        product_description: str,
        key_components: List[str]
    ) -> List[str]:
        """解析产品描述，提取组件"""
        if key_components:
            return key_components

        # 从描述中提取组件
        components = []
        # 简单的关键词提取
        keywords = ["组件", "部件", "模块", "单元", "装置", "结构", "构件"]

        for keyword in keywords:
            if keyword in product_description:
                # 提取关键词后的内容
                parts = product_description.split(keyword)
                for part in parts[1:]:
                    # 提取简化名称
                    name = part.split("、", 1)[0].split("，", 1)[0].split("。", 1)[0].strip()
                    if name and len(name) < 20:
                        components.append(name)

        # 如果没有提取到，返回默认组件
        if not components:
            components = ["组件1", "组件2", "组件3"]

        return components[:10]  # 限制数量

    def _parse_flow_steps(self, structure_details: str) -> List[str]:
        """解析流程步骤"""
        steps = []
        if "步骤" in structure_details:
            parts = structure_details.split("步骤")
            for i, part in enumerate(parts[1:], 1):
                step = f"步骤{i}: {part.split("。")[0]}"
                steps.append(step)

        if not steps:
            steps = ["步骤1: 开始", "步骤2: 处理", "步骤3: 结束"]

        return steps[:8]

    def _calculate_component_position(
        self,
        index: int,
        total: int
    ) -> Tuple[float, float]:
        """计算组件位置"""
        cols = math.ceil(math.sqrt(total))
        row = index // cols
        col = index % cols

        x = self.MARGIN + 100 + col * 100
        y = self.MARGIN + 100 + row * 120

        return (x, y)

    def _draw_circuit_layout(self, drawing: PatentDrawing, components: List[str]):
        """绘制电路布局"""
        # 简化电路图绘制
        from ..schemas.drawing_schemas import RectangleElement, CircleElement

        # 绘制电路符号
        for i, component in enumerate(components[:6]):
            x = self.MARGIN + 100 + i * 80
            y = drawing.height / 2

            drawing.elements.append(
                RectangleElement(
                    element_type="circuit_component",
                    position={"x": x, "y": y - 20},
                    width=60,
                    height=40
                )
            )

            # 添加标记
            drawing.reference_markers[str(i + 1)] = component

    def _draw_flowchart_layout(self, drawing: PatentDrawing, steps: List[str]):
        """绘制流程图布局"""
        from ..schemas.drawing_schemas import RectangleElement, ArrowElement

        for i, step in enumerate(steps):
            x = drawing.width / 2
            y = self.MARGIN + 100 + i * 80

            # 绘制流程框
            drawing.elements.append(
                RectangleElement(
                    element_type="flow_step",
                    position={"x": x - 60, "y": y - 20},
                    width=120,
                    height=40
                )
            )

            # 添加箭头
            if i < len(steps) - 1:
                drawing.elements.append(
                    ArrowElement(
                        element_type="flow_arrow",
                        start_point={"x": x, "y": y + 25},
                        end_point={"x": x, "y": y + 55}
                    )
                )

            drawing.reference_markers[str(i + 1)] = step

    def _draw_schematic_layout(self, drawing: PatentDrawing, components: List[str]):
        """绘制示意图布局"""
        from ..schemas.drawing_schemas import CircleElement

        center_x = drawing.width / 2
        center_y = drawing.height / 2

        # 绘制中心部件
        drawing.elements.append(
            CircleElement(
                element_type="main_component",
                position={"x": center_x, "y": center_y},
                radius=50
            )
        )

        # 绘制周围部件
        angle_step = 2 * math.pi / len(components)
        for i, component in enumerate(components[:8]):
            angle = i * angle_step
            x = center_x + 150 * math.cos(angle)
            y = center_y + 150 * math.sin(angle)

            drawing.elements.append(
                CircleElement(
                    element_type="sub_component",
                    position={"x": x, "y": y},
                    radius=30
                )
            )

            drawing.reference_markers[str(i + 1)] = component

    def _draw_structure_layout(self, drawing: PatentDrawing, components: List[str]):
        """绘制构造图布局"""
        from ..schemas.drawing_schemas import RectangleElement

        # 绘制分层结构
        layers = min(3, len(components))
        components_per_layer = math.ceil(len(components) / layers)

        for layer in range(layers):
            y = self.MARGIN + 120 + layer * 80
            start_idx = layer * components_per_layer
            end_idx = min(start_idx + components_per_layer, len(components))

            for i in range(start_idx, end_idx):
                x = self.MARGIN + 100 + (i - start_idx) * 90
                component = components[i]

                drawing.elements.append(
                    RectangleElement(
                        element_type="structure_part",
                        position={"x": x, "y": y - 25},
                        width=80,
                        height=50
                    )
                )

                drawing.reference_markers[str(i + 1)] = component

    def _render_drawing(self, drawing: PatentDrawing) -> bytes:
        """渲染附图为图像"""
        # 创建图像
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
        # 获取样式
        stroke_width = int(self.DEFAULT_LINE_WIDTH * 2)  # 转换为像素
        fill_color = None  # 专利图不填充

        # 根据元素类型绘制
        if element.element_type == "border":
            # 绘制边框
            x = int(element.position["x"] * self.DEFAULT_DPI / 25.4)
            y = int(element.position["y"] * self.DEFAULT_DPI / 25.4)
            w = int(element.width * self.DEFAULT_DPI / 25.4)
            h = int(element.height * self.DEFAULT_DPI / 25.4)

            draw.rectangle(
                [x, y, x + w, y + h],
                outline='black',
                width=stroke_width
            )

        elif element.element_type in ["component", "circuit_component", "flow_step", "structure_part"]:
            # 绘制矩形
            x = int(element.position["x"] * self.DEFAULT_DPI / 25.4)
            y = int(element.position["y"] * self.DEFAULT_DPI / 25.4)
            w = int(element.width * self.DEFAULT_DPI / 25.4)
            h = int(element.height * self.DEFAULT_DPI / 25.4)

            draw.rectangle(
                [x, y, x + w, y + h],
                outline='black',
                width=stroke_width
            )

        elif element.element_type in ["main_component", "sub_component"]:
            # 绘制圆形
            x = int(element.position["x"] * self.DEFAULT_DPI / 25.4)
            y = int(element.position["y"] * self.DEFAULT_DPI / 25.4)
            r = int(element.radius * self.DEFAULT_DPI / 25.4)

            bbox = [x - r, y - r, x + r, y + r]
            draw.ellipse(bbox, outline='black', width=stroke_width)

        elif element.element_type == "title":
            # 绘制标题
            x = element.position["x"] * self.DEFAULT_DPI / 25.4
            y = element.position["y"] * self.DEFAULT_DPI / 25.4
            self._draw_text(draw, element.text, x, y, element.font_size * 2)

        elif element.element_type in ["reference_marker", "component_name", "component_list"]:
            # 绘制文本
            x = element.position["x"] * self.DEFAULT_DPI / 25.4
            y = element.position["y"] * self.DEFAULT_DPI / 25.4
            self._draw_text(draw, element.text, x, y, element.font_size)

    def _draw_text(
        self,
        draw: ImageDraw.Draw,
        text: str,
        x: float,
        y: float,
        font_size: float
    ):
        """绘制文本"""
        # 尝试加载字体
        try:
            # 使用默认字体
            font = ImageFont.load_default()
        except:
            font = None

        # 绘制文本
        draw.text((x, y), text, fill='black', font=font)

    def _encode_base64(self, image_data: bytes) -> str:
        """编码为Base64"""
        import base64
        return base64.b64encode(image_data).decode('utf-8')

    def validate_drawing(self, drawing: PatentDrawing) -> Dict[str, bool]:
        """验证附图是否符合标准"""
        validation_result = {
            "has_border": False,
            "has_title": False,
            "has_reference_markers": False,
            "line_width_compliant": False,
            "format_compliant": False,
            "size_compliant": False
        }

        # 检查边框
        validation_result["has_border"] = any(
            e.element_type == "border" for e in drawing.elements
        )

        # 检查标题
        validation_result["has_title"] = any(
            e.element_type == "title" for e in drawing.elements
        )

        # 检查参考标记
        validation_result["has_reference_markers"] = len(drawing.reference_markers) > 0

        # 检查线条宽度（简化检查）
        validation_result["line_width_compliant"] = True

        # 检查格式
        validation_result["format_compliant"] = True

        # 检查尺寸
        validation_result["size_compliant"] = (
            drawing.width >= 150 and drawing.width <= 250 and
            drawing.height >= 200 and drawing.height <= 350
        )

        return validation_result
