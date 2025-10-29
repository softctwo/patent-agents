"""
专利审查规则配置模块

该模块定义了可配置的专利审查规则，包括：
- 预审规则
- 附图审查规则
- 检索规则
"""

from typing import Dict, List, Any
from enum import Enum
from pydantic import BaseModel, Field


class ReviewSeverity(Enum):
    """审查严重程度"""
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


class ReviewRule(BaseModel):
    """单个审查规则"""
    rule_id: str = Field(description="规则唯一标识")
    name: str = Field(description="规则名称")
    description: str = Field(description="规则描述")
    category: str = Field(description="规则分类")
    severity: ReviewSeverity = Field(description="严重程度")
    enabled: bool = Field(default=True, description="是否启用")
    check_logic: Dict[str, Any] = Field(description="检查逻辑配置")


class PatentType(Enum):
    """专利类型"""
    INVENTION = "invention"  # 发明专利
    UTILITY_MODEL = "utility_model"  # 实用新型
    DESIGN = "design"  # 外观设计


class ReviewRuleConfig(BaseModel):
    """审查规则配置"""
    patent_type: PatentType = Field(description="专利类型")
    rules: List[ReviewRule] = Field(description="规则列表")
    version: str = Field(default="1.0.0", description="配置版本")


# 默认预审规则
DEFAULT_PRE_REVIEW_RULES = ReviewRuleConfig(
    patent_type=PatentType.INVENTION,
    rules=[
        ReviewRule(
            rule_id="PRE001",
            name="标题长度检查",
            description="检查专利标题长度是否符合要求（5-50字）",
            category="格式检查",
            severity=ReviewSeverity.WARNING,
            check_logic={
                "type": "length",
                "field": "title",
                "min": 5,
                "max": 50
            }
        ),
        ReviewRule(
            rule_id="PRE002",
            name="技术领域完整性",
            description="检查技术领域是否完整描述",
            category="内容完整性",
            severity=ReviewSeverity.ERROR,
            check_logic={
                "type": "required",
                "field": "technical_field",
                "min_length": 50
            }
        ),
        ReviewRule(
            rule_id="PRE003",
            name="背景技术检查",
            description="检查背景技术是否包含现有技术分析",
            category="内容质量",
            severity=ReviewSeverity.ERROR,
            check_logic={
                "type": "required",
                "field": "background_tech",
                "min_length": 100
            }
        ),
        ReviewRule(
            rule_id="PRE004",
            name="发明内容检查",
            description="检查发明内容是否包含技术方案和有益效果",
            category="内容完整性",
            severity=ReviewSeverity.ERROR,
            check_logic={
                "type": "compound",
                "required_fields": ["invention_content", "beneficial_effects"],
                "min_length": 200
            }
        ),
        ReviewRule(
            rule_id="PRE005",
            name="权利要求书检查",
            description="检查权利要求书格式和数量",
            category="格式检查",
            severity=ReviewSeverity.ERROR,
            check_logic={
                "type": "claims",
                "min_count": 1,
                "max_count": 20,
                "require_independent": True
            }
        ),
        ReviewRule(
            rule_id="PRE006",
            name="附图说明检查",
            description="检查是否有相应的附图说明",
            category="格式检查",
            severity=ReviewSeverity.WARNING,
            check_logic={
                "type": "figure_reference",
                "required": True
            }
        ),
    ]
)

# 默认附图审查规则
DEFAULT_FIGURE_REVIEW_RULES = ReviewRuleConfig(
    patent_type=PatentType.INVENTION,
    rules=[
        ReviewRule(
            rule_id="FIG001",
            name="图片清晰度检查",
            description="检查图片分辨率是否符合要求（≥300 DPI）",
            category="图片质量",
            severity=ReviewSeverity.ERROR,
            check_logic={
                "type": "image_quality",
                "min_dpi": 300,
                "check_sharpness": True
            }
        ),
        ReviewRule(
            rule_id="FIG002",
            name="图片格式检查",
            description="检查图片格式是否符合要求",
            category="格式检查",
            severity=ReviewSeverity.ERROR,
            check_logic={
                "type": "image_format",
                "allowed_formats": ["png", "jpg", "tiff"],
                "max_size_mb": 10
            }
        ),
        ReviewRule(
            rule_id="FIG003",
            name="图号标注检查",
            description="检查图片是否正确标注图号",
            category="格式检查",
            severity=ReviewSeverity.WARNING,
            check_logic={
                "type": "figure_number",
                "required": True,
                "sequential": True
            }
        ),
        ReviewRule(
            rule_id="FIG004",
            name="附图引用检查",
            description="检查说明书中的附图引用是否一致",
            category="一致性检查",
            severity=ReviewSeverity.ERROR,
            check_logic={
                "type": "cross_reference",
                "reference_type": "figure",
                "bidirectional": True
            }
        ),
        ReviewRule(
            rule_id="FIG005",
            name="附图标记检查",
            description="检查附图标记是否清晰且在说明书中已说明",
            category="内容检查",
            severity=ReviewSeverity.WARNING,
            check_logic={
                "type": "reference_marks",
                "check_consistency": True
            }
        ),
    ]
)

# 检索规则配置
DEFAULT_SEARCH_RULES = {
    "engines": [
        {
            "name": "cnipa",
            "description": "中国专利数据库",
            "enabled": True,
            "weight": 0.5
        },
        {
            "name": "google_patents",
            "description": "Google Patents",
            "enabled": True,
            "weight": 0.3
        },
        {
            "name": "espacenet",
            "description": "欧洲专利数据库",
            "enabled": True,
            "weight": 0.2
        }
    ],
    "relevance_threshold": 0.7,
    "max_results_per_engine": 50,
    "min_similarity_score": 0.6,
    "analysis_depth": "comprehensive"  # basic, standard, comprehensive
}


class RuleManager:
    """规则管理器"""

    def __init__(self):
        self.pre_review_rules = DEFAULT_PRE_REVIEW_RULES
        self.figure_review_rules = DEFAULT_FIGURE_REVIEW_RULES
        self.search_rules = DEFAULT_SEARCH_RULES

    def load_custom_rules(self, config_path: str):
        """从文件加载自定义规则"""
        # TODO: 实现从 JSON/YAML 文件加载规则
        pass

    def add_rule(self, rule_type: str, rule: ReviewRule):
        """添加新规则"""
        if rule_type == "pre_review":
            self.pre_review_rules.rules.append(rule)
        elif rule_type == "figure_review":
            self.figure_review_rules.rules.append(rule)

    def remove_rule(self, rule_type: str, rule_id: str):
        """删除规则"""
        if rule_type == "pre_review":
            self.pre_review_rules.rules = [
                r for r in self.pre_review_rules.rules if r.rule_id != rule_id
            ]
        elif rule_type == "figure_review":
            self.figure_review_rules.rules = [
                r for r in self.figure_review_rules.rules if r.rule_id != rule_id
            ]

    def enable_rule(self, rule_type: str, rule_id: str, enabled: bool = True):
        """启用/禁用规则"""
        for rule in self.get_rules(rule_type):
            if rule.rule_id == rule_id:
                rule.enabled = enabled
                break

    def get_rules(self, rule_type: str) -> List[ReviewRule]:
        """获取规则列表"""
        if rule_type == "pre_review":
            return self.pre_review_rules.rules
        elif rule_type == "figure_review":
            return self.figure_review_rules.rules
        return []

    def get_enabled_rules(self, rule_type: str) -> List[ReviewRule]:
        """获取启用的规则"""
        return [r for r in self.get_rules(rule_type) if r.enabled]
