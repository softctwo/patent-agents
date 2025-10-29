"""
专利撰写和审查系统 - Web 用户界面

基于 Streamlit 的现代化用户界面
"""

import streamlit as st
import asyncio
import os
from datetime import datetime
import traceback
from typing import Optional

# 配置页面
st.set_page_config(
    page_title="专利助手 - AI 专利撰写与审查系统",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 添加自定义 CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2e86c1;
        margin: 1.5rem 0 1rem 0;
    }
    .success-box {
        padding: 1rem;
        border-left: 4px solid #28a745;
        background-color: #d4edda;
        margin: 1rem 0;
    }
    .warning-box {
        padding: 1rem;
        border-left: 4px solid #ffc107;
        background-color: #fff3cd;
        margin: 1rem 0;
    }
    .error-box {
        padding: 1rem;
        border-left: 4px solid #dc3545;
        background-color: #f8d7da;
        margin: 1rem 0;
    }
    .info-box {
        padding: 1rem;
        border-left: 4px solid #17a2b8;
        background-color: #d1ecf1;
        margin: 1rem 0;
    }
    .result-box {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border: 1px solid #dee2e6;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)


def init_session_state():
    """初始化会话状态"""
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "results" not in st.session_state:
        st.session_state.results = {}
    if "api_configured" not in st.session_state:
        st.session_state.api_configured = os.getenv("GOOGLE_API_KEY") is not None


def display_header():
    """显示页面头部"""
    st.markdown('<h1 class="main-header">📄 专利助手</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p style="text-align: center; font-size: 1.2rem; color: #6c757d;">'
        '基于 Google Gemini AI 的智能专利撰写与审查系统'
        '</p>',
        unsafe_allow_html=True
    )
    st.markdown("---")


def check_api_status():
    """检查 API 配置状态"""
    if not st.session_state.api_configured:
        st.markdown(
            '<div class="warning-box">'
            '<strong>⚠️ API 密钥未配置</strong><br>'
            '请设置 GOOGLE_API_KEY 环境变量以使用 Gemini AI 功能'
            '</div>',
            unsafe_allow_html=True
        )
        return False
    return True


async def run_patent_agent(task_description: str, inputs: dict = None):
    """运行专利 agent"""
    try:
        # 导入 patent_agent
        import sys
        import os
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

        from main_agent import patent_agent
        from agents import Runner

        # 准备输入
        if inputs is None:
            input_text = task_description
        else:
            input_text = task_description + "\n\n" + str(inputs)

        # 运行 agent
        result = await Runner.run(patent_agent, input_text)
        return result.final_output, None

    except Exception as e:
        error_msg = f"执行任务时发生错误：{str(e)}\n\n详细错误：\n{traceback.format_exc()}"
        return None, error_msg


def display_result(title: str, content: str, result_type: str = "info"):
    """显示结果"""
    # 选择样式
    style_map = {
        "success": "success-box",
        "warning": "warning-box",
        "error": "error-box",
        "info": "info-box"
    }

    box_class = style_map.get(result_type, "info-box")

    st.markdown(
        f'<div class="{box_class}">'
        f'<strong>{title}</strong><br><br>{content.replace(chr(10), "<br>")}'
        '</div>',
        unsafe_allow_html=True
    )


def patent_writing_page():
    """专利撰写页面"""
    st.markdown('<h2 class="sub-header">📝 专利撰写</h2>', unsafe_allow_html=True)

    with st.form("patent_writing_form"):
        st.markdown("### 基本信息")

        col1, col2 = st.columns(2)

        with col1:
            invention_title = st.text_input(
                "发明名称",
                placeholder="例如：基于深度学习的智能推荐系统",
                help="简洁明了地描述发明名称"
            )

            technical_field = st.text_input(
                "技术领域",
                placeholder="例如：人工智能、机器学习、数据挖掘",
                help="技术领域应具体、明确"
            )

            patent_type = st.selectbox(
                "专利类型",
                ["invention", "utility_model", "design"],
                format_func=lambda x: {
                    "invention": "发明专利",
                    "utility_model": "实用新型专利",
                    "design": "外观设计专利"
                }[x]
            )

        with col2:
            applicant_name = st.text_input(
                "申请人姓名",
                placeholder="公司名称或个人姓名"
            )

            applicant_address = st.text_input(
                "申请人地址",
                placeholder="详细地址"
            )

            inventor_name = st.text_input(
                "发明人姓名",
                placeholder="发明人姓名"
            )

        st.markdown("### 详细描述")

        invention_description = st.text_area(
            "发明描述",
            height=150,
            placeholder="详细描述您的发明，包括技术原理、实现方法、创新点等...",
            help="详细描述有助于生成更准确的专利申请文件"
        )

        background_info = st.text_area(
            "背景信息（可选）",
            height=100,
            placeholder="现有技术存在的问题、技术难点等..."
        )

        specific_problems = st.text_area(
            "要解决的技术问题（可选）",
            height=100,
            placeholder="详细描述要解决的技术问题..."
        )

        solution = st.text_area(
            "技术解决方案（可选）",
            height=150,
            placeholder="描述具体的技术解决方案和实施方式..."
        )

        beneficial_effects = st.text_area(
            "有益效果（可选）",
            height=100,
            placeholder="描述发明带来的有益效果..."
        )

        submitted = st.form_submit_button(
            "🚀 生成专利申请文件",
            use_container_width=True,
            type="primary"
        )

    if submitted:
        if not all([invention_title, technical_field, invention_description]):
            st.error("请填写必要的信息：发明名称、技术领域和发明描述")
            return

        # 显示加载状态
        with st.spinner("正在生成专利申请文件，请稍候..."):
            # 准备输入参数
            inputs = {
                "invention_description": invention_description,
                "technical_field": technical_field,
                "patent_type": patent_type,
                "background_info": background_info,
                "specific_problems": specific_problems,
                "solution": solution,
                "beneficial_effects": beneficial_effects,
                "applicant_name": applicant_name,
                "applicant_address": applicant_address,
                "inventor_name": inventor_name,
            }

            # 构建任务描述
            task_desc = f"""
            请为以下发明撰写一份完整的{patent_type}专利申请文件：

            发明名称：{invention_title}
            技术领域：{technical_field}
            发明描述：{invention_description}

            {'背景信息：' + background_info if background_info else ''}
            {'要解决的技术问题：' + specific_problems if specific_problems else ''}
            {'技术解决方案：' + solution if solution else ''}
            {'有益效果：' + beneficial_effects if beneficial_effects else ''}
            """

            # 运行 agent
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result, error = loop.run_until_complete(run_patent_agent(task_desc))
            loop.close()

            if error:
                display_result("❌ 错误", error, "error")
            elif result:
                st.markdown("### 📄 生成结果")

                # 创建两个标签页：原始结果和优化结果
                tab1, tab2 = st.tabs(["📄 原始结果", "✨ 优化显示"])

                with tab1:
                    st.markdown('<div class="result-box">', unsafe_allow_html=True)
                    st.markdown(result)
                    st.markdown('</div>', unsafe_allow_html=True)

                with tab2:
                    # 解析并优化显示
                    st.markdown("""
                    <div style="background-color: white; padding: 2rem; border-radius: 0.5rem; border: 1px solid #dee2e6;">
                    """, unsafe_allow_html=True)

                    # 尝试提取不同部分
                    sections = result.split('\n\n')
                    for section in sections:
                        if section.strip():
                            if "发明名称" in section or "title" in section.lower():
                                st.markdown(f"#### {section}")
                            elif any(keyword in section.lower() for keyword in ["技术领域", "背景技术", "发明内容"]):
                                st.markdown(f"#### {section.split(':')[0] if ':' in section else '内容'}")
                                content = section.split(':', 1)[1] if ':' in section else section
                                st.markdown(content)
                            else:
                                st.markdown(section)

                    st.markdown("</div>", unsafe_allow_html=True)

                # 下载按钮
                col1, col2, col3 = st.columns([1, 1, 1])
                with col2:
                    st.download_button(
                        label="💾 下载为文本文件",
                        data=result,
                        file_name=f"专利申请文件_{invention_title}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                        mime="text/plain",
                        use_container_width=True
                    )


def patent_review_page():
    """专利审查页面"""
    st.markdown('<h2 class="sub-header">🔍 专利审查</h2>', unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["📄 申请文件预审", "🖼️ 附图审查"])

    with tab1:
        st.markdown("### 上传专利申请文件进行预审")

        application_text = st.text_area(
            "专利申请文件内容",
            height=400,
            placeholder="请粘贴完整的专利申请文件内容...",
            help="支持纯文本格式的专利申请文件"
        )

        col1, col2 = st.columns([3, 1])

        with col1:
            uploaded_file = st.file_uploader(
                "或上传文件",
                type=['txt', 'doc', 'docx'],
                help="支持 TXT、DOC、DOCX 格式"
            )

        with col2:
            if uploaded_file is not None:
                application_text = uploaded_file.read().decode('utf-8')

        if st.button("🔍 开始审查", type="primary", use_container_width=True):
            if not application_text.strip():
                st.error("请输入专利申请文件内容")
                return

            with st.spinner("正在审查专利申请文件，请稍候..."):
                task_desc = "请审查以下专利申请文件的格式规范性、内容完整性和技术质量："

                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                result, error = loop.run_until_complete(
                    run_patent_agent(task_desc, {"application_text": application_text})
                )
                loop.close()

                if error:
                    display_result("❌ 错误", error, "error")
                elif result:
                    st.markdown("### 📊 审查结果")
                    st.markdown('<div class="result-box">', unsafe_allow_html=True)
                    st.markdown(result)
                    st.markdown('</div>', unsafe_allow_html=True)

                    # 保存结果到会话状态
                    st.session_state.results["review"] = result

    with tab2:
        st.markdown("### 附图审查")

        st.info("👷‍♀️ 附图审查功能正在开发中，敬请期待...")


def patent_search_page():
    """专利检索页面"""
    st.markdown('<h2 class="sub-header">🔎 专利检索</h2>', unsafe_allow_html=True)

    with st.form("patent_search_form"):
        st.markdown("### 检索条件")

        col1, col2 = st.columns(2)

        with col1:
            keywords = st.text_input(
                "检索关键词",
                placeholder="例如：人工智能、机器学习、推荐系统",
                help="多个关键词用逗号分隔"
            )

            applicant = st.text_input(
                "申请人筛选（可选）",
                placeholder="例如：清华大学"
            )

        with col2:
            patent_types = st.multiselect(
                "专利类型",
                ["invention", "utility_model", "design"],
                default=["invention"],
                format_func=lambda x: {
                    "invention": "发明专利",
                    "utility_model": "实用新型",
                    "design": "外观设计"
                }[x]
            )

            inventor = st.text_input(
                "发明人筛选（可选）",
                placeholder="发明人姓名"
            )

        st.markdown("### 检索策略")
        search_strategy = st.selectbox(
            "检索策略",
            ["精确匹配", "模糊匹配", "语义检索"],
            help="选择不同的检索策略以获得更准确的检索结果"
        )

        submitted = st.form_submit_button(
            "🔍 开始检索",
            use_container_width=True,
            type="primary"
        )

    if submitted:
        if not keywords.strip():
            st.error("请输入检索关键词")
            return

        with st.spinner("正在检索专利数据库，请稍候..."):
            task_desc = f"""
            请检索与以下关键词相关的专利：

            关键词：{keywords}
            专利类型：{', '.join(patent_types)}
            申请人：{applicant or '不限'}
            发明人：{inventor or '不限'}
            检索策略：{search_strategy}

            请提供：
            1. 检索结果统计
            2. 相关性分析
            3. 技术领域分布
            4. 竞争态势分析
            5. 新颖性评估
            6. 检索建议
            """

            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result, error = loop.run_until_complete(run_patent_agent(task_desc))
            loop.close()

            if error:
                display_result("❌ 错误", error, "error")
            elif result:
                st.markdown("### 📈 检索结果")
                st.markdown('<div class="result-box">', unsafe_allow_html=True)
                st.markdown(result)
                st.markdown('</div>', unsafe_allow_html=True)

                # 保存结果
                st.session_state.results["search"] = result


def settings_page():
    """设置页面"""
    st.markdown('<h2 class="sub-header">⚙️ 系统设置</h2>', unsafe_allow_html=True)

    # API 配置状态
    st.markdown("### 🔑 API 配置")

    if st.session_state.api_configured:
        st.markdown(
            '<div class="success-box">'
            '<strong>✅ Gemini API 已配置</strong><br>'
            f'API 密钥：{os.getenv("GOOGLE_API_KEY")[:10]}...'
            '</div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            '<div class="error-box">'
            '<strong>❌ Gemini API 未配置</strong><br>'
            '请设置 GOOGLE_API_KEY 环境变量'
            '</div>',
            unsafe_allow_html=True
        )

        st.code("export GOOGLE_API_KEY='your_google_api_key_here'", language="bash")

    st.markdown("---")

    # 审查规则配置
    st.markdown("### 📋 审查规则")

    rule_type = st.selectbox(
        "规则类型",
        ["pre_review", "figure_review"],
        format_func=lambda x: {
            "pre_review": "预审规则",
            "figure_review": "附图审查规则"
        }[x]
    )

    col1, col2 = st.columns([1, 1])

    with col1:
        if st.button("📋 查看规则列表", use_container_width=True):
            with st.spinner("正在获取规则列表..."):
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                result, error = loop.run_until_complete(
                    run_patent_agent(f"请显示{rule_type}的所有规则")
                )
                loop.close()

                if result:
                    st.markdown("### 📝 规则列表")
                    st.markdown('<div class="result-box">', unsafe_allow_html=True)
                    st.markdown(result)
                    st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.info("规则配置功能正在开发中...")

    st.markdown("---")

    # 系统信息
    st.markdown("### ℹ️ 系统信息")

    st.markdown(
        '<div class="info-box">'
        '<strong>专利助手 v1.0.0</strong><br>'
        '基于 OpenAI Agents SDK 和 Google Gemini 构建<br>'
        f'最后更新：{datetime.now().strftime("%Y-%m-%d")}'
        '</div>',
        unsafe_allow_html=True
    )


def main():
    """主函数"""
    # 初始化会话状态
    init_session_state()

    # 显示头部
    display_header()

    # 检查 API 状态
    api_ok = check_api_status()

    # 创建侧边栏导航
    with st.sidebar:
        st.markdown("### 📋 功能导航")

        page = st.radio(
            "选择功能",
            [
                "🏠 首页",
                "📝 专利撰写",
                "🔍 专利审查",
                "🔎 专利检索",
                "⚙️ 系统设置"
            ],
            index=0
        )

        st.markdown("---")

        # API 状态指示器
        if api_ok:
            st.markdown(
                '<div style="padding: 0.5rem; background-color: #d4edda; border-radius: 0.25rem; text-align: center;">'
                '🟢 API 连接正常'
                '</div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                '<div style="padding: 0.5rem; background-color: #f8d7da; border-radius: 0.25rem; text-align: center;">'
                '🔴 API 未配置'
                '</div>',
                unsafe_allow_html=True
            )

    # 根据选择显示不同页面
    if page == "🏠 首页":
        st.markdown("""
        ### 欢迎使用专利助手！

        这是一个基于 Google Gemini AI 的智能专利工作流系统，提供以下功能：

        #### 🚀 主要功能

        1. **📝 专利撰写**
           - 根据发明描述自动生成专利申请文件
           - 支持发明专利、实用新型、外观设计
           - 符合专利局格式要求

        2. **🔍 专利审查**
           - 智能预审申请文件
           - 检查格式规范性和内容完整性
           - 提供详细审查报告

        3. **🔎 专利检索**
           - 多维度专利检索
           - 新颖性分析
           - 竞争态势评估

        4. **⚙️ 系统设置**
           - API 配置管理
           - 审查规则配置
           - 系统状态监控

        #### 💡 使用说明

        1. 确保已配置 Google Gemini API 密钥
        2. 从左侧导航栏选择所需功能
        3. 填写相应表单或上传文件
        4. 点击执行按钮等待结果
        5. 下载或保存生成的结果

        #### 🎯 适用场景

        - 专利代理机构快速撰写专利申请
        - 企业内部专利申请支持
        - 个人发明人专利申请辅助
        - 专利现有技术检索分析

        ---

        **开始使用：请从左侧导航栏选择功能，或直接访问"专利撰写"开始您的专利申请之旅！**
        """)

    elif page == "📝 专利撰写":
        if api_ok:
            patent_writing_page()
        else:
            st.warning("请先配置 API 密钥")

    elif page == "🔍 专利审查":
        if api_ok:
            patent_review_page()
        else:
            st.warning("请先配置 API 密钥")

    elif page == "🔎 专利检索":
        if api_ok:
            patent_search_page()
        else:
            st.warning("请先配置 API 密钥")

    elif page == "⚙️ 系统设置":
        settings_page()


if __name__ == "__main__":
    main()
