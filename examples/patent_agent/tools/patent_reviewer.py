"""
专利审查工具

实现专利预审和附图审查功能
"""

import sys
import os
from typing import List, Dict, Any, Optional
import re
from datetime import datetime

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from schemas.patent_schemas import (
    PatentApplication,
    ReviewResult,
    ReviewIssue,
    PatentFigure,
    ReviewResultStatus,
)
from config.review_rules import RuleManager, ReviewSeverity


class PatentPreReviewer:
    """专利预审工具"""

    def __init__(self, rule_manager: RuleManager):
        self.rule_manager = rule_manager

    async def review_application(
        self,
        application: PatentApplication,
        custom_rules: Optional[Dict[str, Any]] = None
    ) -> ReviewResult:
        """
        审查专利申请文件

        Args:
            application: 专利申请文件
            custom_rules: 自定义审查规则

        Returns:
            审查结果
        """
        issues = []
        rules = self.rule_manager.get_enabled_rules("pre_review")

        # 应用自定义规则（如果提供）
        if custom_rules:
            # TODO: 应用自定义规则逻辑
            pass

        # 执行规则检查
        for rule in rules:
            rule_issues = self._check_rule(rule, application)
            issues.extend(rule_issues)

        # 计算总体评分
        score = self._calculate_score(issues)

        # 确定审查状态
        status = self._determine_status(issues)

        return ReviewResult(
            application_id=application.application_number or "N/A",
            review_type="pre_review",
            status=status,
            issues=issues,
            score=score,
            reviewer_notes=None,
        )

    def _check_rule(self, rule, application: PatentApplication) -> List[ReviewIssue]:
        """检查单个规则"""
        issues = []
        check_logic = rule.check_logic
        check_type = check_logic.get("type")

        try:
            if check_type == "length":
                field = check_logic.get("field")
                min_length = check_logic.get("min", 0)
                max_length = check_logic.get("max", float('inf'))

                field_value = getattr(application, field, "")
                if isinstance(field_value, str):
                    length = len(field_value)
                    if length < min_length or length > max_length:
                        issues.append(ReviewIssue(
                            rule_id=rule.rule_id,
                            issue_type="长度不符合要求",
                            severity=rule.severity.value,
                            message=f"{field}长度应为{min_length}-{max_length}字符，当前为{length}字符",
                            location=field,
                            suggestion=f"请调整{field}的长度至{min_length}-{max_length}字符之间"
                        ))

            elif check_type == "required":
                field = check_logic.get("field")
                min_length = check_logic.get("min_length", 1)

                field_value = getattr(application, field, "")
                if not field_value or len(field_value.strip()) < min_length:
                    issues.append(ReviewIssue(
                        rule_id=rule.rule_id,
                        issue_type="必填字段缺失",
                        severity=rule.severity.value,
                        message=f"{field}为必填字段，且长度不少于{min_length}字符",
                        location=field,
                        suggestion=f"请填写{field}，内容不少于{min_length}字符"
                    ))

            elif check_type == "compound":
                required_fields = check_logic.get("required_fields", [])
                min_length = check_logic.get("min_length", 0)

                missing_fields = []
                total_length = 0

                for field in required_fields:
                    field_value = getattr(application, field, "")
                    if not field_value or len(field_value.strip()) < 1:
                        missing_fields.append(field)
                    else:
                        total_length += len(field_value)

                if missing_fields:
                    issues.append(ReviewIssue(
                        rule_id=rule.rule_id,
                        issue_type="复合字段检查失败",
                        severity=rule.severity.value,
                        message=f"缺少必填字段：{', '.join(missing_fields)}",
                        location=", ".join(missing_fields),
                        suggestion=f"请填写以下字段：{', '.join(missing_fields)}"
                    ))

                if total_length < min_length:
                    issues.append(ReviewIssue(
                        rule_id=rule.rule_id,
                        issue_type="内容长度不足",
                        severity=rule.severity.value,
                        message=f"相关内容总长度不足{min_length}字符",
                        suggestion="请增加更多详细内容"
                    ))

            elif check_type == "claims":
                min_count = check_logic.get("min_count", 1)
                max_count = check_logic.get("max_count", 50)
                require_independent = check_logic.get("require_independent", False)

                claims = application.claims
                claim_count = len(claims)

                if claim_count < min_count:
                    issues.append(ReviewIssue(
                        rule_id=rule.rule_id,
                        issue_type="权利要求数量不足",
                        severity=rule.severity.value,
                        message=f"权利要求数量不足，最少需要{min_count}项",
                        suggestion="请增加权利要求项"
                    ))
                elif claim_count > max_count:
                    issues.append(ReviewIssue(
                        rule_id=rule.rule_id,
                        issue_type="权利要求数量过多",
                        severity=rule.severity.value,
                        message=f"权利要求数量超过{max_count}项，建议精简",
                        suggestion="请精简权利要求"
                    ))

                if require_independent:
                    has_independent = any(c.claim_type == "独立权利要求" for c in claims)
                    if not has_independent:
                        issues.append(ReviewIssue(
                            rule_id=rule.rule_id,
                            issue_type="缺少独立权利要求",
                            severity=rule.severity.value,
                            message="缺少独立权利要求",
                            suggestion="请至少添加一项独立权利要求"
                        ))

            elif check_type == "figure_reference":
                required = check_logic.get("required", False)

                if required and not application.figures:
                    issues.append(ReviewIssue(
                        rule_id=rule.rule_id,
                        issue_type="缺少附图",
                        severity=rule.severity.value,
                        message="申请文件缺少必要的附图",
                        suggestion="请添加相应的附图"
                    ))

        except Exception as e:
            issues.append(ReviewIssue(
                rule_id=rule.rule_id,
                issue_type="规则检查异常",
                severity=ReviewSeverity.ERROR.value,
                message=f"检查规则 {rule.rule_id} 时发生异常：{str(e)}",
                suggestion="请检查规则配置"
            ))

        return issues

    def _calculate_score(self, issues: List[ReviewIssue]) -> float:
        """计算审查评分"""
        if not issues:
            return 100.0

        # 基础分数
        score = 100.0

        # 根据问题严重程度扣分
        for issue in issues:
            if issue.severity == "error":
                score -= 10
            elif issue.severity == "warning":
                score -= 5
            else:  # info
                score -= 2

        # 确保分数不低于0
        return max(score, 0.0)

    def _determine_status(self, issues: List[ReviewIssue]) -> ReviewResultStatus:
        """确定审查状态"""
        errors = [i for i in issues if i.severity == "error"]
        warnings = [i for i in issues if i.severity == "warning"]

        if errors:
            return ReviewResultStatus.FAIL
        elif warnings:
            return ReviewResultStatus.WARNING
        else:
            return ReviewResultStatus.PASS

    def generate_review_report(self, result: ReviewResult, application: PatentApplication) -> str:
        """
        生成审查报告

        Args:
            result: 审查结果
            application: 专利申请

        Returns:
            审查报告文本
        """
        report = f"专利预审报告\n"
        report += f"{'='*50}\n\n"

        # 基本信息
        report += f"申请号：{result.application_id}\n"
        report += f"发明名称：{application.title}\n"
        report += f"申请人：{application.applicant.name}\n"
        report += f"审查时间：{result.reviewed_at.strftime('%Y-%m-%d %H:%M:%S')}\n\n"

        # 审查结果
        report += f"审查状态：{result.status.value}\n"
        report += f"综合评分：{result.score:.1f}/100\n\n"

        # 问题统计
        errors = [i for i in result.issues if i.severity == "error"]
        warnings = [i for i in result.issues if i.severity == "warning"]
        infos = [i for i in result.issues if i.severity == "info"]

        report += f"问题统计：\n"
        report += f"- 错误：{len(errors)} 个\n"
        report += f"- 警告：{len(warnings)} 个\n"
        report += f"- 提示：{len(infos)} 个\n\n"

        # 详细问题
        if result.issues:
            report += "详细问题：\n"
            report += f"{'-'*50}\n"

            for i, issue in enumerate(result.issues, 1):
                report += f"\n{i}. 【{issue.severity.upper()}】{issue.message}\n"
                report += f"   规则ID：{issue.rule_id}\n"
                report += f"   问题类型：{issue.issue_type}\n"
                if issue.location:
                    report += f"   位置：{issue.location}\n"
                if issue.suggestion:
                    report += f"   建议：{issue.suggestion}\n"
        else:
            report += "未发现问题，恭喜！\n"

        # 审查结论
        report += f"\n{'-'*50}\n"
        report += "审查结论：\n"
        if result.status == ReviewResultStatus.PASS:
            report += "申请文件符合要求，建议提交正式审查。\n"
        elif result.status == ReviewResultStatus.WARNING:
            report += "申请文件基本符合要求，但存在需要注意的问题，请参考上述建议进行修改。\n"
        else:
            report += "申请文件存在严重问题，必须修改后才能提交审查。\n"

        return report


