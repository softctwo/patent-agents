#!/usr/bin/env python3
"""
实用新型专利撰写测试 - 区块链硬件钱包
使用Gemini-2.5-Pro模型进行智能专利撰写
"""

import os
import sys
import json
from datetime import datetime
from typing import Dict, List
import google.generativeai as genai
from dotenv import load_dotenv

# 加载.env文件
load_dotenv()

class GeminiUtilityModelWriter:
    """基于Gemini-2.5-Pro的实用新型专利撰写工具"""

    def __init__(self):
        """初始化Gemini模型"""
        self.gemini_model = None
        self._init_gemini()

    def _init_gemini(self):
        """初始化Gemini模型"""
        try:
            api_key = os.getenv("GOOGLE_API_KEY")
            if api_key and api_key != "your_gemini_api_key_here":
                genai.configure(api_key=api_key)
                self.gemini_model = genai.GenerativeModel('gemini-2.5-pro')
                print("✅ Gemini-2.5-Pro模型初始化成功")
            else:
                print("❌ 未设置有效的GOOGLE_API_KEY")
        except Exception as e:
            print(f"❌ 模型初始化失败: {e}")
            self.gemini_model = None

    def generate_utility_model_patent(
        self,
        product_name: str,
        technical_field: str,
        product_description: str,
        key_components: List[str],
        structural_features: str,
        innovative_points: str,
        beneficial_effects: str
    ) -> str:
        """
        生成实用新型专利申请文件

        Args:
            product_name: 产品名称
            technical_field: 技术领域
            product_description: 产品描述
            key_components: 关键组件列表
            structural_features: 结构特征
            innovative_points: 创新点
            beneficial_effects: 有益效果

        Returns:
            生成的专利申请文件
        """
        if not self.gemini_model:
            print("❌ Gemini模型未初始化")
            return None

        print("\n" + "=" * 70)
        print("🧠 Gemini-2.5-Pro 实用新型专利撰写")
        print("=" * 70)

        # 构建详细的撰写提示
        prompt = f"""
作为专业的专利撰写专家，请撰写一份符合中国专利法要求的实用新型专利申请文件。

**产品信息：**
- 产品名称：{product_name}
- 技术领域：{technical_field}
- 产品描述：{product_description}

**结构特征：**
{structural_features}

**关键组件：**
{', '.join(key_components)}

**创新点：**
{innovative_points}

**有益效果：**
{beneficial_effects}

**撰写要求：**
1. 必须严格符合实用新型专利的格式要求
2. 重点保护产品的形状、构造及其结合
3. 包含以下8个完整章节：
   【1】技术领域
   【2】背景技术
   【3】实用新型内容
   【4】附图说明
   【5】具体实施方式
   【6】权利要求书（至少5项权利要求）
   【7】实用新型说明

4. 技术方案描述要具体、清楚、完整
5. 权利要求书要从属关系清晰，保护范围合理
6. 不得包含软件算法、治疗方法等非实用新型内容
7. 必须是实体产品的结构特征

请生成完整的实用新型专利申请文件，格式规范，内容专业。
"""

        try:
            print("🧠 正在使用Gemini-2.5-Pro生成专利内容...")
            response = self.gemini_model.generate_content(prompt)
            patent_content = response.text

            print("✅ 专利内容生成完成")
            print(f"📝 内容长度: {len(patent_content):,} 字符")

            return patent_content

        except Exception as e:
            print(f"❌ 生成专利内容时发生错误: {e}")
            import traceback
            traceback.print_exc()
            return None

    def analyze_patent_quality(self, patent_content: str) -> Dict:
        """分析专利质量"""
        analysis = {
            "total_score": 0,
            "compliance_score": 0,
            "completeness_score": 0,
            "quality_score": 0,
            "issues": [],
            "strengths": []
        }

        # 检查必要章节
        required_sections = [
            "技术领域", "背景技术", "实用新型内容",
            "附图说明", "具体实施方式", "权利要求书"
        ]

        found_sections = []
        for section in required_sections:
            if section in patent_content:
                found_sections.append(section)

        completeness = len(found_sections) / len(required_sections) * 100
        analysis["completeness_score"] = completeness

        # 检查权利要求数量
        claim_count = patent_content.count("权利要求")
        if claim_count >= 5:
            analysis["strengths"].append("权利要求数量充足")
            analysis["total_score"] += 20
        else:
            analysis["issues"].append("权利要求数量不足（建议至少5项）")
            analysis["total_score"] += max(0, claim_count * 4)

        # 检查技术方案描述
        if "结构" in patent_content or "构造" in patent_content:
            analysis["strengths"].append("重点描述结构特征（符合实用新型要求）")
            analysis["total_score"] += 20
        else:
            analysis["issues"].append("结构特征描述不够突出")

        # 检查是否包含非实用新型内容
        forbidden_terms = ["算法", "软件", "方法步骤", "治疗方法", "控制方法"]
        has_forbidden = any(term in patent_content for term in forbidden_terms)
        if not has_forbidden:
            analysis["strengths"].append("未包含非实用新型内容")
            analysis["compliance_score"] = 100
            analysis["total_score"] += 30
        else:
            analysis["issues"].append("包含可能不适用于实用新型的内容")
            analysis["compliance_score"] = 50

        # 检查创新性描述
        if "创新" in patent_content or "改进" in patent_content:
            analysis["strengths"].append("突出技术创新点")
            analysis["total_score"] += 15

        # 检查具体实施方式
        if "如图" in patent_content and "所示" in patent_content:
            analysis["strengths"].append("包含详细的实施方式说明")
            analysis["total_score"] += 15

        # 计算总分
        analysis["total_score"] = min(100, analysis["total_score"])
        analysis["quality_score"] = (
            analysis["completeness_score"] * 0.3 +
            analysis["compliance_score"] * 0.4 +
            analysis["total_score"] * 0.3
        )

        return analysis


