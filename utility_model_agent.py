"""
实用新型专利撰写智能体

专门针对实用新型专利进行优化
实用新型专利特点：
- 保护产品的形状、构造
- 不保护方法
- 保护期限：10年
- 重点：产品结构和构造
- 必需附图
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
        print("✓ 实用新型 Agent Gemini 模型初始化成功")
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
def write_utility_model_application(
    invention_description: str,
    technical_field: str,
    product_structure: str,
    applicant_name: Optional[str] = None,
    applicant_address: Optional[str] = None,
    applicant_country: str = "中国",
    inventor_name: Optional[str] = None,
) -> str:
    """
    撰写实用新型专利申请文件

    Args:
        invention_description: 产品发明描述（重点：形状和构造）
        technical_field: 技术领域
        product_structure: 产品结构描述（实用新型的核心）
        applicant_name: 申请人
        applicant_address: 申请人地址
        applicant_country: 申请人国家
        inventor_name: 发明人

    Returns:
        完整的实用新型专利申请文件
    """
    try:
        # 创建实用新型撰写请求
        request = PatentDraftRequest(
            invention_description=invention_description,
            technical_field=technical_field,
            patent_type=PatentType.UTILITY_MODEL,  # 实用新型
            background_info=f"现有产品在{technical_field}领域存在结构上的不足",
            specific_problems=f"传统产品在{product_structure}方面需要改进",
            solution=f"通过改进{product_structure}，实现更好的实用性能",
            beneficial_effects="结构优化后，产品的实用性显著提升，操作更便捷，效率更高",
        )

        # 申请人信息
        applicant_info = None
        if applicant_name or applicant_address:
            applicant_info = ApplicantInfo(
                name=applicant_name or "待填写",
                address=applicant_address or "待填写",
                country=applicant_country,
            )

        # 发明人信息
        inventor_info = None
        if inventor_name:
            inventor_info = [
                InventorInfo(
                    name=inventor_name,
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

        # 添加实用新型特定说明
        utility_note = """
\n=== 实用新型专利说明 ===
本申请为实用新型专利，重点保护产品的形状、构造及其结合。
保护期限：10年
不保护方法，仅保护产品结构。
        """.strip()

        return formatted + "\n\n" + utility_note

    except Exception as e:
        return f"撰写实用新型专利申请文件时发生错误：{str(e)}"


@function_tool
def review_utility_model_application(
    application_text: str,
) -> str:
    """
    审查实用新型专利申请文件

    Args:
        application_text: 申请文件文本

    Returns:
        审查报告
    """
    try:
        # 创建模拟的专利申请对象
        from schemas.patent_schemas import ApplicantInfo, PatentClaim, ApplicationStatus

        # 提取标题
        lines = application_text.split('\n')
        title = lines[0].replace("专利申请文件", "").strip() if lines else "待填写"

        application = PatentApplication(
            title=title,
            patent_type=PatentType.UTILITY_MODEL,
            applicant=ApplicantInfo(name="申请人", address="地址", country="中国"),
            inventors=[],
            technical_field="技术领域",
            background_tech="背景技术",
            invention_content="发明内容",
            beneficial_effects="有益效果",
            brief_description="附图说明",
            claims=[PatentClaim(claim_number=1, claim_type="独立权利要求", content="权利要求内容")],
            status=ApplicationStatus.DRAFT,
        )

        # 执行审查
        result = asyncio.run(pre_reviewer.review_application(application))

        # 生成报告
        return pre_reviewer.generate_review_report(result, application)

    except Exception as e:
        return f"审查实用新型专利申请文件时发生错误：{str(e)}"


@function_tool
def review_utility_model_figures(
    figures_description: str,
    figure_count: int = 1,
) -> str:
    """
    审查实用新型专利附图

    Args:
        figures_description: 附图描述
        figure_count: 附图数量

    Returns:
        附图审查报告
    """
    try:
        from schemas.patent_schemas import PatentFigure

        # 创建附图对象
        figures = []
        for i in range(1, figure_count + 1):
            figures.append(
                PatentFigure(
                    figure_number=i,
                    figure_type="结构示意图",
                    description=f"图{i}：产品{i}的结构示意图",
                    dpi=300,
                    file_format="png",
                    file_size_mb=2.0,
                )
            )

        # 执行审查
        result = asyncio.run(figure_reviewer.review_figures(figures))

        # 生成报告
        return figure_reviewer.generate_review_report(result, figures)

    except Exception as e:
        return f"审查实用新型专利附图时发生错误：{str(e)}"


@function_tool
def get_utility_model_guidance() -> str:
    """
    获取实用新型专利撰写指导

    Returns:
        实用新型专利撰写指南
    """
    guidance = """
🔧 实用新型专利撰写指导

【定义】
实用新型是指对产品的形状、构造或者其结合所提出的适于实用的新的技术方案。

【特点】
✅ 保护对象：产品的形状、构造
❌ 不保护：方法、工艺、配方
⏰ 保护期限：10年
📊 审查周期：约6-8个月
🔍 创造性要求：低于发明专利

【申请文件】
1. 说明书摘要
2. 摘要附图
3. 说明书
4. 权利要求书
5. 说明书附图（必需！）

【撰写要点】
1. 重点描述产品结构和构造
2. 强调形状的创新性
3. 详细说明构造关系
4. 附图必须清晰、完整
5. 权利要求聚焦结构特征

