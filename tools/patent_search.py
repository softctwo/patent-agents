"""
专利检索工具

实现专利检索功能，支持多个专利数据库
"""

import asyncio
import sys
import os
from typing import List, Dict, Any, Optional
from datetime import datetime
import json
import re

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from schemas.patent_schemas import (
    PatentSearchQuery,
    PatentSearchResult,
    PatentSearchReport,
    PatentType,
)


class PatentSearchEngine:
    """专利搜索引擎基类"""

    def __init__(self, name: str, weight: float = 1.0):
        self.name = name
        self.weight = weight

    async def search(self, query: PatentSearchQuery) -> List[PatentSearchResult]:
        """执行检索"""
        raise NotImplementedError

    def calculate_similarity(self, patent: PatentSearchResult, query: PatentSearchQuery) -> float:
        """计算相似度"""
        # 简单的关键词匹配算法
        score = 0.0
        total_keywords = len(query.keywords)

        if total_keywords == 0:
            return 0.0

        # 在标题中查找关键词
        title_lower = patent.title.lower()
        for keyword in query.keywords:
            if keyword.lower() in title_lower:
                score += 0.3

        # 在摘要中查找关键词
        if patent.abstract:
            abstract_lower = patent.abstract.lower()
            for keyword in query.keywords:
                if keyword.lower() in abstract_lower:
                    score += 0.2

        # 在申请人中查找
        if query.applicant:
            if query.applicant.lower() in patent.applicant.lower():
                score += 0.1

        return min(score, 1.0)


class CNIPASearchEngine(PatentSearchEngine):
    """中国专利数据库检索引擎"""

    def __init__(self):
        super().__init__("cnipa", 0.5)

    async def search(self, query: PatentSearchQuery) -> List[PatentSearchResult]:
        """
        模拟 CNIPA 检索
        在实际应用中，这里会调用真实的 CNIPA API
        """
        # 模拟数据
        mock_results = [
            {
                "patent_id": f"CN{2024000001}",
                "title": "基于人工智能的智能推荐系统及其方法",
                "patent_number": f"CN20241000001",
                "applicant": "清华大学",
                "inventors": ["张三", "李四"],
                "application_date": datetime(2024, 1, 15),
                "publication_date": datetime(2024, 8, 20),
                "abstract": "本发明涉及一种基于深度学习的智能推荐系统，包括数据采集模块、特征提取模块、模型训练模块和推荐生成模块...",
                "classification_codes": ["G06N3/08", "G06Q30/06"],
            },
            {
                "patent_id": f"CN{2024000002}",
                "title": "一种机器学习模型优化方法及系统",
                "patent_number": f"CN20241000002",
                "applicant": "北京大学",
                "inventors": ["王五", "赵六"],
                "application_date": datetime(2024, 2, 10),
                "publication_date": datetime(2024, 9, 15),
                "abstract": "本发明公开了一种机器学习模型训练优化方法，通过自适应学习率调整和梯度裁剪技术...",
                "classification_codes": ["G06N3/084", "G06N20/00"],
            },
        ]

        results = []
        for data in mock_results:
            result = PatentSearchResult(**data)
            result.similarity_score = self.calculate_similarity(result, query)
            if result.similarity_score >= 0.3:  # 最低阈值
                results.append(result)

        return results


class GooglePatentsSearchEngine(PatentSearchEngine):
    """Google Patents 检索引擎"""

    def __init__(self):
        super().__init__("google_patents", 0.3)

    async def search(self, query: PatentSearchQuery) -> List[PatentSearchResult]:
        """
        模拟 Google Patents 检索
        在实际应用中，这里会调用 Google Patents API
        """
        mock_results = [
            {
                "patent_id": "US20240123456",
                "title": "AI-Based Intelligent Recommendation System",
                "patent_number": "US11,123,456",
                "applicant": "Tech Corp",
                "inventors": ["John Doe", "Jane Smith"],
                "application_date": datetime(2024, 3, 5),
                "publication_date": datetime(2024, 10, 10),
                "abstract": "The invention relates to an AI-based recommendation system that uses deep learning...",
                "classification_codes": ["G06N3/08", "G06Q30/06"],
                "url": "https://patents.google.com/patent/US11123456",
            },
        ]

        results = []
        for data in mock_results:
            result = PatentSearchResult(**data)
            result.similarity_score = self.calculate_similarity(result, query)
            if result.similarity_score >= 0.3:
                results.append(result)

        return results


