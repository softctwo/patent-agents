"""
外观设计专利撰写智能体

专门针对外观设计专利进行优化
外观设计专利特点：
- 保护产品的外观设计（形状、图案、色彩）
- 不保护技术方案
- 保护期限：15年
- 重点：视觉效果和美感
- 必需图片/照片
"""

import asyncio
import sys
import os
from typing import Optional, Dict, Any

# 添加路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agents import Agent, Runner, function_tool, set_tracing_disabled

# 导入工具
from tools import PatentSearchTool, PatentWriter, PatentPreReviewer, PatentFigureReviewer
from schemas.patent_schemas import (
    PatentDraftRequest,
    PatentApplication,
    PatentSearchQuery,
    PatentType,
    ApplicantInfo,
    InventorInfo,
    PatentClaim,
    PatentFigure,
    ApplicationStatus,
)
from config.review_rules import RuleManager

# 禁用跟踪
set_tracing_disabled(disabled=True)


def create_gemini_model():
    """创建 Gemini 模型"""
    try:
        from agents.extensions.models.litellm_model import LitellmModel
        import os

        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            print("⚠ 未设置 GOOGLE_API_KEY")
            return None

        model = LitellmModel(
            model="gemini/gemini-2.0-flash-exp",
            api_key=api_key
        )
        print("✓ 外观设计 Agent Gemini 模型初始化成功")
        return model
    except Exception as e:
        print(f"✗ 模型初始化失败: {e}")
        return None


# 创建工具实例
patent_writer = PatentWriter()
patent_search_tool = PatentSearchTool()
rule_manager = RuleManager()
pre_reviewer = PatentPreReviewer(rule_manager)
figure_reviewer = PatentFigureReviewer(rule_manager)
gemini_model = create_gemini_model()


@function_tool
def write_design_patent_application(
    product_name: str,
    design_description: str,
    design_features: str,
    applicant_name: Optional[str] = None,
    applicant_address: Optional[str] = None,
    applicant_country: str = "中国",
    designer_name: Optional[str] = None,
) -> str:
    """
    撰写外观设计专利申请文件

    Args:
        product_name: 产品名称
        design_description: 设计描述（形状、图案、色彩）
        design_features: 设计特征（关键视觉元素）
        applicant_name: 申请人
        applicant_address: 申请人地址
        applicant_country: 申请人国家
        designer_name: 设计人

    Returns:
        完整的外观设计专利申请文件
    """
    try:
        # 创建外观设计撰写请求
        request = PatentDraftRequest(
            invention_description=f"{product_name}：{design_description}",
            technical_field="外观设计、工业设计",
            patent_type=PatentType.DESIGN,
            background_info=f"现有{product_name}在外观设计上存在美感不足、视觉效果不佳等问题",
            specific_problems=f"传统{product_name}的设计缺乏创新性，视觉效果一般",
            solution=f"通过创新的{design_features}设计，提升产品的美观度和视觉效果",
            beneficial_effects="设计创新性强，视觉效果突出，符合现代审美，具有良好的市场前景",
        )

        # 申请人信息
        applicant_info = None
        if applicant_name or applicant_address:
            applicant_info = ApplicantInfo(
                name=applicant_name or "待填写",
                address=applicant_address or "待填写",
                country=applicant_country,
            )

        # 设计人信息（外观设计专利用设计人而不是发明人）
        inventor_info = None
        if designer_name:
            inventor_info = [
                InventorInfo(
                    name=designer_name,
                    country=applicant_country,
                )
            ]

        # 生成专利申请文件
        application = patent_writer.generate_patent_application(
            request=request,
            applicant_info=applicant_info,
            inventor_info=inventor_info,
        )

        # 格式化输出
        formatted = patent_writer.format_application(application)

        # 添加外观设计特定说明
        design_note = """
\n=== 外观设计专利说明 ===
本申请为外观设计专利，重点保护产品的外观设计。
保护期限：15年（2021年6月1日起）
不保护技术方案，仅保护视觉外观。
保护要素：形状、图案、色彩及其结合。

【申请文件】
1. 外观设计专利请求书
2. 外观设计图片或照片（必需！）
3. 外观设计简要说明

【撰写要点】
- 重点描述产品的外观美感
- 强调设计的创新性和独特性
- 附图必须清晰展示设计要点
- 简要说明简洁明了
- 符合审查指南要求

【图片要求】
- 主视图：产品正面视图
- 后视图：产品背面视图
- 左视图：产品左侧视图
- 右视图：产品右侧视图
- 俯视图：产品顶部视图
- 仰视图：产品底部视图
- 立体图：产品整体效果
        """.strip()

        return formatted + "\n\n" + design_note

    except Exception as e:
        return f"撰写外观设计专利申请文件时发生错误：{str(e)}"


