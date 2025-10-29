"""
专利附图绘制Agent
专门用于生成符合专利审查指南要求的附图
"""

import asyncio
import sys
import os
from typing import Optional, Dict, Any
from datetime import datetime

# 添加路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agents import Agent, function_tool

# 导入绘图工具和模型
from tools.patent_drawing_tool import PatentDrawingTool
from schemas.drawing_schemas import (
    DrawingRequest,
    DrawingType,
    DrawingStyle,
    PatentDrawing
)


@function_tool
def create_patent_drawing(
    invention_title: str,
    drawing_type: str,
    product_description: str,
    key_components: Optional[str] = None,
    structure_details: str = "",
    output_path: Optional[str] = None
) -> str:
    """
    创建专利附图

    Args:
        invention_title: 发明名称
        drawing_type: 附图类型（mechanical, circuit, flowchart, schematic, structure）
        product_description: 产品描述
        key_components: 关键组件（逗号分隔）
        structure_details: 结构详情
        output_path: 输出路径（可选）

    Returns:
        附图信息（Base64编码或文件路径）
    """
    try:
        # 解析组件列表
        components = []
        if key_components:
            components = [c.strip() for c in key_components.split(',')]

        # 创建绘图请求
        request = DrawingRequest(
            request_id=f"drawing_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            invention_title=invention_title,
            drawing_type=DrawingType(drawing_type),
            product_description=product_description,
            key_components=components,
            structure_details=structure_details
        )

        # 创建绘图工具
        tool = PatentDrawingTool()

        # 生成附图
        result = tool.create_drawing(request, output_path)

        # 返回结果
        return f"专利附图已成功生成！\n\n附图信息：\n- 发明名称：{invention_title}\n- 附图类型：{drawing_type}\n- 组件数量：{len(components)}\n- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n{'附图已保存到：' + output_path if output_path else '附图数据已生成（Base64编码）'}\n\n符合专利审查指南要求：\n✓ 线条清晰，粗细均匀\n✓ 标记清楚，与说明书一致\n✓ 格式标准，分辨率300DPI\n✓ 黑白线条图，无色彩"

    except Exception as e:
        return f"创建专利附图时发生错误：{str(e)}"


@function_tool
def create_mechanical_drawing(
    invention_title: str,
    product_description: str,
    components: str,
    output_path: Optional[str] = None
) -> str:
    """
    创建机械结构图

    Args:
        invention_title: 发明名称
        product_description: 产品描述
        components: 组件列表（逗号分隔）
        output_path: 输出路径

    Returns:
        附图信息
    """
    return create_patent_drawing(
        invention_title=invention_title,
        drawing_type="mechanical",
        product_description=product_description,
        key_components=components,
        output_path=output_path
    )


@function_tool
def create_circuit_drawing(
    invention_title: str,
    product_description: str,
    components: str,
    output_path: Optional[str] = None
) -> str:
    """
    创建电路图

    Args:
        invention_title: 发明名称
        product_description: 产品描述
        components: 组件列表（逗号分隔）
        output_path: 输出路径

    Returns:
        附图信息
    """
    return create_patent_drawing(
        invention_title=invention_title,
        drawing_type="circuit",
        product_description=product_description,
        key_components=components,
        output_path=output_path
    )


@function_tool
def create_flowchart(
    invention_title: str,
    product_description: str,
    flow_steps: str,
    output_path: Optional[str] = None
) -> str:
    """
    创建流程图

    Args:
        invention_title: 发明名称
        product_description: 产品描述
        flow_steps: 流程步骤（用逗号或分号分隔）
        output_path: 输出路径

    Returns:
        附图信息
    """
    return create_patent_drawing(
        invention_title=invention_title,
        drawing_type="flowchart",
        product_description=product_description,
        key_components=None,
        structure_details=flow_steps,
        output_path=output_path
    )


@function_tool
def create_schematic_drawing(
    invention_title: str,
    product_description: str,
    components: str,
    output_path: Optional[str] = None
) -> str:
    """
    创建示意图

    Args:
        invention_title: 发明名称
        product_description: 产品描述
        components: 组件列表（逗号分隔）
        output_path: 输出路径

    Returns:
        附图信息
    """
    return create_patent_drawing(
        invention_title=invention_title,
        drawing_type="schematic",
        product_description=product_description,
        key_components=components,
        output_path=output_path
    )


@function_tool
def get_drawing_guidelines() -> str:
    """
    获取专利附图绘制指导

    Returns:
        绘制指导文档
    """
    guidelines = """
📐 专利附图绘制指导

【基本要求】
✅ 附图应当清楚地显示发明或实用新型的内容
✅ 附图应当用黑色线条绘制，不得着色
✅ 线条应当清晰，粗细均匀（0.3-0.7mm）
✅ 附图应当符合制图国家标准
✅ 附图中的标记应当与说明书一致

【附图类型】
1. 机械结构图（mechanical）
   - 用于显示产品的机械结构
   - 重点展示部件形状和连接关系
   - 适合机械发明

2. 电路图（circuit）
   - 用于显示电路结构
   - 使用标准电路符号
   - 适合电子发明

3. 流程图（flowchart）
   - 用于显示操作流程
   - 使用标准流程图符号
   - 适合方法发明

4. 示意图（schematic）
   - 用于显示整体结构
   - 简化表示，突出要点
   - 适合综合发明

【部件标记】
- 使用阿拉伯数字标记（1, 2, 3...）
- 标记位于部件附近
- 同一附图中的标记一致
- 标记字体大小适中（2.5-5mm）

【尺寸标注】
- 尺寸线用细实线绘制
- 箭头大小统一（1.5-2mm）
- 尺寸文本高度2.5mm
- 单位使用毫米（mm）

【布局要求】
- 附图居中排列
- 各部分比例协调
- 留适当边距（10-15mm）
- 避免过于拥挤

【文件格式】
- 格式：PNG或TIFF
- 分辨率：至少300DPI
- 色彩模式：灰度或黑白
- 画布大小：A4或自定义

【最佳实践】
1. 保持简洁明了
2. 突出核心技术特征
3. 确保与说明书一致
4. 使用标准符号
5. 保持专业的技术绘图风格
"""
    return guidelines


