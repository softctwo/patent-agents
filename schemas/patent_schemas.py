"""
专利相关的数据模型

定义专利申请、审查结果等数据结构
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum


class PatentType(str, Enum):
    """专利类型"""
    INVENTION = "invention"  # 发明专利
    UTILITY_MODEL = "utility_model"  # 实用新型
    DESIGN = "design"  # 外观设计


class ApplicationStatus(str, Enum):
    """申请状态"""
    DRAFT = "draft"  # 草稿
    UNDER_REVIEW = "under_review"  # 审查中
    APPROVED = "approved"  # 批准
    REJECTED = "rejected"  # 拒绝
    PENDING = "pending"  # 待审


class ReviewResultStatus(str, Enum):
    """审查结果状态"""
    PASS = "pass"  # 通过
    FAIL = "fail"  # 不通过
    WARNING = "warning"  # 警告
    INFO = "info"  # 提示


class ApplicantInfo(BaseModel):
    """申请人信息"""
    name: str = Field(description="申请人姓名/名称")
    address: str = Field(description="地址")
    country: str = Field(description="国家")
    email: Optional[str] = Field(default=None, description="邮箱")
    phone: Optional[str] = Field(default=None, description="电话")


class InventorInfo(BaseModel):
    """发明人信息"""
    name: str = Field(description="发明人姓名")
    address: Optional[str] = Field(default=None, description="地址")
    country: str = Field(description="国家")


class PatentClaim(BaseModel):
    """专利权利要求"""
    claim_number: int = Field(description="权利要求号")
    claim_type: str = Field(description="权利要求类型（独立/从属）")
    content: str = Field(description="权利要求内容")
    depends_on: Optional[List[int]] = Field(default=None, description="依附的权利要求号")


class PatentFigure(BaseModel):
    """专利附图"""
    figure_number: int = Field(description="图号")
    figure_type: str = Field(description="图类型（流程图、结构图等）")
    file_path: Optional[str] = Field(default=None, description="文件路径")
    description: str = Field(description="附图说明")
    dpi: Optional[int] = Field(default=None, description="分辨率")
    file_format: Optional[str] = Field(default=None, description="文件格式")
    file_size_mb: Optional[float] = Field(default=None, description="文件大小（MB）")


class PatentApplication(BaseModel):
    """专利申请文件"""
    title: str = Field(description="专利标题")
    patent_type: PatentType = Field(description="专利类型")
    application_number: Optional[str] = Field(default=None, description="申请号")
    application_date: Optional[datetime] = Field(default=None, description="申请日期")

    # 申请人信息
    applicant: ApplicantInfo = Field(description="申请人")
    inventors: List[InventorInfo] = Field(description="发明人列表")

    # 技术内容
    technical_field: str = Field(description="技术领域")
    background_tech: str = Field(description="背景技术")
    invention_content: str = Field(description="发明内容")
    beneficial_effects: str = Field(description="有益效果")
    brief_description: str = Field(description="附图简要说明")

    # 权利要求
    claims: List[PatentClaim] = Field(description="权利要求列表")

    # 附图
    figures: List[PatentFigure] = Field(default_factory=list, description="附图列表")

    # 元数据
    status: ApplicationStatus = Field(default=ApplicationStatus.DRAFT)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class ReviewIssue(BaseModel):
    """审查问题"""
    rule_id: str = Field(description="触发的规则ID")
    issue_type: str = Field(description="问题类型")
    severity: str = Field(description="严重程度")
    message: str = Field(description="问题描述")
    location: Optional[str] = Field(default=None, description="问题位置")
    suggestion: Optional[str] = Field(default=None, description="修改建议")


class ReviewResult(BaseModel):
    """审查结果"""
    application_id: str = Field(description="申请ID")
    review_type: str = Field(description="审查类型（pre_review/figure_review/search）")
    status: ReviewResultStatus = Field(description="审查状态")
    issues: List[ReviewIssue] = Field(default_factory=list, description="发现的问题")
    score: Optional[float] = Field(default=None, description="综合评分（0-100）")
    reviewed_at: datetime = Field(default_factory=datetime.now)
    reviewer_notes: Optional[str] = Field(default=None, description="审查员备注")


class PatentSearchQuery(BaseModel):
    """专利检索查询"""
    keywords: List[str] = Field(description="关键词列表")
    patent_types: Optional[List[PatentType]] = Field(default=None, description="专利类型筛选")
    date_range: Optional[tuple] = Field(default=None, description="日期范围")
    applicant: Optional[str] = Field(default=None, description="申请人筛选")
    inventor: Optional[str] = Field(default=None, description="发明人筛选")
    classification_codes: Optional[List[str]] = Field(default=None, description="分类号筛选")


class PatentSearchResult(BaseModel):
    """专利检索结果"""
    patent_id: str = Field(description="专利ID")
    title: str = Field(description="专利标题")
    patent_number: Optional[str] = Field(default=None, description="专利号")
    application_number: Optional[str] = Field(default=None, description="申请号")
    applicant: str = Field(description="申请人")
    inventors: List[str] = Field(description="发明人列表")
    application_date: Optional[datetime] = Field(default=None, description="申请日期")
    publication_date: Optional[datetime] = Field(default=None, description="公开日期")
    abstract: Optional[str] = Field(default=None, description="摘要")
    classification_codes: List[str] = Field(default_factory=list, description="分类号")
    similarity_score: Optional[float] = Field(default=None, description="相似度分数（0-1）")
    relevance_explanation: Optional[str] = Field(default=None, description="相关性说明")
    url: Optional[str] = Field(default=None, description="原文链接")


class PatentSearchReport(BaseModel):
    """专利检索报告"""
    query: PatentSearchQuery = Field(description="检索查询")
    results: List[PatentSearchResult] = Field(description="检索结果")
    total_results: int = Field(description="总结果数")
    high_relevance_count: int = Field(description="高相关度结果数")
    medium_relevance_count: int = Field(description="中相关度结果数")
    low_relevance_count: int = Field(description="低相关度结果数")
    analysis: Optional[str] = Field(default=None, description="检索分析")
    novelty_analysis: Optional[str] = Field(default=None, description="新颖性分析")
    similarity_analysis: Optional[str] = Field(default=None, description="相似性分析")
    recommendations: List[str] = Field(default_factory=list, description="建议")
    generated_at: datetime = Field(default_factory=datetime.now)


class PatentDraftRequest(BaseModel):
    """专利撰写请求"""
    invention_description: str = Field(description="发明描述")
    technical_field: str = Field(description="技术领域")
    background_info: Optional[str] = Field(default=None, description="背景信息")
    specific_problems: Optional[str] = Field(default=None, description="要解决的技术问题")
    solution: Optional[str] = Field(default=None, description="技术解决方案")
    beneficial_effects: Optional[str] = Field(default=None, description="有益效果")
    reference_materials: Optional[List[str]] = Field(default=None, description="参考材料")
    patent_type: PatentType = Field(default=PatentType.INVENTION, description="专利类型")
    language: str = Field(default="zh", description="撰写语言")


class PatentWorkflowRequest(BaseModel):
    """专利工作流请求"""
    request_type: str = Field(description="请求类型（draft/review/figure_review/search）")
    application_data: Optional[PatentApplication] = Field(default=None, description="专利申请数据")
    draft_request: Optional[PatentDraftRequest] = Field(default=None, description="撰写请求")
    figures: Optional[List[PatentFigure]] = Field(default=None, description="附图列表")
    search_query: Optional[PatentSearchQuery] = Field(default=None, description="检索查询")
    custom_rules: Optional[Dict[str, Any]] = Field(default=None, description="自定义审查规则")
