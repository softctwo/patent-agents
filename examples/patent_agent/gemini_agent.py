"""
使用 Gemini API 的专利 Agent

集成 Google Gemini API 增强 AI 能力
"""

import os
import google.generativeai as genai
from typing import Optional, List, Dict, Any
import asyncio
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 配置 Gemini API
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)
    print(f"✓ 已配置 Gemini API 密钥")
else:
    print("⚠ 未找到 GOOGLE_API_KEY 环境变量")


class GeminiPatentAgent:
    """基于 Gemini API 的专利助手"""

    def __init__(self, model_name: str = "gemini-1.5-flash"):
        """
        初始化 Gemini 专利助手

        Args:
            model_name: Gemini 模型名称
        """
        self.model_name = model_name
        self.model = None
        self._initialize_model()

    def _initialize_model(self):
        """初始化 Gemini 模型"""
        try:
            self.model = genai.GenerativeModel(self.model_name)
            print(f"✓ Gemini 模型 {self.model_name} 初始化成功")
        except Exception as e:
            print(f"✗ Gemini 模型初始化失败：{e}")
            self.model = None

    async def generate_patent_application(
        self,
        invention_description: str,
        technical_field: str,
        patent_type: str = "invention",
        background_info: Optional[str] = None,
        applicant_info: Optional[str] = None,
        inventor_info: Optional[str] = None,
    ) -> str:
        """
        使用 Gemini 生成专利申请文件

        Args:
            invention_description: 发明描述
            technical_field: 技术领域
            patent_type: 专利类型
            background_info: 背景信息
            applicant_info: 申请人信息
            inventor_info: 发明人信息

        Returns:
            生成的专利申请文件
        """
        if not self.model:
            return "错误：Gemini 模型未初始化"

        prompt = f"""
        你是一位专业的专利撰写专家。请根据以下信息撰写一份完整的{patent_type}专利申请文件：

        发明描述：{invention_description}
        技术领域：{technical_field}
        专利类型：{patent_type}

        请按照以下结构撰写：

        1. 发明名称
        2. 技术领域
        3. 背景技术（详细分析现有技术的问题）
        4. 发明内容
           - 要解决的技术问题
           - 技术解决方案
           - 有益效果
        5. 附图说明
        6. 具体实施方式
        7. 权利要求书（至少5项，包含独立和从属权利要求）

        要求：
        - 内容专业、逻辑清晰
        - 技术描述准确、完整
        - 权利要求层次分明
        - 符合专利局格式要求

        {'申请人信息：' + applicant_info if applicant_info else ''}
        {'发明人信息：' + inventor_info if inventor_info else ''}
        """

        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"生成专利申请文件时发生错误：{str(e)}"

    async def review_patent_application(
        self,
        application_text: str,
    ) -> str:
        """
        使用 Gemini 审查专利申请文件

        Args:
            application_text: 专利申请文件文本

        Returns:
            审查报告
        """
        if not self.model:
            return "错误：Gemini 模型未初始化"

        prompt = f"""
        你是一位资深的专利审查员。请仔细审查以下专利申请文件，并提供详细的审查报告：

        {application_text}

        请从以下维度进行审查：

        1. 格式规范性检查
           - 标题长度和格式
           - 各章节结构
           - 权利要求格式

        2. 内容完整性检查
           - 技术领域描述
           - 背景技术分析
           - 发明内容完整性
           - 附图说明

        3. 技术质量评估
           - 技术方案的创新性
           - 技术问题的明确性
           - 解决方案的可行性
           - 有益效果的合理性

        4. 法律合规性
           - 新颖性评估
           - 创造性评估
           - 实用性评估

        请按以下格式输出审查报告：

        ## 审查结果
        - 审查状态：[通过/有条件通过/不通过]
        - 综合评分：[0-100分]

        ## 发现的问题
        ### 严重问题（必须修改）
        [列出所有严重问题及修改建议]

        ### 一般问题（建议修改）
        [列出所有一般问题及修改建议]

        ### 优化建议
        [提供进一步优化的建议]

        ## 审查结论
        [总结审查意见，给出明确建议]

        请客观、专业地完成审查，优缺点并重。
        """

        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"审查专利申请文件时发生错误：{str(e)}"

    async def search_patents_analysis(
        self,
        keywords: str,
        technical_field: str,
    ) -> str:
        """
        使用 Gemini 分析专利检索需求

        Args:
            keywords: 检索关键词
            technical_field: 技术领域

        Returns:
            检索分析报告
        """
        if not self.model:
            return "错误：Gemini 模型未初始化"

        prompt = f"""
        你是一位专业的专利检索专家。请为以下专利检索需求提供详细的检索策略和分析：

        检索关键词：{keywords}
        技术领域：{technical_field}

        请提供：

        1. 检索策略建议
           - 关键词优化建议
           - 分类号建议
           - 检索式构建

        2. 技术背景分析
           - 该技术领域的发展现状
           - 主要技术路线
           - 关键技术和核心专利

        3. 竞争态势分析
           - 主要申请人
           - 技术热点
           - 专利布局特点

        4. 检索建议
           - 优先检索的数据库
           - 检索时间范围
           - 相似度阈值建议

        5. 风险提示
           - 可能的现有技术冲突
           - 技术规避建议
           - 专利性评估要点

        请提供专业、详细的分析报告。
        """

        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"专利检索分析时发生错误：{str(e)}"

    async def optimize_patent_draft(
        self,
        draft_text: str,
        optimization_goal: str,
    ) -> str:
        """
        使用 Gemini 优化专利草稿

        Args:
            draft_text: 专利草稿
            optimization_goal: 优化目标（如：提高创造性、增强保护范围等）

        Returns:
            优化建议和修改后的文本
        """
        if not self.model:
            return "错误：Gemini 模型未初始化"

        prompt = f"""
        你是一位资深的专利代理师。请优化以下专利草稿，优化目标是：{optimization_goal}

        专利草稿：
        {draft_text}

        请提供：

        1. 当前文本分析
           - 优点
           - 不足之处
           - 与优化目标的差距

        2. 具体优化建议
           - 技术方案描述优化
           - 权利要求优化
           - 附图说明优化

        3. 优化后的完整文本
           - 保持原有核心内容
           - 应用优化建议
           - 提升整体质量

        4. 优化说明
           - 重点修改内容
           - 修改理由
   - 对提升专利质量的作用

        请确保优化后的文本更加专业、完整、有说服力。
        """

        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"优化专利草稿时发生错误：{str(e)}"

    async def answer_patent_question(
        self,
        question: str,
        context: Optional[str] = None,
    ) -> str:
        """
        使用 Gemini 回答专利相关问题

        Args:
            question: 问题
            context: 可选的上下文信息

        Returns:
            答案
        """
        if not self.model:
            return "错误：Gemini 模型未初始化"

        prompt = f"""
        你是一位专利法专家。请回答以下专利相关问题：

        问题：{question}

        {'相关上下文：' + context if context else ''}

        请提供：
        1. 直接回答
        2. 详细解释
        3. 相关法规依据（如适用）
        4. 实际案例（如适用）

        请确保答案准确、专业、易懂。
        """

        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"回答问题时发生错误：{str(e)}"

    def get_model_info(self) -> Dict[str, Any]:
        """获取模型信息"""
        return {
            "model_name": self.model_name,
            "api_configured": GOOGLE_API_KEY is not None,
            "model_initialized": self.model is not None,
        }