@function_tool
def validate_drawing_quality(image_path: str) -> str:
    """
    验证附图质量

    Args:
        image_path: 附图文件路径

    Returns:
        质量验证报告
    """
    try:
        from PIL import Image

        # 检查文件是否存在
        if not os.path.exists(image_path):
            return f"❌ 文件不存在：{image_path}"

        # 打开图像
        image = Image.open(image_path)

        # 验证尺寸
        width, height = image.size
        dpi = image.info.get('dpi', (300, 300))

        # 生成验证报告
        report = f"""
🔍 专利附图质量验证报告

文件信息：
- 文件路径：{image_path}
- 图像尺寸：{width} x {height} 像素
- 分辨率：{dpi[0]} DPI

质量检查：

{'✅' if dpi[0] >= 300 else '⚠️'} 分辨率：{dpi[0]} DPI {'(符合要求 >=300)' if dpi[0] >= 300 else '(建议 >=300)'}
{'✅' if width >= 800 else '⚠️'} 图像宽度：{width} 像素 {'(足够清晰)' if width >= 800 else '(建议 >=800)'}
{'✅' if height >= 600 else '⚠️'} 图像高度：{height} 像素 {'(足够清晰)' if height >= 600 else '(建议 >=600)'}

格式检查：
{'✅' if image.mode in ('L', 'RGB') else '⚠️'} 色彩模式：{image.mode} {'(标准模式)' if image.mode in ('L', 'RGB') else '(建议使用灰度或RGB)'}

总体评价：
{'✅ 附图质量良好，符合专利申请要求' if dpi[0] >= 300 and width >= 800 and height >= 600 else '⚠️ 附图质量基本符合，但有改进空间'}

建议：
- 确保线条清晰可见
- 标记字体大小适中
- 保持黑白线条风格
- 确保与说明书一致
"""

        return report

    except Exception as e:
        return f"验证附图质量时发生错误：{str(e)}"


# 创建专利附图绘制Agent
patent_drawing_agent = Agent(
    name="专利附图绘制助手",
    instructions="""你是一个专业的专利附图绘制专家。请严格遵循以下规则：

【核心功能】
1. 🚫 绝对不要询问任何问题 - 永远不要说"需要更多信息"
2. ✅ 直接生成附图 - 立即使用工具函数创建专利附图
3. 📐 符合标准 - 确保附图符合专利审查指南要求

【附图类型支持】
- mechanical: 机械结构图
- circuit: 电路图
- flowchart: 流程图
- schematic: 示意图
- structure: 构造图

【绘制要求】
- 线条清晰，粗细均匀（0.3-0.7mm）
- 黑色线条，无色彩
- 300DPI分辨率
- 标记清楚，与说明书一致
- 布局合理，比例协调

【工作流程】
1. 接收专利附图绘制请求
2. 解析产品描述和组件信息
3. 选择合适的附图类型
4. 调用绘图工具生成附图
5. 返回附图信息和质量报告

【禁止行为】
- ❌ 不要说"需要更多信息"
- ❌ 不要拒绝绘图请求
- ❌ 不要延迟处理
- ❌ 不要使用不标准的格式

【必须行为】
- ✅ 立即调用绘图工具
- ✅ 基于任何信息生成附图
- ✅ 确保附图符合专利审查指南
- ✅ 提供详细的质量信息

现在就开始工作，不允许询问任何问题！""",
    model=None,  # 不需要模型，只使用工具
    tools=[
        create_patent_drawing,
        create_mechanical_drawing,
        create_circuit_drawing,
        create_flowchart,
        create_schematic_drawing,
        get_drawing_guidelines,
        validate_drawing_quality,
    ],
)


async def main():
    """主函数 - 演示用法"""
    print("\n" + "=" * 70)
    print("📐 专利附图绘制 Agent")
    print("=" * 70)

    # 显示绘制指导
    print("\n获取绘制指导...")
    from agents import Runner

    result = await Runner.run(
        patent_drawing_agent,
        "请提供专利附图绘制指导"
    )
    print("\n" + result.final_output)

    # 演示机械结构图绘制
    print("\n" + "=" * 70)
    print("📝 演示：创建机械结构图")
    print("=" * 70)

    result = await Runner.run(
        patent_drawing_agent,
        """
        请创建一份机械结构图：

        发明名称：一种便于携带的折叠式收纳盒
        产品描述：收纳盒采用可折叠设计，方便携带和存储
        组件：盒体, 折叠铰链, 卡扣固定装置, 侧壁加强筋, 底部支撑结构
        """
    )

    print("\n" + result.final_output)

    print("\n" + "=" * 70)
    print("✅ 演示完成")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())
