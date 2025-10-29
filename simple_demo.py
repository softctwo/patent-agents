"""
简化的专利 agent 演示（无需 OpenAI API 密钥）

直接展示工具功能，不依赖外部 API
"""

import asyncio
import sys
import os

# 添加当前目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

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


def demo_patent_writer():
    """演示专利撰写功能"""
    print("=" * 60)
    print("演示1：专利撰写工具")
    print("=" * 60)

    writer = PatentWriter()

    # 创建撰写请求
    request = PatentDraftRequest(
        invention_description="一种基于深度学习的智能推荐系统，通过神经网络分析用户行为数据，实现个性化推荐",
        technical_field="人工智能、机器学习、数据挖掘",
        patent_type=PatentType.INVENTION,
    )

    # 生成专利申请文件
    application = writer.generate_patent_application(request)

    # 格式化输出
    formatted = writer.format_application(application)

    print("生成的专利申请文件：")
    print(formatted)
    print("\n" + "=" * 60 + "\n")


def demo_patent_search():
    """演示专利检索功能"""
    print("=" * 60)
    print("演示2：专利检索工具")
    print("=" * 60)

    search_tool = PatentSearchTool()

    # 创建检索查询
    query = PatentSearchQuery(
        keywords=["人工智能", "推荐系统", "机器学习"],
        patent_types=[PatentType.INVENTION],
        applicant="清华大学",
    )

    # 执行检索
    result = asyncio.run(search_tool.search_patents(query))

    print(f"检索关键词：{', '.join(query.keywords)}")
    print(f"总结果数：{result.total_results}")
    print(f"高相关度：{result.high_relevance_count} 篇")
    print(f"中相关度：{result.medium_relevance_count} 篇")
    print(f"低相关度：{result.low_relevance_count} 篇")

    print("\n主要检索结果：")
    for i, patent in enumerate(result.results[:3], 1):
        print(f"\n{i}. {patent.title}")
        print(f"   申请人：{patent.applicant}")
        print(f"   相似度：{patent.similarity_score:.2f}")
        if patent.abstract:
            print(f"   摘要：{patent.abstract[:100]}...")

    print("\n" + "=" * 60 + "\n")


def demo_patent_pre_review():
    """演示专利预审功能"""
    print("=" * 60)
    print("演示3：专利预审工具")
    print("=" * 60)

    rule_manager = RuleManager()
    pre_reviewer = PatentPreReviewer(rule_manager)

    # 创建一个不完整的专利申请（故意有问题）
    incomplete_application = PatentApplication(
        title="一种方法",  # 标题太短，应该会触发警告
        patent_type=PatentType.INVENTION,
        applicant=ApplicantInfo(name="某公司", address="地址", country="中国"),
        inventors=[],
        technical_field="",  # 技术领域为空，会触发错误
        background_tech="背景技术",  # 内容太短
        invention_content="发明内容",  # 内容太短
        beneficial_effects="有益效果",
        brief_description="附图说明",
        claims=[],  # 缺少权利要求，会触发错误
        status=ApplicationStatus.DRAFT,
    )

    # 执行预审
    result = asyncio.run(pre_reviewer.review_application(incomplete_application))

    print(f"审查状态：{result.status.value}")
    print(f"综合评分：{result.score:.1f}/100")
    print(f"发现问题数量：{len(result.issues)}")

    print("\n发现的问题：")
    for i, issue in enumerate(result.issues[:5], 1):
        print(f"\n{i}. 【{issue.severity.upper()}】{issue.message}")
        if issue.suggestion:
            print(f"   建议：{issue.suggestion}")

    print("\n" + "=" * 60 + "\n")


def demo_figure_review():
    """演示附图审查功能"""
    print("=" * 60)
    print("演示4：附图审查工具")
    print("=" * 60)

    rule_manager = RuleManager()
    figure_reviewer = PatentFigureReviewer(rule_manager)

    # 创建附图列表
    figures = [
        PatentFigure(
            figure_number=1,
            figure_type="架构图",
            description="系统整体架构示意图",
            dpi=300,
            file_format="png",
            file_size_mb=2.5,
        ),
        PatentFigure(
            figure_number=2,
            figure_type="流程图",
            description="算法执行流程图",
            dpi=200,  # DPI 不够，会触发错误
            file_format="pdf",  # 不支持的格式，会触发错误
            file_size_mb=1.5,
        ),
        PatentFigure(
            figure_number=3,
            figure_type="示意图",
            description="用户界面示意图",
            dpi=300,
            file_format="png",
            file_size_mb=2.0,
        ),
    ]

    # 执行附图审查
    result = asyncio.run(figure_reviewer.review_figures(figures))

    print(f"审查状态：{result.status.value}")
    print(f"综合评分：{result.score:.1f}/100")
    print(f"发现问题数量：{len(result.issues)}")

    print("\n发现的问题：")
    for i, issue in enumerate(result.issues, 1):
        print(f"\n{i}. 【{issue.severity.upper()}】{issue.message}")
        if issue.suggestion:
            print(f"   建议：{issue.suggestion}")

    print("\n" + "=" * 60 + "\n")


