"""
专利撰写工具

根据需求自动生成专利申请文件
"""

import sys
import os
from typing import List, Optional
from datetime import datetime

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from schemas.patent_schemas import (
    PatentDraftRequest,
    PatentApplication,
    PatentType,
    ApplicantInfo,
    InventorInfo,
    PatentClaim,
    PatentFigure,
    ApplicationStatus,
)


class PatentWriter:
    """专利撰写工具"""

    def __init__(self):
        self.templates = self._load_templates()

    def _load_templates(self) -> dict:
        """加载撰写模板"""
        return {
            PatentType.INVENTION: {
                "structure": [
                    "技术领域",
                    "背景技术",
                    "发明内容",
                    "附图说明",
                    "具体实施方式",
                    "权利要求书"
                ],
                "min_length": {
                    "technical_field": 50,
                    "background_tech": 200,
                    "invention_content": 300,
                    "beneficial_effects": 100,
                    "brief_description": 100,
                }
            },
            PatentType.UTILITY_MODEL: {
                "structure": [
                    "技术领域",
                    "背景技术",
                    "实用新型内容",
                    "附图说明",
                    "具体实施方式",
                    "权利要求书"
                ],
                "min_length": {
                    "technical_field": 50,
                    "background_tech": 150,
                    "invention_content": 250,
                    "beneficial_effects": 100,
                    "brief_description": 80,
                }
            }
        }

    def generate_patent_application(
        self,
        request: PatentDraftRequest,
        applicant_info: Optional[ApplicantInfo] = None,
        inventor_info: Optional[List[InventorInfo]] = None,
    ) -> PatentApplication:
        """
        生成专利申请文件

        Args:
            request: 撰写请求
            applicant_info: 申请人信息（可选）
            inventor_info: 发明人信息（可选）

        Returns:
            专利申请文件
        """
        template = self.templates.get(
            request.patent_type,
            self.templates[PatentType.INVENTION]
        )

        # 生成技术领域
        technical_field = request.technical_field or self._generate_technical_field(
            request.invention_description
        )

        # 生成背景技术
        background_tech = request.background_info or self._generate_background_tech(
            technical_field, request.invention_description
        )

        # 生成发明内容
        invention_content = request.solution or self._generate_invention_content(
            request.invention_description,
            request.specific_problems,
            request.solution
        )

        # 生成有益效果
        beneficial_effects = request.beneficial_effects or self._generate_beneficial_effects(
            request.invention_description,
            request.solution
        )

        # 生成附图说明
        brief_description = self._generate_brief_description(
            request.invention_description
        )

        # 生成权利要求
        claims = self._generate_claims(
            request.invention_description,
            request.solution
        )

        # 使用默认申请人信息（如果未提供）
        if applicant_info is None:
            applicant_info = ApplicantInfo(
                name="待填写",
                address="待填写",
                country="中国",
            )

        # 使用默认发明人信息（如果未提供）
        if inventor_info is None:
            inventor_info = [
                InventorInfo(
                    name="待填写",
                    country="中国"
                )
            ]

        return PatentApplication(
            title=self._generate_title(request.invention_description),
            patent_type=request.patent_type,
            applicant=applicant_info,
            inventors=inventor_info,
            technical_field=technical_field,
            background_tech=background_tech,
            invention_content=invention_content,
            beneficial_effects=beneficial_effects,
            brief_description=brief_description,
            claims=claims,
            figures=[],  # 暂时为空，附图需要单独上传
            status=ApplicationStatus.DRAFT,
        )

    def _generate_title(self, description: str) -> str:
        """生成专利标题"""
        # 简单的标题生成逻辑
        # 实际应用中可能使用更复杂的 NLP 技术
        words = description.split()[:10]  # 取前10个词
        if len(words) < 5:
            return f"基于{description}的技术方案"

        # 生成一个简洁的标题
        if "方法" in description:
            return f"一种基于{description[:20]}的方法"
        elif "系统" in description or "装置" in description:
            return f"一种{description[:20]}系统"
        else:
            return f"一种{description[:15]}的技术方案"

    def _generate_technical_field(self, description: str) -> str:
        """生成技术领域"""
        # 分析描述中的技术关键词
        tech_keywords = []
        common_fields = {
            "人工智能": "人工智能技术领域",
            "机器学习": "机器学习技术领域",
            "深度学习": "深度学习技术领域",
            "数据": "数据处理技术领域",
            "算法": "算法技术领域",
            "网络": "网络技术领域",
            "图像": "图像处理技术领域",
            "语音": "语音处理技术领域",
            "自然语言": "自然语言处理技术领域",
        }

        for keyword, field in common_fields.items():
            if keyword in description:
                tech_keywords.append(field)

        if not tech_keywords:
            tech_keywords.append("计算机技术领域")

        return "、".join(tech_keywords)

    def _generate_background_tech(self, technical_field: str, description: str) -> str:
        """生成背景技术"""
        # 简化的背景技术生成
        bg_template = f"""
本发明涉及{technical_field}。

目前，该领域存在以下问题：
1. 现有技术方案在处理复杂场景时效率低下；
2. 传统的解决方法难以适应动态变化的需求；
3. 现有方案在准确性和稳定性方面有待提高。

因此，亟需一种新的技术方案来解决上述问题。
        """.strip()

        return bg_template

    def _generate_invention_content(
        self,
        description: str,
        problems: Optional[str] = None,
        solution: Optional[str] = None
    ) -> str:
        """生成发明内容"""
        content = f"为了解决上述问题，本发明提供以下技术方案：\n\n"

        if solution:
            content += f"{solution}\n\n"
        else:
            content += f"本发明提供一种基于{description[:30]}的技术方案，"
            content += "该方案包括以下主要步骤：\n"
            content += "1. 数据采集与预处理\n"
            content += "2. 特征提取与分析\n"
            content += "3. 模型训练与优化\n"
            content += "4. 结果输出与应用\n\n"

        if problems:
            content += f"本发明要解决的技术问题：{problems}\n\n"

        content += "本发明的技术方案具有以下特点：\n"
        content += "1. 高效性：采用优化的算法提高处理效率；\n"
        content += "2. 准确性：通过精细的模型设计提高准确性；\n"
        content += "3. 适应性：能够适应不同应用场景的需求。\n"

        return content

    def _generate_beneficial_effects(self, description: str, solution: Optional[str] = None) -> str:
        """生成有益效果"""
        effects = "与现有技术相比，本发明具有以下有益效果：\n\n"
        effects += "1. 提高了处理效率，相比传统方法提升30%以上；\n"
        effects += "2. 增强了系统的稳定性和可靠性；\n"
        effects += "3. 降低了资源消耗和成本；\n"
        effects += "4. 提高了用户体验和满意度。\n"

        if solution:
            effects += f"\n具体来说，本发明的{solution}能够有效解决现有技术中的关键问题。\n"

        return effects

    def _generate_brief_description(self, description: str) -> str:
        """生成附图简要说明"""
        return """
图1是本发明的整体架构图；
图2是本发明主要流程图；
图3是本发明核心模块示意图；
图4是本发明实施例效果图。
        """.strip()

    def _generate_claims(self, description: str, solution: Optional[str] = None) -> List[PatentClaim]:
        """生成权利要求书"""
        claims = []

        # 独立权利要求
        independent_claim = PatentClaim(
            claim_number=1,
            claim_type="独立权利要求",
            content="1. 一种基于" + description[:20] + "的技术方案，其特征在于，包括以下步骤："
                    "\n(1) 数据采集步骤；"
                    "\n(2) 数据处理步骤；"
                    "\n(3) 结果输出步骤。",
        )
        claims.append(independent_claim)

        # 从属权利要求
        dependent_claims = [
            PatentClaim(
                claim_number=2,
                claim_type="从属权利要求",
                content="2. 根据权利要求1所述的技术方案，其特征在于，所述数据采集步骤包括..."
            ),
            PatentClaim(
                claim_number=3,
                claim_type="从属权利要求",
                content="3. 根据权利要求1所述的技术方案，其特征在于，所述数据处理步骤包括..."
            ),
            PatentClaim(
                claim_number=4,
                claim_type="从属权利要求",
                content="4. 根据权利要求1所述的技术方案，其特征在于，所述结果输出步骤包括..."
            ),
        ]
        claims.extend(dependent_claims)

        return claims

    def format_application(self, application: PatentApplication) -> str:
        """
        格式化专利申请文件为文本

        Args:
            application: 专利申请文件

        Returns:
            格式化的专利申请文本
        """
        formatted = f"专利申请文件\n"
        formatted += f"{'='*50}\n\n"

        # 标题
        formatted += f"发明名称：{application.title}\n\n"

        # 申请人信息
        formatted += f"申请人：{application.applicant.name}\n"
        formatted += f"地址：{application.applicant.address}\n\n"

        # 发明人信息
        formatted += "发明人："
        for i, inventor in enumerate(application.inventors):
            if i > 0:
                formatted += "，"
            formatted += inventor.name
        formatted += "\n\n"

        # 技术领域
        formatted += f"技术领域\n"
        formatted += f"{application.technical_field}\n\n"

        # 背景技术
        formatted += "背景技术\n"
        formatted += f"{application.background_tech}\n\n"

        # 发明内容
        formatted += "发明内容\n"
        formatted += f"{application.invention_content}\n\n"

        # 有益效果
        formatted += "有益效果\n"
        formatted += f"{application.beneficial_effects}\n\n"

        # 附图说明
        formatted += "附图说明\n"
        formatted += f"{application.brief_description}\n\n"

        # 权利要求书
        formatted += "权利要求书\n"
        for claim in application.claims:
            formatted += f"{claim.content}\n\n"

        return formatted

    def export_to_xml(self, application: PatentApplication) -> str:
        """
        导出为 XML 格式（标准专利申请格式）

        Args:
            application: 专利申请文件

        Returns:
            XML 格式的申请文件
        """
        # 简化的 XML 格式
        xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<patent_application>
    <title>{application.title}</title>
    <patent_type>{application.patent_type}</patent_type>
    <applicant>
        <name>{application.applicant.name}</name>
        <address>{application.applicant.address}</address>
        <country>{application.applicant.country}</country>
    </applicant>
    <inventors>"""

        for inventor in application.inventors:
            xml += f"""
        <inventor>
            <name>{inventor.name}</name>
            <address>{inventor.address or ''}</address>
            <country>{inventor.country}</country>
        </inventor>"""

        xml += """
    </inventors>
    <technical_field>"""
        xml += application.technical_field
        xml += """
    </technical_field>
    <background_tech>"""
        xml += application.background_tech
        xml += """
    </background_tech>
    <invention_content>"""
        xml += application.invention_content
        xml += """
    </invention_content>
    <beneficial_effects>"""
        xml += application.beneficial_effects
        xml += """
    </beneficial_effects>
    <brief_description>"""
        xml += application.brief_description
        xml += """
    </brief_description>
    <claims>"""

        for claim in application.claims:
            xml += f"""
        <claim number="{claim.claim_number}" type="{claim.claim_type}">
            {claim.content}
        </claim>"""

        xml += """
    </claims>
</patent_application>"""

        return xml
