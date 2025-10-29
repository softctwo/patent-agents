"""
专利附图绘制数据模型
符合专利审查指南要求的附图定义
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum


class DrawingType(str, Enum):
    """专利附图类型"""
    MECHANICAL = "mechanical"  # 机械结构图
    CIRCUIT = "circuit"  # 电路图
    FLOWCHART = "flowchart"  # 流程图
    SCHEMATIC = "schematic"  # 示意图
    STRUCTURE = "structure"  # 构造图
    ASSEMBLY = "assembly"  # 装配图
    SECTION = "section"  # 剖面图
    DETAIL = "detail"  # 详图
    OVERVIEW = "overview"  # 整体图
    COMPONENT = "component"  # 零部件图


class DrawingStyle(str, Enum):
    """绘图风格"""
    LINE_ART = "line_art"  # 线条图
    BLACK_WHITE = "black_white"  # 黑白图
    TECHNICAL = "technical"  # 技术图
    OUTLINE = "outline"  # 轮廓图


class LineStyle(str, Enum):
    """线条类型"""
    SOLID = "solid"  # 实线
    DASHED = "dashed"  # 虚线
    DOTTED = "dotted"  # 点线
    THICK = "thick"  # 粗线
    THIN = "thin"  # 细线


class DrawingElement(BaseModel):
    """绘图元素基类"""
    element_type: str = Field(..., description="元素类型")
    position: Dict[str, float] = Field(..., description="位置坐标")
    style: Optional[Dict[str, Any]] = Field(default=None, description="样式")


class LineElement(DrawingElement):
    """线条元素"""
    start_point: Dict[str, float] = Field(..., description="起点")
    end_point: Dict[str, float] = Field(..., description="终点")
    line_style: LineStyle = Field(default=LineStyle.SOLID, description="线条类型")
    line_width: float = Field(default=1.0, description="线条宽度")


class RectangleElement(DrawingElement):
    """矩形元素"""
    width: float = Field(..., description="宽度")
    height: float = Field(..., description="高度")


class CircleElement(DrawingElement):
    """圆形元素"""
    radius: float = Field(..., description="半径")


class ArrowElement(DrawingElement):
    """箭头元素"""
    start_point: Dict[str, float] = Field(..., description="起点")
    end_point: Dict[str, float] = Field(..., description="终点")
    arrow_size: float = Field(default=1.0, description="箭头大小")


class TextElement(DrawingElement):
    """文本元素"""
    text: str = Field(..., description="文本内容")
    font_size: float = Field(default=12, description="字体大小")
    font_family: str = Field(default="Arial", description="字体家族")


class DimensionElement(DrawingElement):
    """尺寸标注元素"""
    start_point: Dict[str, float] = Field(..., description="起点")
    end_point: Dict[str, float] = Field(..., description="终点")
    dimension_text: str = Field(..., description="尺寸文本")


class ComponentElement(DrawingElement):
    """组件元素"""
    component_id: str = Field(..., description="组件ID")
    component_name: str = Field(..., description="组件名称")
    shape: str = Field(..., description="形状类型")
    dimensions: Dict[str, float] = Field(default_factory=dict, description="尺寸")


class PatentDrawing(BaseModel):
    """专利附图"""
    drawing_id: str = Field(..., description="附图ID")
    title: str = Field(..., description="附图标题")
    drawing_type: DrawingType = Field(..., description="附图类型")
    style: DrawingStyle = Field(default=DrawingStyle.LINE_ART, description="绘图风格")
    width: float = Field(default=210, description="画布宽度(mm)")
    height: float = Field(default=297, description="画布高度(mm)")
    dpi: int = Field(default=300, description="分辨率")
    elements: List[DrawingElement] = Field(default_factory=list, description="绘图元素")
    reference_markers: Dict[str, str] = Field(default_factory=dict, description="参考标记")
    description: str = Field(default="", description="附图说明")
    layer_info: Optional[Dict[str, Any]] = Field(default=None, description="图层信息")


class DrawingTemplate(BaseModel):
    """绘图模板"""
    template_id: str = Field(..., description="模板ID")
    template_name: str = Field(..., description="模板名称")
    drawing_type: DrawingType = Field(..., description="适用的附图类型")
    description: str = Field(..., description="模板描述")
    standard_elements: List[Dict[str, Any]] = Field(default_factory=list, description="标准元素")
    layout_config: Dict[str, Any] = Field(default_factory=dict, description="布局配置")


class DrawingRequest(BaseModel):
    """绘图请求"""
    request_id: str = Field(..., description="请求ID")
    invention_title: str = Field(..., description="发明名称")
    drawing_type: DrawingType = Field(..., description="附图类型")
    product_description: str = Field(..., description="产品描述")
    key_components: List[str] = Field(default_factory=list, description="关键组件")
    structure_details: str = Field(default="", description="结构详情")
    drawing_style: DrawingStyle = Field(default=DrawingStyle.LINE_ART, description="绘图风格")
    output_format: str = Field(default="png", description="输出格式")
    additional_requirements: Dict[str, Any] = Field(default_factory=dict, description="附加要求")


class DrawingStandard(BaseModel):
    """专利审查指南绘图标准"""
    standard_id: str = Field(..., description="标准ID")
    standard_name: str = Field(..., description="标准名称")
    guidelines: List[str] = Field(..., description="指导原则")
    requirements: Dict[str, Any] = Field(..., description="具体要求")
    examples: List[str] = Field(default_factory=list, description="示例")


# 专利审查指南绘图标准
PATENT_DRAWING_STANDARDS = {
    "basic_requirements": DrawingStandard(
        standard_id="basic",
        standard_name="基本要求",
        guidelines=[
            "附图应当清楚地显示发明或实用新型的内容",
            "附图应当用黑色线条绘制，不得着色",
            "线条应当清晰，粗细均匀",
            "附图应当符合制图国家标准",
            "附图中的标记应当与说明书一致"
        ],
        requirements={
            "line_width": "0.3-0.7mm",
            "min_line_width": "0.3mm",
            "text_height": ">=2.5mm",
            "dpi": ">=300",
            "format": "PNG/TIFF",
            "color_mode": "Grayscale"
        }
    ),
    "component_marking": DrawingStandard(
        standard_id="marking",
        standard_name="部件标记",
        guidelines=[
            "附图中的部件应当用阿拉伯数字标记",
            "标记应当位于部件附近",
            "同一附图中的标记应当一致",
            "标记的字体大小应当适中",
            "避免标记与线条重叠"
        ],
        requirements={
            "font_size": "2.5-5mm",
            "font_family": "Arial/Helvetica",
            "offset": "1-2mm",
            "style": "Bold"
        }
    ),
    "dimensioning": DrawingStandard(
        standard_id="dimensioning",
        standard_name="尺寸标注",
        guidelines=[
            "尺寸标注应当用毫米为单位",
            "尺寸线应当用细实线绘制",
            "箭头大小应当统一",
            "避免在附图内部标注",
            "重要的尺寸应当标注"
        ],
        requirements={
            "dimension_line_width": "0.3mm",
            "arrow_size": "1.5-2mm",
            "text_size": "2.5mm",
            "unit": "mm"
        }
    ),
    "layout": DrawingStandard(
        standard_id="layout",
        standard_name="布局要求",
        guidelines=[
            "附图应当居中排列",
            "各部分比例应当协调",
            "留有适当的边距",
            "避免过于拥挤",
            "保持视觉平衡"
        ],
        requirements={
            "margin": "10-15mm",
            "title_height": "20-30mm",
            "min_spacing": "5mm"
        }
    )
}
