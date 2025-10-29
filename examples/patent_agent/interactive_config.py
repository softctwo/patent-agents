#!/usr/bin/env python3
"""
交互式API密钥配置助手
"""

import os
import sys
from dotenv import load_dotenv

def main():
    print("\n" + "=" * 70)
    print("🔑 专利附图绘制系统 - API密钥配置助手")
    print("=" * 70)
    
    # 加载.env文件
    load_dotenv()
    
    # 检查当前配置
    print("\n📊 当前配置状态:")
    print("-" * 70)
    
    google_key = os.getenv('GOOGLE_API_KEY')
    openai_key = os.getenv('OPENAI_API_KEY')
    
    # 检查Google API Key
    if google_key and google_key != 'your_gemini_api_key_here':
        print(f"✅ Google Gemini API Key: {google_key[:20]}...")
    else:
        print("❌ Google Gemini API Key: 未配置")
    
    # 检查OpenAI API Key
    if openai_key and openai_key != 'your_openai_api_key_here':
        print(f"✅ OpenAI API Key: {openai_key[:20]}...")
    else:
        print("⚠️  OpenAI API Key: 未配置（可选）")
    
    print()
    
    # 提供配置选项
    print("请选择配置方式:")
    print("1. 编辑.env文件（永久配置）")
    print("2. 设置环境变量（临时配置）")
    print("3. 退出")
    
    while True:
        choice = input("\n请输入选项 (1-3): ").strip()
        
        if choice == '1':
            print("\n📝 请手动编辑 .env 文件:")
            print("文件路径:", os.path.abspath('.env'))
            print("\n示例内容:")
            print("GOOGLE_API_KEY=AIzaSyxxxxxxxxxxxxxxxxxxxxx")
            print("OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxx")
            print("\n💡 提示: 保存文件后重新运行此脚本验证")
            input("\n按回车键继续...")
            break
            
        elif choice == '2':
            print("\n💡 请在终端中执行:")
            print("export GOOGLE_API_KEY='您的真实密钥'")
            print("export OPENAI_API_KEY='您的真实密钥（可选）'")
            input("\n设置完成后按回车键继续...")
            break
            
        elif choice == '3':
            print("\n👋 再见!")
            sys.exit(0)
            
        else:
            print("\n❌ 无效选项，请重新输入")
    
    # 重新检查
    print("\n" + "=" * 70)
    print("🔍 重新检查配置...")
    print("=" * 70)
    
    load_dotenv()
    google_key = os.getenv('GOOGLE_API_KEY')
    
    if google_key and google_key != 'your_gemini_api_key_here':
        print("\n✅ 配置成功!")
        print("🔑 API Key: ", google_key[:20] + "...")
        print("\n🚀 您现在可以:")
        print("   1. 运行 python test_ai_drawing.py 测试AI绘图")
        print("   2. 运行 python test_gemini_drawing_demo.py 查看演示")
        print("   3. 在代码中直接使用AI绘图功能")
    else:
        print("\n❌ 配置失败或未保存")
        print("\n💡 请确保:")
        print("   1. 密钥格式正确（以AIzaSy开头）")
        print("   2. 文件已保存")
        print("   3. 重新运行此脚本验证")
    
    print("\n" + "=" * 70)

if __name__ == "__main__":
    main()