class EspacenetSearchEngine(PatentSearchEngine):
    """欧洲专利数据库检索引擎"""

    def __init__(self):
        super().__init__("espacenet", 0.2)

    async def search(self, query: PatentSearchQuery) -> List[PatentSearchResult]:
        """
        模拟 Espacenet 检索
        """
        mock_results = [
            {
                "patent_id": "EP2024123456",
                "title": "Intelligent System for Data Processing",
                "patent_number": "EP12345678",
                "applicant": "European Tech Ltd",
                "inventors": ["Hans Mueller", "Anna Schmidt"],
                "application_date": datetime(2024, 4, 20),
                "publication_date": datetime(2024, 11, 5),
                "abstract": "The present invention discloses an intelligent data processing system...",
                "classification_codes": ["G06F40/30", "G06N3/08"],
            },
        ]

        results = []
        for data in mock_results:
            result = PatentSearchResult(**data)
            result.similarity_score = self.calculate_similarity(result, query)
            if result.similarity_score >= 0.3:
                results.append(result)

        return results


class PatentSearchTool:
    """专利检索工具"""

    def __init__(self):
        self.engines = [
            CNIPASearchEngine(),
            GooglePatentsSearchEngine(),
            EspacenetSearchEngine(),
        ]
        self.config = {
            "relevance_threshold": 0.7,
            "max_results_per_engine": 50,
            "min_similarity_score": 0.6,
            "analysis_depth": "comprehensive",
        }

    async def search_patents(
        self,
        query: PatentSearchQuery,
        use_engines: Optional[List[str]] = None,
    ) -> PatentSearchReport:
        """
        执行专利检索

        Args:
            query: 检索查询
            use_engines: 指定使用的搜索引擎名称列表

        Returns:
            专利检索报告
        """
        # 确定使用的搜索引擎
        active_engines = [
            e for e in self.engines
            if use_engines is None or e.name in use_engines
        ]

        # 并行执行检索
        search_tasks = [engine.search(query) for engine in active_engines]
        search_results = await asyncio.gather(*search_tasks)

        # 合并结果
        all_results = []
        for results in search_results:
            all_results.extend(results)

        # 按相似度排序
        all_results.sort(key=lambda x: x.similarity_score or 0, reverse=True)

        # 去重（基于专利号）
        unique_results = []
        seen_patent_numbers = set()
        for result in all_results:
            patent_key = result.patent_number or result.application_number or result.patent_id
            if patent_key and patent_key not in seen_patent_numbers:
                seen_patent_numbers.add(patent_key)
                unique_results.append(result)

        # 限制结果数量
        max_total_results = self.config["max_results_per_engine"] * len(active_engines)
        unique_results = unique_results[:max_total_results]

        # 计算相关性统计
        high_relevance = sum(1 for r in unique_results if (r.similarity_score or 0) >= 0.7)
        medium_relevance = sum(
            1 for r in unique_results
            if 0.4 <= (r.similarity_score or 0) < 0.7
        )
        low_relevance = sum(1 for r in unique_results if (r.similarity_score or 0) < 0.4)

        # 生成检索分析
        analysis = self._generate_search_analysis(query, unique_results)

        # 生成新颖性分析
        novelty_analysis = self._generate_novelty_analysis(query, unique_results)

        # 生成相似性分析
        similarity_analysis = self._generate_similarity_analysis(query, unique_results)

        # 生成建议
        recommendations = self._generate_recommendations(query, unique_results)

        return PatentSearchReport(
            query=query,
            results=unique_results,
            total_results=len(unique_results),
            high_relevance_count=high_relevance,
            medium_relevance_count=medium_relevance,
            low_relevance_count=low_relevance,
            analysis=analysis,
            novelty_analysis=novelty_analysis,
            similarity_analysis=similarity_analysis,
            recommendations=recommendations,
        )

    def _generate_search_analysis(
        self, query: PatentSearchQuery, results: List[PatentSearchResult]
    ) -> str:
        """生成检索分析"""
        if not results:
            return "未找到相关专利，建议调整检索关键词或扩大检索范围。"

        analysis = f"## 检索分析报告\n\n"
        analysis += f"本次检索使用了 {len(query.keywords)} 个关键词：{', '.join(query.keywords)}\n\n"
        analysis += f"共检索到 {len(results)} 篇相关专利：\n"
        analysis += f"- 高相关度：{sum(1 for r in results if (r.similarity_score or 0) >= 0.7)} 篇\n"
        analysis += f"- 中相关度：{sum(1 for r in results if 0.4 <= (r.similarity_score or 0) < 0.7)} 篇\n"
        analysis += f"- 低相关度：{sum(1 for r in results if (r.similarity_score or 0) < 0.4)} 篇\n\n"

        # 分析技术领域分布
        all_classifications = []
        for result in results:
            all_classifications.extend(result.classification_codes)

        if all_classifications:
            analysis += "### 技术领域分布\n"
            for i, classification in enumerate(all_classifications[:5], 1):
                analysis += f"{i}. {classification}\n"
            analysis += "\n"

        return analysis

    def _generate_novelty_analysis(
        self, query: PatentSearchQuery, results: List[PatentSearchResult]
    ) -> str:
        """生成新颖性分析"""
        high_relevance_results = [
            r for r in results if (r.similarity_score or 0) >= self.config["min_similarity_score"]
        ]

        analysis = "## 新颖性分析\n\n"

        if not high_relevance_results:
            analysis += "未发现与本发明高度相似的现有技术，本发明具有较好的新颖性。\n"
        else:
            analysis += f"发现 {len(high_relevance_results)} 篇高度相关的现有技术：\n\n"
            for i, result in enumerate(high_relevance_results[:3], 1):
                analysis += f"{i}. {result.title}\n"
                analysis += f"   - 相似度：{result.similarity_score:.2f}\n"
                if result.relevance_explanation:
                    analysis += f"   - 相关性说明：{result.relevance_explanation}\n"
                analysis += "\n"

            analysis += "### 新颖性评估\n"
            analysis += "基于现有技术分析，"
            if len(high_relevance_results) <= 2:
                analysis += "本发明在某些方面可能具有新颖性，建议重点关注技术差异点。\n"
            else:
                analysis += "需要进一步分析本发明与现有技术的本质区别。\n"

        return analysis

    def _generate_similarity_analysis(
        self, query: PatentSearchQuery, results: List[PatentSearchResult]
    ) -> str:
        """生成相似性分析"""
        analysis = "## 相似性分析\n\n"

        # 按相似度分组
        very_high = [r for r in results if (r.similarity_score or 0) >= 0.9]
        high = [r for r in results if 0.7 <= (r.similarity_score or 0) < 0.9]
        medium = [r for r in results if 0.4 <= (r.similarity_score or 0) < 0.7]

        analysis += f"### 相似度分布\n"
        analysis += f"- 极高相似度（≥90%）：{len(very_high)} 篇\n"
        analysis += f"- 高相似度（70-89%）：{len(high)} 篇\n"
        analysis += f"- 中等相似度（40-69%）：{len(medium)} 篇\n\n"

        if very_high:
            analysis += "### 需要重点关注的高相似度专利\n"
            for result in very_high:
                analysis += f"- {result.title}\n"
                analysis += f"  相似度：{result.similarity_score:.2f}\n"
                analysis += f"  申请人：{result.applicant}\n\n"

        return analysis

    def _generate_recommendations(
        self, query: PatentSearchQuery, results: List[PatentSearchResult]
    ) -> List[str]:
        """生成建议"""
        recommendations = []

        high_relevance_count = sum(1 for r in results if (r.similarity_score or 0) >= 0.7)

        if high_relevance_count == 0:
            recommendations.append(
                "建议扩大检索关键词范围，增加同义词或相关技术词汇"
            )
            recommendations.append(
                "建议调整专利类型筛选条件，获取更全面的现有技术信息"
            )
        elif high_relevance_count > 10:
            recommendations.append(
                "发现较多相似专利，建议进一步细化检索条件"
            )
            recommendations.append(
                "重点关注与本发明核心技术差异点，准备应对可能的现有技术挑战"
            )
        else:
            recommendations.append(
                "检索结果数量适中，建议仔细分析每篇高相关度专利的技术方案"
            )
            recommendations.append(
                "重点关注权利要求书的技术特征，分析本发明的创新点"
            )

        # 建议检索策略
        recommendations.append(
            "建议检索同族专利和引用专利，获取更完整的技术背景"
        )
        recommendations.append(
            "建议检索竞争对手的专利布局，了解市场竞争态势"
        )

        return recommendations

    def save_report(self, report: PatentSearchReport, file_path: str):
        """保存检索报告到文件"""
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(report.model_dump(), f, ensure_ascii=False, indent=2, default=str)
