"""
专利撰写和审查主代理

协调整个专利工作流程，包括：
1. 专利撰写
2. 专利预审
3. 附图审查
4. 专利检索
"""

import asyncio
import sys
import os
from typing import Optional, Dict, Any
from datetime import datetime

# 添加当前目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agents import Agent, Runner, function_tool, set_tracing_disabled

from tools import PatentSearchTool, PatentWriter, PatentPreReviewer, PatentFigureReviewer
from schemas.patent_schemas import (
    PatentDraftRequest,
    PatentApplication,
    PatentSearchQuery,
    PatentWorkflowRequest,
    PatentType,
    ApplicantInfo,
    InventorInfo,
)
from config.review_rules import RuleManager

# 禁用跟踪以简化输出
set_tracing_disabled(disabled=True)


def create_gemini_model():
    """创建 Google Gemini 模型实例"""
    try:
        from agents.extensions.models.litellm_model import LitellmModel
        import os

        # 检查 API key
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            print("⚠ 警告：未设置 GOOGLE_API_KEY 环境变量")
            print("请设置：export GOOGLE_API_KEY='your_api_key'")
            return None

        # 创建 Gemini 模型
        model = LitellmModel(
            model="gemini/gemini-2.0-flash-exp",
            api_key=api_key
        )
        print("✓ Gemini 模型初始化成功")
        return model
    except Exception as e:
        print(f"✗ Gemini 模型初始化失败：{e}")
        return None


# 创建工具实例
patent_writer = PatentWriter()
patent_search_tool = PatentSearchTool()
rule_manager = RuleManager()
pre_reviewer = PatentPreReviewer(rule_manager)
figure_reviewer = PatentFigureReviewer(rule_manager)

# 创建 Gemini 模型
gemini_model = create_gemini_model()


@function_tool
def write_patent_application(
    invention_description: str,
    technical_field: str,
    patent_type: str = "invention",
    background_info: Optional[str] = None,
    specific_problems: Optional[str] = None,
    solution: Optional[str] = None,
    beneficial_effects: Optional[str] = None,
    applicant_name: Optional[str] = None,
    applicant_address: Optional[str] = None,
    applicant_country: str = "中国",
    inventor_name: Optional[str] = None,
) -> str:
    """
    撰写专利申请文件

    Args:
        invention_description: 发明描述
        technical_field: 技术领域
        patent_type: 专利类型（invention/utility_model/design）
        background_info: 背景信息
        specific_problems: 要解决的技术问题
        solution: 技术解决方案
        beneficial_effects: 有益效果
        applicant_name: 申请人姓名
        applicant_address: 申请人地址
        applicant_country: 申请人国家
        inventor_name: 发明人姓名

    Returns:
        格式化的专利申请文件
    """
    try:
        # 创建撰写请求
        request = PatentDraftRequest(
            invention_description=invention_description,
            technical_field=technical_field,
            patent_type=PatentType(patent_type),
            background_info=background_info,
            specific_problems=specific_problems,
            solution=solution,
            beneficial_effects=beneficial_effects,
        )

        # 创建申请人信息
        applicant_info = None
        if applicant_name or applicant_address:
            applicant_info = ApplicantInfo(
                name=applicant_name or "待填写",
                address=applicant_address or "待填写",
                country=applicant_country,
            )

        # 创建发明人信息
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
        return patent_writer.format_application(application)

    except Exception as e:
        return f"撰写专利申请文件时发生错误：{str(e)}"


