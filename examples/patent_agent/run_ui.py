"""
启动专利助手 Web 界面

运行命令：
python run_ui.py

或者直接使用 streamlit：
streamlit run ui/app.py
"""

import os
import sys
import subprocess

def check_dependencies():
    """检查依赖"""
    print("🔍 检查依赖...")
    required_packages = ['streamlit', 'google-generativeai']

    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"  ✓ {package}")
        except ImportError:
            print(f"  ✗ {package} (未安装)")
            missing_packages.append(package)

    if missing_packages:
        print(f"\n❌ 缺少依赖：{', '.join(missing_packages)}")
        print("请运行：pip install " + " ".join(missing_packages))
        return False

    print("\n✅ 所有依赖已安装")
    return True


def check_api_key():
    """检查 API 密钥"""
    print("\n🔑 检查 API 配置...")
    api_key = os.getenv("GOOGLE_API_KEY")

    if api_key:
        print(f"  ✓ API 密钥已配置：{api_key[:10]}...")
        return True
    else:
        print("  ✗ GOOGLE_API_KEY 未设置")
        print("\n请设置环境变量：")
        print("  export GOOGLE_API_KEY='your_google_api_key_here'")
        print("\n获取 API 密钥请访问：https://aistudio.google.com/app/apikey")
        return False


def launch_ui():
    """启动 UI"""
    print("\n🚀 启动专利助手 Web 界面...")
    print("\n" + "=" * 60)
    print("📄 专利助手 - AI 专利撰写与审查系统")
    print("=" * 60)
    print("\n界面将在浏览器中自动打开...")
    print("如果未自动打开，请手动访问：http://localhost:8501")
    print("\n按 Ctrl+C 停止服务")
    print("=" * 60 + "\n")

    # 启动 streamlit
    ui_path = os.path.join(os.path.dirname(__file__), "ui", "app.py")
    subprocess.run([
        sys.executable, "-m", "streamlit", "run", ui_path,
        "--server.port", "8501",
        "--server.address", "0.0.0.0",
        "--browser.gatherUsageStats", "false"
    ])


def main():
    """主函数"""
    print("\n" + "=" * 60)
    print("专利助手启动器")
    print("=" * 60)

    # 检查依赖
    if not check_dependencies():
        sys.exit(1)

    # 检查 API 密钥
    api_ok = check_api_key()

    if not api_ok:
        print("\n⚠️ 警告：API 密钥未配置，部分功能可能不可用")
        response = input("\n是否继续启动？(y/n): ")
        if response.lower() != 'y':
            sys.exit(0)

    # 启动 UI
    launch_ui()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 感谢使用专利助手！")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 启动失败：{e}")
        sys.exit(1)