# 创建全局实例
gemini_agent = GeminiPatentAgent()


async def demo_gemini_capabilities():
    """演示 Gemini 能力"""
    print("\n" + "=" * 60)
    print("Gemini AI 能力演示")
    print("=" * 60)

    # 1. 测试模型信息
    info = gemini_agent.get_model_info()
    print(f"\n模型信息：{info}")

    # 2. 专利撰写测试
    print("\n--- 测试专利撰写 ---")
    patent_text = await gemini_agent.generate_patent_application(
        invention_description="一种基于深度学习的智能推荐系统，通过分析用户行为数据实现个性化推荐",
        technical_field="人工智能、机器学习、数据挖掘",
        patent_type="发明专利",
        applicant_info="张三科技有限公司",
        inventor_info="李四",
    )
    print(patent_text[:500] + "...")

    # 3. 专利审查测试
    print("\n--- 测试专利审查 ---")
    review_result = await gemini_agent.review_patent_application(
        application_text="发明名称：一种方法\n技术领域：人工智能\n背景技术：现有技术存在问题"
    )
    print(review_result[:500] + "...")

    # 4. 检索分析测试
    print("\n--- 测试检索分析 ---")
    search_analysis = await gemini_agent.search_patents_analysis(
        keywords="人工智能、推荐系统",
        technical_field="机器学习",
    )
    print(search_analysis[:500] + "...")

    print("\n" + "=" * 60)
    print("演示完成")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(demo_gemini_capabilities())