def demo_rule_manager():
    """演示规则管理器"""
    print("=" * 60)
    print("演示5：审查规则配置")
    print("=" * 60)

    rule_manager = RuleManager()

    # 显示预审规则
    print("预审规则：")
    print("-" * 40)
    for rule in rule_manager.get_rules("pre_review"):
        status = "✓ 已启用" if rule.enabled else "✗ 已禁用"
        print(f"[{status}] {rule.rule_id}: {rule.name}")
        print(f"   严重程度：{rule.severity.value}")

    print("\n附图审查规则：")
    print("-" * 40)
    for rule in rule_manager.get_rules("figure_review"):
        status = "✓ 已启用" if rule.enabled else "✗ 已禁用"
        print(f"[{status}] {rule.rule_id}: {rule.name}")
        print(f"   严重程度：{rule.severity.value}")

    print("\n" + "=" * 60 + "\n")


def demo_comprehensive_workflow():
    """演示完整工作流"""
    print("=" * 60)
    print("演示6：完整专利工作流")
    print("=" * 60)

    # 1. 撰写专利
    print("步骤1：撰写专利申请文件")
    writer = PatentWriter()
    request = PatentDraftRequest(
        invention_description="一种基于区块链的分布式身份认证系统，通过智能合约管理身份信息，使用零知识证明保护隐私",
        technical_field="区块链、身份认证、分布式系统",
        patent_type=PatentType.INVENTION,
    )
    application = writer.generate_patent_application(request)
    print(f"✓ 已生成专利申请文件：{application.title}")

    # 2. 预审
    print("\n步骤2：执行专利预审")
    rule_manager = RuleManager()
    pre_reviewer = PatentPreReviewer(rule_manager)
    review_result = asyncio.run(pre_reviewer.review_application(application))
    print(f"✓ 预审完成，状态：{review_result.status.value}，评分：{review_result.score:.1f}/100")

    # 3. 检索现有技术
    print("\n步骤3：检索现有技术")
    search_tool = PatentSearchTool()
    search_query = PatentSearchQuery(
        keywords=["区块链", "身份认证", "分布式"],
        patent_types=[PatentType.INVENTION],
    )
    search_result = asyncio.run(search_tool.search_patents(search_query))
    print(f"✓ 检索完成，共找到 {search_result.total_results} 篇相关专利")

    # 4. 附图审查
    print("\n步骤4：审查专利附图")
    figures = [
        PatentFigure(figure_number=1, figure_type="架构图", description="系统架构图", dpi=300, file_format="png", file_size_mb=2.0),
        PatentFigure(figure_number=2, figure_type="流程图", description="认证流程图", dpi=300, file_format="png", file_size_mb=2.0),
    ]
    figure_reviewer = PatentFigureReviewer(rule_manager)
    figure_result = asyncio.run(figure_reviewer.review_figures(figures))
    print(f"✓ 附图审查完成，状态：{figure_result.status.value}，评分：{figure_result.score:.1f}/100")

    print("\n工作流总结：")
    print(f"- 专利撰写：✓")
    print(f"- 专利预审：✓ ({len(review_result.issues)} 个问题)")
    print(f"- 现有技术检索：✓ ({search_result.total_results} 篇)")
    print(f"- 附图审查：✓ ({len(figure_result.issues)} 个问题)")

    print("\n" + "=" * 60 + "\n")


def main():
    """主演示函数"""
    print("\n" + "=" * 60)
    print("专利撰写和审查系统演示（独立版本）")
    print("=" * 60)
    print("\n本演示将展示专利 agent 的各项功能：\n")
    print("1. 专利撰写工具")
    print("2. 专利检索工具")
    print("3. 专利预审工具")
    print("4. 附图审查工具")
    print("5. 规则配置管理")
    print("6. 完整工作流")
    print("\n" + "=" * 60 + "\n")

    try:
        demo_patent_writer()
    except Exception as e:
        print(f"演示1出错：{e}\n")

    try:
        demo_patent_search()
    except Exception as e:
        print(f"演示2出错：{e}\n")

    try:
        demo_patent_pre_review()
    except Exception as e:
        print(f"演示3出错：{e}\n")

    try:
        demo_figure_review()
    except Exception as e:
        print(f"演示4出错：{e}\n")

    try:
        demo_rule_manager()
    except Exception as e:
        print(f"演示5出错：{e}\n")

    try:
        demo_comprehensive_workflow()
    except Exception as e:
        print(f"演示6出错：{e}\n")

    print("\n" + "=" * 60)
    print("演示结束")
    print("=" * 60)


if __name__ == "__main__":
    main()
