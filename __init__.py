"""
专利撰写和审查 Agent 系统

这是一个基于 OpenAI Agents SDK 的专利工作流系统，支持：
- 专利撰写
- 专利预审
- 附图审查
- 专利检索
- 可配置的审查规则
"""

from .main_agent import patent_agent
from .tools import PatentSearchTool, PatentWriter, PatentPreReviewer, PatentFigureReviewer
from .config import RuleManager
from .schemas import PatentApplication, PatentDraftRequest, PatentSearchQuery

__all__ = [
    "patent_agent",
    "PatentSearchTool",
    "PatentWriter",
    "PatentPreReviewer",
    "PatentFigureReviewer",
    "RuleManager",
    "PatentApplication",
    "PatentDraftRequest",
    "PatentSearchQuery",
]

__version__ = "1.0.0"
