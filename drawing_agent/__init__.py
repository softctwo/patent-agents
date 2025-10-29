"""
专利附图绘制Agent
专门用于生成符合专利审查指南要求的附图

主要功能：
- 机械结构图绘制
- 电路图绘制
- 流程图绘制
- 示意图绘制
- 构造图绘制

符合专利审查指南要求：
- 线条清晰，粗细均匀
- 黑色线条，无色彩
- 300DPI分辨率
- 标记清楚，与说明书一致
"""

from .patent_drawing_agent import (
    patent_drawing_agent,
    create_patent_drawing,
    create_mechanical_drawing,
    create_circuit_drawing,
    create_flowchart,
    create_schematic_drawing,
    get_drawing_guidelines,
    validate_drawing_quality
)

from .tools.patent_drawing_tool import PatentDrawingTool
from .schemas.drawing_schemas import (
    DrawingType,
    DrawingStyle,
    PatentDrawing,
    DrawingRequest
)

__all__ = [
    'patent_drawing_agent',
    'create_patent_drawing',
    'create_mechanical_drawing',
    'create_circuit_drawing',
    'create_flowchart',
    'create_schematic_drawing',
    'get_drawing_guidelines',
    'validate_drawing_quality',
    'PatentDrawingTool',
    'DrawingType',
    'DrawingStyle',
    'PatentDrawing',
    'DrawingRequest'
]