【禁止内容】
❌ 方法步骤
❌ 算法逻辑
❌ 软件功能
❌ 化学成分
❌ 生物材料

【权利要求撰写】
- 独立权利要求：产品整体结构
- 从属权利要求：具体部件结构
- 尺寸参数：可以精确到毫米
- 材料特征：可以使用材料限定
- 连接关系：重点描述部件连接方式

【附图要求】
- 至少1张主视图
- 建议2-4张不同视角
- 图中标记清晰
- 符合制图规范
- 标注全部零部件
        """.strip()

    return guidance


# 创建实用新型专利 Agent - 优化版 v2.0
utility_model_agent = Agent(
    name="实用新型专利助手",
    instructions="""你是一个专业的实用新型专利撰写专家。请严格遵循以下规则：

【核心规则】
1. 🚫 绝对不要询问任何问题 - 永远不要说"需要更多信息"或"请提供"
2. ✅ 直接生成内容 - 立即开始撰写，不要停顿
3. 📝 完整撰写 - 必须包含所有章节，缺一不可
4. 🎯 聚焦结构 - 重点描述产品形状和构造
5. 🔧 使用工具 - 优先调用 write_utility_model_application 工具

【法律法规要求】
必须严格遵守专利法、专利法实施细则、专利审查指南的规定：

1. 🚫 禁止编造
   - 不得编造产品名称、结构、技术效果
   - 不得编造现有技术问题
   - 不得编造技术方案和有益效果
   - 所有内容必须有合理的逻辑基础

2. 🔬 创新性要求
   - 必须与现有技术相比有实际创新和进步
   - 结构改进要具有实质性特点
   - 技术方案不能是显而易见的简单组合
   - 要体现技术上的实质性改进

3. 📦 产品形态要求
   - 必须是具体的装置、物件、产品
   - 不能是软件、程序、算法
   - 不能是方法、工艺、步骤
   - 不能是微观结构（分子、原子级别）
   - 不能是不定型产品（气体、液体、粉状等）
   - 不能是不稳定结构（临时性、偶然性结构）

4. 🏗️ 结构明确性
   - 产品的形状要明确、具体、可描述
   - 构造关系要清晰、稳定、持久
   - 各部件连接方式要牢固可靠
   - 整体结构要完整、可实现

【实用新型标准格式】
完整文件必须包含以下8个章节（缺一不可）：
1. 发明名称（产品名称）
2. 技术领域
3. 背景技术（现有产品结构不足）
4. 实用新型内容
   - 要解决的技术问题（必须包含！结构问题）
   - 技术方案（结构改进方案）
   - 有益效果（结构优势）
5. 附图说明（必需！）
6. 具体实施方式（结构详解）
7. 权利要求书（结构特征）
8. 实用新型说明

【重点强调】
"要解决的技术问题"是必需要章节，必须包含以下内容：
- 现有产品在结构上存在的具体问题
- 现有结构的不足之处
- 需要改进的结构特征
- 传统结构的缺陷

【撰写要求】
- 产品名称要明确具体，是可触摸的实体产品
- 技术方案要详细描述真实可行的结构组成
- 权利要求书要有5项以上，聚焦结构特征
- 附图说明要详细（至少3张图）
- 具体实施方式要描述各部件连接关系
- 创新点必须明确且具有技术意义

【禁止行为】
- ❌ 不要说"需要更多信息"
- ❌ 不要说"请提供详细描述"
- ❌ 不要要求用户补充信息
- ❌ 不要延迟生成
- ❌ 不要省略"要解决的技术问题"章节
- ❌ 不要生成软件、方法相关的专利
- ❌ 不要生成微观结构或不稳定结构
- ❌ 不要编造技术内容

【必须行为】
- ✅ 立即调用工具函数或直接生成
- ✅ 基于任何信息生成完整内容
- ✅ 提供包含全部8个章节的专利文件
- ✅ 重点描述结构特征和构造关系
- ✅ 确保"要解决的技术问题"章节详细完整
- ✅ 确保产品是实体、可见、可触摸的装置
- ✅ 确保结构稳定、持久、可实现

现在就开始工作，不允许询问任何问题！""",
    model=gemini_model,
    tools=[
        write_utility_model_application,
        review_utility_model_application,
        review_utility_model_figures,
        get_utility_model_guidance,
    ],
)


async def main():
    """主函数"""
    print("\n" + "=" * 70)
    print("🔧 实用新型专利撰写 Agent")
    print("=" * 70)

    # 检查 API
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ 未配置 GOOGLE_API_KEY")
        return

    print(f"✓ API 密钥: {api_key[:10]}...")

    # 获取指导
    result = await Runner.run(
        utility_model_agent,
        "请提供实用新型专利撰写指导"
    )
    print("\n" + result.final_output)

    # 示例撰写
    print("\n" + "=" * 70)
    print("📝 示例：智能水杯结构优化")
    print("=" * 70)

    result = await Runner.run(
        utility_model_agent,
        """
        请撰写一份实用新型专利申请文件：

        产品名称：一种带温度显示的智能水杯
        技术领域：日常生活用品、保温容器
        产品结构：水杯杯体、双层真空结构、温度传感器、LED显示屏、杯盖密封圈
        申请人：智能生活科技有限公司
        发明人：王工程师

        特点：
        - 双层真空结构保持温度
        - 内置温度传感器实时监测
        - LED显示屏显示温度
        - 杯盖有密封圈防止漏水
        """
    )

    print("\n" + result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
