"""
测试 Gemini 专利撰写功能 - 完整版

提供完整信息来生成专利申请文件
"""

import asyncio
import os
from dotenv import load_dotenv
from datetime import datetime

# 加载环境变量
load_dotenv('/Users/zhangyanlong/workspaces/openai-agents-python/.env')

from main_agent import patent_agent
from agents import Runner


async def test_writing_complete():
    """测试完整的专利撰写"""
    print("=" * 60)
    print("🔬 Gemini 专利撰写功能测试（完整版）")
    print("=" * 60)

    # 检查 API 配置
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ 错误：未设置 GOOGLE_API_KEY 环境变量")
        print("请设置：export GOOGLE_API_KEY='your_api_key'")
        return

    print(f"✓ API 密钥已配置：{api_key[:10]}...")

    # 完整的专利撰写请求
    prompt = """
    请撰写一份完整的发明专利申请文件，包括以下所有章节：

    ## 发明信息
    - 发明名称：基于深度学习的智能推荐系统
    - 技术领域：人工智能、机器学习、数据挖掘
    - 申请人：张三科技有限公司
    - 发明人：李四

    ## 发明描述
    1. 背景技术：
       - 现有推荐系统主要基于协同过滤和内容过滤
       - 存在的问题：冷启动问题、推荐准确率有限、无法捕捉用户兴趣动态变化
       - 传统方法难以处理大规模用户和物品数据

    2. 要解决的技术问题：
       - 提高推荐准确率
       - 解决冷启动问题
       - 捕捉用户兴趣的动态变化
       - 处理大规模数据的高效性

    3. 技术解决方案：
       - 采用多层神经网络架构
       - 结合嵌入层、隐藏层和输出层
       - 融合协同过滤和内容推荐技术
       - 实时学习用户反馈

    4. 有益效果：
       - 推荐准确率提升30%以上
       - 有效解决冷启动问题
       - 提升用户满意度和转化率
       - 计算效率提升50%

    5. 附图说明：
       - 图1：系统整体架构图
       - 图2：神经网络结构图
       - 图3：推荐流程图

    6. 具体实施方式：
       - 详细描述系统各模块
       - 神经网络训练方法
       - 实时学习机制

    7. 权利要求书：
       - 独立权利要求（1项）
       - 从属权利要求（5项）

    请按标准专利申请格式撰写，包含完整的发明名称、技术领域、背景技术、发明内容、附图说明、具体实施方式和权利要求书。
    """

    print("\n📝 正在生成完整的专利申请文件...")
    print("-" * 60)

    result = await Runner.run(patent_agent, prompt)

    # 保存结果
    output = result.final_output
    print("\n" + "=" * 60)
    print("📄 生成结果预览（前1000字符）")
    print("=" * 60)
    print(output[:1000] + "..." if len(output) > 1000 else output)

    # 保存到文件
    with open("patent_writing_complete_result.txt", "w", encoding="utf-8") as f:
        f.write("Gemini 专利撰写完整测试结果\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"测试时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"API 密钥：{api_key[:10]}...\n\n")
        f.write("完整请求：\n")
        f.write("-" * 60 + "\n")
        f.write(prompt.strip() + "\n\n")
        f.write("=" * 60 + "\n\n")
        f.write("生成结果：\n")
        f.write("-" * 60 + "\n")
        f.write(output)
        f.write("\n\n" + "=" * 60 + "\n")
        f.write(f"结果长度：{len(output)} 字符\n")
        f.write("测试状态：✅ 成功\n")

    print(f"\n✅ 测试完成！")
    print(f"📊 结果统计：")
    print(f"   - 输出长度：{len(output)} 字符")
    print(f"   - 行数：{output.count(chr(10))} 行")
    print(f"💾 详细结果已保存到：patent_writing_complete_result.txt")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(test_writing_complete())