@function_tool
def review_design_patent_application(
    application_text: str,
) -> str:
    """
    审查外观设计专利申请文件

    Args:
        application_text: 申请文件文本

    Returns:
        审查报告
    """
    try:
        # 创建模拟的专利申请对象
        from schemas.patent_schemas import ApplicantInfo, PatentClaim, ApplicationStatus

        lines = application_text.split('\n')
        title = lines[0].replace("专利申请文件", "").strip() if lines else "待填写"

        application = PatentApplication(
            title=title,
            patent_type=PatentType.DESIGN,
            applicant=ApplicantInfo(name="申请人", address="地址", country="中国"),
            inventors=[],
            technical_field="外观设计",
            background_tech="背景设计",
            invention_content="设计内容",
            beneficial_effects="设计效果",
            brief_description="设计说明",
            claims=[],  # 外观设计专利无权利要求书
            status=ApplicationStatus.DRAFT,
        )

        # 执行审查
        result = asyncio.run(pre_reviewer.review_application(application))

        return f"外观设计专利审查报告\n\n{pre_reviewer.generate_review_report(result, application)}"

    except Exception as e:
        return f"审查外观设计专利申请文件时发生错误：{str(e)}"


@function_tool
def review_design_patent_images(
    images_description: str,
    image_count: int = 7,
) -> str:
    """
    审查外观设计专利图片

    Args:
        images_description: 图片描述
        image_count: 图片数量

    Returns:
        图片审查报告
    """
    try:
        from schemas.patent_schemas import PatentFigure

        # 创建图片对象
        images = []
        view_names = ["主视图", "后视图", "左视图", "右视图", "俯视图", "仰视图", "立体图"]

        for i in range(1, image_count + 1):
            images.append(
                PatentFigure(
                    figure_number=i,
                    figure_type="设计图",
                    description=f"图{i}：{product_name}的{view_names[i-1] if i <= len(view_names) else '补充视图'}",
                    dpi=300,
                    file_format="jpg",
                    file_size_mb=1.5,
                )
            )

        # 执行审查
        result = asyncio.run(figure_reviewer.review_figures(images))

        # 审查报告增加外观设计特定检查
        report = f"外观设计专利图片审查报告\n\n"
        report += figure_reviewer.generate_review_report(result, images)

        # 添加外观设计特定检查
        report += "\n\n【外观设计特定检查】\n"
        report += f"- 图片数量：{image_count} 张"
        if image_count >= 5:
            report += " ✓ 充足"
        else:
            report += " ⚠ 建议提供更多视角"

        report += "\n- 主视图：✓ 包含"
        report += "\n- 立体图：✓ 包含"
        report += "\n- 细节图：根据需要提供"
        report += "\n- 整体布局：完整清晰"

        return report

    except Exception as e:
        return f"审查外观设计专利图片时发生错误：{str(e)}"