@function_tool
def review_patent_application(
    application_text: str,
    patent_type: str = "invention",
) -> str:
    """
    审查专利申请文件

    Args:
        application_text: 专利申请文件文本
        patent_type: 专利类型

    Returns:
        审查报告
    """
    try:
        # 这里简化处理，实际应用中需要解析申请文本
        # 创建模拟的专利申请对象
        from .schemas.patent_schemas import (
            ApplicantInfo,
            PatentClaim,
            ApplicationStatus,
        )

        # 提取标题（假设标题在第一行）
        lines = application_text.split('\n')
        title = lines[0].replace("专利申请文件", "").strip() if lines else "待填写"

        application = PatentApplication(
            title=title,
            patent_type=PatentType(patent_type),
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
        return f"审查专利申请文件时发生错误：{str(e)}"


@function_tool
def review_patent_figures(
    figures_description: str,
    figure_count: int = 1,
) -> str:
    """
    审查专利附图

    Args:
        figures_description: 附图描述信息
        figure_count: 附图数量

    Returns:
        附图审查报告
    """
    try:
        from .schemas.patent_schemas import PatentFigure

        # 创建模拟的附图对象
        figures = []
        for i in range(1, figure_count + 1):
            figures.append(
                PatentFigure(
                    figure_number=i,
                    figure_type="示意图",
                    description=f"图{i}说明",
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
        return f"审查附图时发生错误：{str(e)}"


@function_tool
def search_patents(
    keywords: str,
    patent_types: Optional[str] = None,
    applicant: Optional[str] = None,
    inventor: Optional[str] = None,
) -> str:
    """
    检索专利

    Args:
        keywords: 关键词（多个关键词用逗号分隔）
        patent_types: 专利类型筛选（invention,utility_model,design）
        applicant: 申请人筛选
        inventor: 发明人筛选

    Returns:
        专利检索报告
    """
    try:
        # 解析关键词
        keyword_list = [k.strip() for k in keywords.split(',') if k.strip()]

        # 解析专利类型
        types_list = None
        if patent_types:
            types_list = [PatentType(t.strip()) for t in patent_types.split(',') if t.strip()]

        # 创建检索查询
        query = PatentSearchQuery(
            keywords=keyword_list,
            patent_types=types_list,
            applicant=applicant,
            inventor=inventor,
        )

        # 执行检索
        result = asyncio.run(patent_search_tool.search_patents(query))

        # 格式化输出
        report = f"专利检索报告\n"
        report += f"{'='*50}\n\n"
        report += f"检索关键词：{', '.join(keyword_list)}\n"
        report += f"检索时间：{result.generated_at.strftime('%Y-%m-%d %H:%M:%S')}\n"
        report += f"总结果数：{result.total_results}\n\n"

        report += f"相关性分布：\n"
        report += f"- 高相关度：{result.high_relevance_count} 篇\n"
        report += f"- 中相关度：{result.medium_relevance_count} 篇\n"
        report += f"- 低相关度：{result.low_relevance_count} 篇\n\n"

        if result.analysis:
            report += f"检索分析：\n{result.analysis}\n"

        if result.novelty_analysis:
            report += f"\n新颖性分析：\n{result.novelty_analysis}\n"

        if result.recommendations:
            report += f"\n建议：\n"
            for i, rec in enumerate(result.recommendations, 1):
                report += f"{i}. {rec}\n"

        # 添加部分检索结果
        if result.results:
            report += f"\n主要检索结果（前5篇）：\n"
            report += f"{'-'*50}\n"
            for i, patent in enumerate(result.results[:5], 1):
                report += f"\n{i}. {patent.title}\n"
                report += f"   申请人：{patent.applicant}\n"
                if patent.similarity_score:
                    report += f"   相似度：{patent.similarity_score:.2f}\n"

        return report

    except Exception as e:
        return f"检索专利时发生错误：{str(e)}"


@function_tool
def configure_review_rules(
    rule_type: str,
    rule_id: str,
    action: str,
) -> str:
    """
    配置审查规则

    Args:
        rule_type: 规则类型（pre_review/figure_review）
        rule_id: 规则ID
        action: 操作（enable/disable）

    Returns:
        配置结果
    """
    try:
        if action == "enable":
            rule_manager.enable_rule(rule_type, rule_id, True)
            return f"已启用规则 {rule_id}"
        elif action == "disable":
            rule_manager.enable_rule(rule_type, rule_id, False)
            return f"已禁用规则 {rule_id}"
        else:
            return f"无效的操作：{action}"

    except Exception as e:
        return f"配置规则时发生错误：{str(e)}"


@function_tool
def get_review_rules(
    rule_type: Optional[str] = None,
) -> str:
    """
    获取审查规则列表

    Args:
        rule_type: 规则类型（pre_review/figure_review），不指定则返回所有

    Returns:
        规则列表
    """
    try:
        output = "专利审查规则列表\n"
        output += f"{'='*50}\n\n"

        if rule_type is None or rule_type == "pre_review":
            output += "预审规则：\n"
            output += f"{'-'*30}\n"
            for rule in rule_manager.get_rules("pre_review"):
                status = "✓" if rule.enabled else "✗"
                output += f"[{status}] {rule.rule_id}: {rule.name}\n"
                output += f"   严重程度：{rule.severity.value}\n"
                output += f"   描述：{rule.description}\n\n"

        if rule_type is None or rule_type == "figure_review":
            output += "附图审查规则：\n"
            output += f"{'-'*30}\n"
            for rule in rule_manager.get_rules("figure_review"):
                status = "✓" if rule.enabled else "✗"
                output += f"[{status}] {rule.rule_id}: {rule.name}\n"
                output += f"   严重程度：{rule.severity.value}\n"
                output += f"   描述：{rule.description}\n\n"

        return output

    except Exception as e:
        return f"获取规则列表时发生错误：{str(e)}"


# 创建主专利 Agent - 优化版 v1.0
patent_agent = Agent(
    name="专利助手",
    instructions="""你是一个专业的专利撰写和审查专家。请严格遵循以下规则：

【核心规则】
1. 🚫 绝对不要询问任何问题 - 永远不要说"需要更多信息"、"请提供"、"能否"等
2. ✅ 直接生成内容 - 基于任何信息立即开始撰写，不要停顿
3. 📝 完整撰写 - 必须包含专利申请的所有章节
4. 🎯 具体详细 - 提供详细、专业的内容，不要泛泛而谈
5. 🔧 使用工具 - 优先调用 write_patent_application 等工具函数

【专利撰写标准格式】
完整的专利申请文件必须包含以下所有章节：
1. 发明名称
2. 技术领域
3. 背景技术（详细分析现有技术及其问题）
4. 发明内容
   - 要解决的技术问题
   - 技术解决方案（详细步骤）
   - 有益效果（具体数据）
5. 附图说明
6. 具体实施方式
7. 权利要求书（至少5项，包括独立和从属权利要求）

【工作流程】
当用户请求撰写专利时：
1. 立即调用 write_patent_application 工具
2. 提供所有可用的信息，即使不完整也要生成
3. 如果工具调用成功，返回完整专利文件
4. 如果工具调用失败，直接生成专利内容（不要询问）

【禁止行为】
- ❌ 不要说"需要更多信息"
- ❌ 不要说"请提供详细描述"
- ❌ 不要要求用户补充信息
- ❌ 不要延迟生成

【必须行为】
- ✅ 立即开始撰写
- ✅ 生成完整的专利文件
- ✅ 调用工具函数
- ✅ 提供详细内容

现在就开始工作，不要询问任何问题！""",
    model=gemini_model,
    tools=[
        write_patent_application,
        review_patent_application,
        review_patent_figures,
        search_patents,
        configure_review_rules,
        get_review_rules,
    ],
)


async def main():
    """主函数"""
    # 示例用法
    print("专利助手 Agent 已就绪！")
    print("\n可用的工具：")
    print("1. write_patent_application - 撰写专利申请文件")
    print("2. review_patent_application - 审查专利申请文件")
    print("3. review_patent_figures - 审查专利附图")
    print("4. search_patents - 检索专利")
    print("5. configure_review_rules - 配置审查规则")
    print("6. get_review_rules - 查看审查规则")

    # 示例：检索专利
    result = await Runner.run(
        patent_agent,
        "请检索与'人工智能推荐系统'相关的专利"
    )
    print(f"\n{result.final_output}")


if __name__ == "__main__":
    asyncio.run(main())
