#!/usr/bin/env python
"""
Google Gemini + OpenAI Agents SDK 配置验证脚本

此脚本将检查：
1. LiteLLM 是否已安装
2. Google API Key 是否设置
3. 模型连接是否正常
"""

import os
import sys
import subprocess


def check_litellm():
    """检查 LiteLLM 是否安装"""
    print("🔍 检查 LiteLLM 安装...")
    try:
        import litellm
        # 尝试获取版本信息
        try:
            version = litellm.__version__
        except AttributeError:
            version = "unknown"

        print(f"✅ LiteLLM 已安装，版本：{version}")
        return True
    except ImportError:
        print("❌ LiteLLM 未安装")
        print("   解决方案：pip install litellm")
        return False


def check_api_key():
    """检查 Google API Key"""
    print("\n🔑 检查 Google API Key...")
    api_key = os.getenv("GOOGLE_API_KEY")
    if api_key:
        # 隐藏 API Key 用于显示
        masked_key = api_key[:8] + "*" * (len(api_key) - 12) + api_key[-4:]
        print(f"✅ API Key 已设置：{masked_key}")
        return True
    else:
        print("❌ GOOGLE_API_KEY 环境变量未设置")
        print("   解决方案：export GOOGLE_API_KEY='your_api_key_here'")
        print("   获取 API Key：https://aistudio.google.com/app/apikey")
        return False


def test_model_connection():
    """测试模型连接"""
    print("\n🌐 测试模型连接...")
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("⏭️  跳过连接测试（未设置 API Key）")
        return False

    try:
        import litellm

        print("   正在测试 gemini/gemini-2.0-flash...")
        response = litellm.completion(
            model="gemini/gemini-2.0-flash",
            messages=[{"role": "user", "content": "Say 'connection successful'"}],
            api_key=api_key,
            max_tokens=10
        )

        print(f"✅ 模型连接成功")
        print(f"   响应：{response.choices[0].message.content}")
        return True

    except Exception as e:
        print(f"❌ 模型连接失败：{str(e)}")
        print("   请检查：")
        print("   1. API Key 是否正确")
        print("   2. 网络连接是否正常")
        print("   3. Google 账户是否有权限访问 Gemini")
        return False


def check_agents_installed():
    """检查 OpenAI Agents SDK 是否安装"""
    print("\n📦 检查 OpenAI Agents SDK...")
    try:
        from agents import Agent, Runner
        print("✅ OpenAI Agents SDK 已安装")
        return True
    except ImportError as e:
        print(f"❌ OpenAI Agents SDK 未安装或导入失败：{e}")
        return False


def show_next_steps():
    """显示后续步骤"""
    print("\n" + "=" * 60)
    print("📋 后续步骤")
    print("=" * 60)

    api_key_set = os.getenv("GOOGLE_API_KEY") is not None

    if api_key_set:
        print("\n✅ 恭喜！您已配置好 Google Gemini + OpenAI Agents SDK")
        print("\n运行示例：")
        print("  1. python examples/basic/hello_world_google.py")
        print("  2. python examples/basic/hello_world_google_litellm.py")
        print("  3. uv run examples/model_providers/litellm_provider.py --model gemini/gemini-2.0-flash")
    else:
        print("\n请先完成以下步骤：")
        print("\n1️⃣ 获取 Google API Key：")
        print("   - 访问：https://aistudio.google.com/app/apikey")
        print("   - 创建新的 API Key")
        print("\n2️⃣ 设置环境变量：")
        print("   export GOOGLE_API_KEY='your_api_key_here'")
        print("\n3️⃣ 验证安装：")
        print("   python examples/basic/test_google_config.py")
        print("\n4️⃣ 运行测试：")
        print("   python examples/basic/hello_world_google.py")

    print("\n📚 更多信息请查看：")
    print("   examples/basic/GOOGLE_SETUP_GUIDE.md")


def main():
    """主函数"""
    print("=" * 60)
    print("  Google Gemini + OpenAI Agents SDK 配置验证")
    print("=" * 60)

    # 执行所有检查
    checks = [
        ("LiteLLM", check_litellm),
        ("Agents SDK", check_agents_installed),
        ("API Key", check_api_key),
    ]

    results = []
    for name, check_func in checks:
        results.append(check_func())

    # 测试连接（如果 API Key 已设置）
    test_model_connection()

    # 显示后续步骤
    show_next_steps()

    # 返回适当的退出代码
    if all(results):
        print("\n🎉 所有检查通过！")
        sys.exit(0)
    else:
        print("\n⚠️  部分检查失败，请查看上方说明")
        sys.exit(1)


if __name__ == "__main__":
    main()