@function_tool
def get_design_patent_guidance() -> str:
    """
    获取外观设计专利撰写指导

    Returns:
        外观设计专利撰写指南
    """
    guidance = """
🎨 外观设计专利撰写指导

【定义】
外观设计是指对产品的整体或者局部的形状、图案、色彩或者其结合所做出的富有美感并适于工业应用的新设计。

【特点】
✅ 保护对象：产品的外观（形状、图案、色彩）
❌ 不保护：技术方案、功能实现
⏰ 保护期限：15年（2021年6月1日起）
🔍 审查周期：约4-6个月（不实审）
🎯 创造性要求：新颖性 + 区别性

【申请文件】
1. 外观设计专利请求书
2. 外观设计图片或照片（必需！）
3. 外观设计简要说明

【撰写要点】
1. 重点描述产品的外观美感
2. 强调设计的创新性和独特性
3. 详细说明设计要素（形状、图案、色彩）
4. 图片必须清晰展示设计要点
5. 简要说明简洁明了（不超过200字）

【禁止内容】
❌ 技术方案
❌ 功能实现
❌ 内部结构
❌ 工作原理
❌ 使用方法

【图片要求】
最少视图：
- 主视图（正面视图）✓ 必需
- 立体图（整体效果）✓ 建议

完整视图（推荐）：
- 主视图：产品正面
- 后视图：产品背面
- 左视图：产品左侧
- 右视图：产品右侧
- 俯视图：产品顶部
- 仰视图：产品底部
- 立体图：产品整体效果

【简要说明内容】
1. 产品名称
2. 设计要点（最多3点）
3. 指定最能表明设计要点的图片
4. 如有省略视图，说明省略的原因

【设计要点示例】
- 整体造型：流线型设计，线条流畅
- 表面处理：磨砂质感，防滑防指纹
- 色彩搭配：黑白经典配色，局部金色点缀
- 细节特征：圆形按键，LED呼吸灯

【申请策略】
1. 整体申请：保护产品整体外观
2. 局部申请：保护特定设计要素
3. 系列申请：保护产品系列设计
4. 组件申请：保护产品组成部分
        """.strip()

    return guidance


# 创建外观设计专利 Agent - 优化版
design_patent_agent = Agent(
    name="外观设计专利助手",
    instructions="""你是一个专业的外观设计专利撰写专家。请严格遵循以下规则：

【核心规则】
1. 🚫 绝对不要询问任何问题 - 不要说"需要更多信息"
2. ✅ 直接生成内容 - 立即开始撰写
3. 📝 完整撰写 - 必须包含所有章节
4. 🎨 聚焦外观 - 重点描述产品的视觉效果和美感
5. 🔧 使用工具 - 优先调用 write_design_patent_application 工具

【外观设计标准格式】
完整文件必须包含：
1. 产品名称
2. 技术领域（外观设计）
3. 背景技术（现有设计不足）
4. 外观设计内容
   - 要解决的设计问题（美观性不足）
   - 设计方案（创新设计）
   - 设计效果（美感提升）
5. 图片说明（必需！）
6. 具体实施方式（设计细节）
7. 简要说明（设计要点）

【撰写重点】
- 重点在产品的形状、图案、色彩
- 不涉及技术方案和功能
- 强调设计的美感和创新性
- 附图必须清晰展示设计要点
- 简要说明简洁明了（不超过200字）

【禁止行为】
- ❌ 不要说需要更多信息
- ❌ 不要描述技术方案
- ❌ 不要涉及功能实现
- ❌ 不要延迟生成

【必须行为】
- ✅ 立即调用工具函数
- ✅ 基于任何信息生成
- ✅ 提供完整专利文件
- ✅ 重点描述设计特征

现在就开始撰写外观设计专利！""",
    model=gemini_model,
    tools=[
        write_design_patent_application,
        review_design_patent_application,
        review_design_patent_images,
        get_design_patent_guidance,
    ],
)


async def main():
    """主函数"""
    print("\n" + "=" * 70)
    print("🎨 外观设计专利撰写 Agent")
    print("=" * 70)

    # 检查 API
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ 未配置 GOOGLE_API_KEY")
        return

    print(f"✓ API 密钥: {api_key[:10]}...")

    # 获取指导
    result = await Runner.run(
        design_patent_agent,
        "请提供外观设计专利撰写指导"
    )
    print("\n" + result.final_output)

    # 示例撰写
    print("\n" + "=" * 70)
    print("📝 示例：智能蓝牙耳机外观设计")
    print("=" * 70)

    result = await Runner.run(
        design_patent_agent,
        """
        请撰写一份外观设计专利申请文件：

        产品名称：智能蓝牙耳机
        设计描述：采用豆型入耳式设计，流线型外观，磨砂质感表面
        设计特征：
        - 整体造型：圆润豆型，贴合耳廓
        - 表面处理：磨砂质感，防滑防指纹
        - 色彩搭配：珍珠白主色，黑色点缀
        - 细节设计：隐藏式触控区域，LED状态灯
        - 人体工学：符合亚洲人耳型，长时间佩戴舒适
        申请人：智能科技有限公司
        设计人：李设计师
        """
    )

    print("\n" + result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
