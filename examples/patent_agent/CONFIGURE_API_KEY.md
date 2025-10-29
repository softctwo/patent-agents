# 🔑 API密钥配置指南

## 当前状态
❌ .env文件中的密钥仍为示例值

## 需要您做的操作

### 方法1：直接编辑.env文件（推荐）

```bash
cd /Users/zhangyanlong/workspaces/openai-agents-python/examples/patent_agent
nano .env
```

将文件内容改为：

```env
GOOGLE_API_KEY=您的真实Gemini密钥（以AIzaSy开头）
OPENAI_API_KEY=您的真实OpenAI密钥（可选，以sk-开头）
```

### 方法2：通过命令行设置（临时）

```bash
export GOOGLE_API_KEY="您的真实Gemini密钥"
export OPENAI_API_KEY="您的真实OpenAI密钥（可选）"
```

### 方法3：通过Python设置（临时）

```python
import os
os.environ['GOOGLE_API_KEY'] = '您的真实Gemini密钥'
```

## 如何获取API密钥

### Google Gemini API Key（必需）
1. 访问：https://aistudio.google.com/app/apikey
2. 点击"Create API Key"
3. 复制生成的密钥（格式：AIzaSy...）

### OpenAI API Key（可选）
1. 访问：https://platform.openai.com/api-keys
2. 点击"Create new secret key"
3. 复制生成的密钥（格式：sk-...）

## 验证配置

配置后运行：

```bash
python -c "
import os
from dotenv import load_dotenv
load_dotenv()
key = os.getenv('GOOGLE_API_KEY')
if key and key != 'your_gemini_api_key_here':
    print('✅ Google API Key 已配置')
else:
    print('❌ Google API Key 未配置')
"
```

## 配置成功后

您将看到：

```
✅ Gemini-2.5-Pro AI模型初始化成功（从.env文件加载）
✅ 附图生成成功
```

🎯 **配置完成后，您的附图质量将大幅提升！**