class PatentFigureReviewer:
    """专利附图审查工具"""

    def __init__(self, rule_manager: RuleManager):
        self.rule_manager = rule_manager

    async def review_figures(
        self,
        figures: List[PatentFigure],
        application: Optional[PatentApplication] = None
    ) -> ReviewResult:
        """
        审查专利附图

        Args:
            figures: 附图列表
            application: 专利申请（用于交叉引用检查）

        Returns:
            审查结果
        """
        issues = []
        rules = self.rule_manager.get_enabled_rules("figure_review")

        # 执行规则检查
        for rule in rules:
            rule_issues = self._check_figure_rule(rule, figures, application)
            issues.extend(rule_issues)

        # 计算总体评分
        score = self._calculate_score(issues)

        # 确定审查状态
        status = self._determine_status(issues)

        return ReviewResult(
            application_id=application.application_number if application else "N/A",
            review_type="figure_review",
            status=status,
            issues=issues,
            score=score,
        )

    def _check_figure_rule(self, rule, figures: List[PatentFigure], application: Optional[PatentApplication] = None) -> List[ReviewIssue]:
        """检查附图规则"""
        issues = []
        check_logic = rule.check_logic
        check_type = check_logic.get("type")

        try:
            if check_type == "image_format":
                allowed_formats = check_logic.get("allowed_formats", [])
                max_size_mb = check_logic.get("max_size_mb", 10)

                for figure in figures:
                    if figure.file_format and figure.file_format.lower() not in allowed_formats:
                        issues.append(ReviewIssue(
                            rule_id=rule.rule_id,
                            issue_type="文件格式不符合要求",
                            severity=rule.severity.value,
                            message=f"图{figure.figure_number}格式为{figure.file_format}，不在允许的格式列表中：{', '.join(allowed_formats)}",
                            location=f"图{figure.figure_number}",
                            suggestion=f"请将图片转换为以下格式之一：{', '.join(allowed_formats)}"
                        ))

                    if figure.file_size_mb and figure.file_size_mb > max_size_mb:
                        issues.append(ReviewIssue(
                            rule_id=rule.rule_id,
                            issue_type="文件大小超标",
                            severity=rule.severity.value,
                            message=f"图{figure.figure_number}文件大小为{figure.file_size_mb}MB，超过了{max_size_mb}MB的限制",
                            location=f"图{figure.figure_number}",
                            suggestion=f"请压缩图片文件至{max_size_mb}MB以内"
                        ))

            elif check_type == "figure_number":
                required = check_logic.get("required", False)
                sequential = check_logic.get("sequential", False)

                if required and not figures:
                    issues.append(ReviewIssue(
                        rule_id=rule.rule_id,
                        issue_type="缺少附图",
                        severity=rule.severity.value,
                        message="申请文件缺少附图",
                        suggestion="请添加必要的附图"
                    ))
                    return issues

                if sequential:
                    expected_numbers = list(range(1, len(figures) + 1))
                    actual_numbers = sorted([f.figure_number for f in figures])

                    if expected_numbers != actual_numbers:
                        issues.append(ReviewIssue(
                            rule_id=rule.rule_id,
                            issue_type="图号不连续",
                            severity=rule.severity.value,
                            message=f"图号应连续编号，当前图号：{actual_numbers}",
                            suggestion="请按顺序重新编号附图"
                        ))

            elif check_type == "cross_reference":
                reference_type = check_logic.get("reference_type", "figure")
                bidirectional = check_logic.get("bidirectional", False)

                if not application:
                    return issues

                # 检查附图说明与附图的一致性
                brief_desc = application.brief_description.lower()

                figure_numbers = [f.figure_number for f in figures]
                referenced_figures = []

                # 简单的图号提取（查找"图X"或"Figure X"等模式）
                patterns = [r"图(\d+)", r"图\s*(\d+)", r"figure\s*(\d+)", r"Fig\.\s*(\d+)"]
                for pattern in patterns:
                    matches = re.findall(pattern, brief_desc, re.IGNORECASE)
                    referenced_figures.extend([int(m) for m in matches])

                # 去重并排序
                referenced_figures = sorted(list(set(referenced_figures)))

                if referenced_figures:
                    missing_figures = [num for num in referenced_figures if num not in figure_numbers]
                    if missing_figures:
                        issues.append(ReviewIssue(
                            rule_id=rule.rule_id,
                            issue_type="附图引用不完整",
                            severity=rule.severity.value,
                            message=f"附图说明中引用了图{missing_figures}，但未提供相应附图",
                            suggestion="请添加缺失的附图或修正附图说明"
                        ))

                    # 检查是否有未引用的附图
                    extra_figures = [num for num in figure_numbers if num not in referenced_figures]
                    if extra_figures and len(extra_figures) > len(figure_numbers) * 0.5:
                        issues.append(ReviewIssue(
                            rule_id=rule.rule_id,
                            issue_type="存在未引用的附图",
                            severity=rule.severity.value,
                            message=f"附图{extra_figures}在附图说明中未被引用",
                            suggestion="请在附图说明中引用这些附图"
                        ))

            elif check_type == "reference_marks":
                check_consistency = check_logic.get("check_consistency", False)

                if check_consistency and figures:
                    # 检查附图标记是否在说明书中出现
                    # 这里简化处理，实际应用中会更复杂
                    for figure in figures:
                        if not figure.description or len(figure.description.strip()) < 10:
                            issues.append(ReviewIssue(
                                rule_id=rule.rule_id,
                                issue_type="附图说明不完整",
                                severity=rule.severity.value,
                                message=f"图{figure.figure_number}的说明过于简单",
                                location=f"图{figure.figure_number}",
                                suggestion="请提供更详细的附图说明"
                            ))

        except Exception as e:
            issues.append(ReviewIssue(
                rule_id=rule.rule_id,
                issue_type="规则检查异常",
                severity=ReviewSeverity.ERROR.value,
                message=f"检查规则 {rule.rule_id} 时发生异常：{str(e)}",
                suggestion="请检查规则配置"
            ))

        return issues

    def _calculate_score(self, issues: List[ReviewIssue]) -> float:
        """计算审查评分"""
        if not issues:
            return 100.0

        score = 100.0

        for issue in issues:
            if issue.severity == "error":
                score -= 15  # 附图问题扣分更多
            elif issue.severity == "warning":
                score -= 8
            else:
                score -= 3

        return max(score, 0.0)

    def _determine_status(self, issues: List[ReviewIssue]) -> ReviewResultStatus:
        """确定审查状态"""
        errors = [i for i in issues if i.severity == "error"]
        warnings = [i for i in issues if i.severity == "warning"]

        if errors:
            return ReviewResultStatus.FAIL
        elif warnings:
            return ReviewResultStatus.WARNING
        else:
            return ReviewResultStatus.PASS

    def generate_review_report(self, result: ReviewResult, figures: List[PatentFigure]) -> str:
        """生成附图审查报告"""
        report = f"专利附图审查报告\n"
        report += f"{'='*50}\n\n"

        report += f"附图数量：{len(figures)}\n"
        report += f"审查时间：{result.reviewed_at.strftime('%Y-%m-%d %H:%M:%S')}\n\n"

        report += f"审查状态：{result.status.value}\n"
        report += f"综合评分：{result.score:.1f}/100\n\n"

        errors = [i for i in result.issues if i.severity == "error"]
        warnings = [i for i in result.issues if i.severity == "warning"]
        infos = [i for i in result.issues if i.severity == "info"]

        report += f"问题统计：\n"
        report += f"- 错误：{len(errors)} 个\n"
        report += f"- 警告：{len(warnings)} 个\n"
        report += f"- 提示：{len(infos)} 个\n\n"

        if result.issues:
            report += "详细问题：\n"
            report += f"{'-'*50}\n"

            for i, issue in enumerate(result.issues, 1):
                report += f"\n{i}. 【{issue.severity.upper()}】{issue.message}\n"
                if issue.suggestion:
                    report += f"   建议：{issue.suggestion}\n"
        else:
            report += "所有附图符合要求！\n"

        return report