def main():
    """主测试函数"""
    print("\n" + "=" * 70)
    print("🎯 实用新型专利撰写测试 - 区块链硬件钱包")
    print("📅 测试时间:", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print("🤖 使用模型: Gemini-2.5-Pro")
    print("=" * 70)

    # 初始化撰写工具
    writer = GeminiUtilityModelWriter()

    if not writer.gemini_model:
        print("❌ 无法初始化Gemini模型，测试终止")
        return

    # 定义区块链硬件钱包的专利信息
    product_info = {
        "product_name": "一种带生物识别和无线充电功能的区块链硬件钱包",
        "technical_field": "数字资产存储设备领域，具体涉及区块链硬件钱包的结构设计",
        "product_description": "本产品是一种便携式区块链硬件钱包，用于安全存储加密货币私钥和进行数字签名。产品采用椭圆形的紧凑结构，集成指纹识别、OLED显示屏、无线充电和安全芯片等组件。",
        "key_components": [
            "椭圆形外壳体", "指纹识别模块", "OLED显示屏", "PCB主板",
            "锂电池", "无线充电线圈", "USB-C接口", "物理按钮",
            "安全芯片", "防拆解结构"
        ],
        "structural_features": """
        1. 椭圆形外壳体：采用ABS工程塑料材质，内部设有加强筋结构，尺寸为85mm×55mm×8mm
        2. 指纹识别模块：电容式传感器，位于外壳正面下方，通过FPC柔性电路板连接
        3. OLED显示屏：1.3英寸240×240像素分辨率，位于外壳正面中央
        4. PCB主板：6层板设计，包含STM32H743主控芯片、ATECC608A加密芯片
        5. 锂电池：500mAh锂聚合物电池，可拆卸式连接器固定
        6. 无线充电线圈：绕制在外壳内部边缘，支持Qi标准
        7. USB-C接口：位于外壳底部，外露部分有防水硅胶塞
        8. 物理按钮：硅胶按键结构，包括确认键和返回键
        9. 安全芯片：SIM卡大小，通过弹片式卡槽安装
        10. 防拆解结构：包括易碎贴和防拆螺丝
        """,
        "innovative_points": """
        1. 椭圆形紧凑结构设计：相比传统卡片式或U盘式钱包，便携性提升40%
        2. 双重身份验证：指纹识别+密码，提供60%的安全性提升
        3. 无线充电功能：支持Qi标准无线充电，摆脱线缆束缚
        4. 模块化安全芯片：可插拔设计，便于升级和更换
        5. 防拆解结构：多层安全防护，有效防止物理攻击
        """,
        "beneficial_effects": """
        1. 便携性：椭圆形紧凑设计，体积缩小40%，便于携带
        2. 安全性：指纹识别+加密芯片，安全性提升60%
        3. 续航能力：500mAh电池+无线充电，续航时间达30天
        4. 用户体验：1.3英寸OLED显示屏，视觉体验提升50%
        5. 升级能力：模块化设计，支持安全芯片更换和升级
        6. 防护等级：防拆解结构，有效抵御物理攻击
        """
    }

    print("\n📋 测试产品信息:")
    print(f"  产品名称: {product_info['product_name']}")
    print(f"  技术领域: {product_info['technical_field']}")
    print(f"  关键组件数量: {len(product_info['key_components'])}")

    # 生成专利申请文件
    patent_content = writer.generate_utility_model_patent(
        product_name=product_info['product_name'],
        technical_field=product_info['technical_field'],
        product_description=product_info['product_description'],
        key_components=product_info['key_components'],
        structural_features=product_info['structural_features'],
        innovative_points=product_info['innovative_points'],
        beneficial_effects=product_info['beneficial_effects']
    )

    if not patent_content:
        print("❌ 专利内容生成失败")
        return

    # 保存生成的专利文件
    output_file = f"实用新型专利_区块链硬件钱包_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("=" * 70 + "\n")
        f.write("实用新型专利申请文件\n")
        f.write("基于Gemini-2.5-Pro智能生成\n")
        f.write("=" * 70 + "\n\n")
        f.write(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"产品名称: {product_info['product_name']}\n")
        f.write(f"模型: Gemini-2.5-Pro\n\n")
        f.write("-" * 70 + "\n\n")
        f.write(patent_content)

    print(f"\n✅ 专利文件已保存: {output_file}")

    # 质量分析
    print("\n📊 质量分析中...")
    analysis = writer.analyze_patent_quality(patent_content)

    # 输出分析结果
    print("\n" + "=" * 70)
    print("📈 专利质量分析报告")
    print("=" * 70)
    print(f"总体评分: {analysis['quality_score']:.1f}/100")
    print(f"合规性评分: {analysis['compliance_score']:.1f}/100")
    print(f"完整性评分: {analysis['completeness_score']:.1f}/100")
    print(f"内容评分: {analysis['total_score']}/100")

    print("\n✅ 优势:")
    for strength in analysis['strengths']:
        print(f"  • {strength}")

    if analysis['issues']:
        print("\n⚠️ 改进建议:")
        for issue in analysis['issues']:
            print(f"  • {issue}")

    # 保存分析报告
    report_file = f"专利质量分析报告_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(analysis, f, ensure_ascii=False, indent=2)

    print(f"\n📄 分析报告已保存: {report_file}")

    # 最终总结
    print("\n" + "=" * 70)
    print("✅ 测试完成!")
    print("=" * 70)
    print(f"📄 专利文件: {output_file}")
    print(f"📊 分析报告: {report_file}")
    print(f"🏆 质量评分: {analysis['quality_score']:.1f}/100")

    return {
        "status": "success",
        "patent_file": output_file,
        "report_file": report_file,
        "quality_score": analysis['quality_score']
    }


if __name__ == "__main__":
    result = main()
    if result:
        print(f"\n🎉 测试成功完成！质量评分: {result['quality_score']:.1f}/100")
