# 🔐 环境变量配置指南

## 📋 概述

专利附图绘制系统使用`.env`文件管理API密钥等敏感配置。本指南将帮助您正确配置环境变量。

## 🚀 快速开始

### 步骤1：复制配置模板

```bash
cp .env.example .env
```

### 步骤2：编辑.env文件

```bash
# 使用您喜欢的编辑器
nano .env
# 或
vim .env
# 或
code .env
```

### 步骤3：配置API密钥

在`.env`文件中填入您的真实API密钥：

```env
GOOGLE_API_KEY=AIzaSyC-xxxxxxxxxxxxxxxxxxxxxxxxx
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

## 🔑 API密钥获取

### Google Gemini API Key（推荐 - 必需）

1. **访问Google AI Studio**
   - 网址：https://aistudio.google.com/app/apikey

2. **创建API密钥**
   - 点击"Create API Key"按钮
   - 选择您的Google账号
   - 复制生成的API密钥

3. **格式示例**
   ```
   GOOGLE_API_KEY=AIzaSyC-1a2b3c4d5e6f7g8h9i0jklmnopqrstuvwxyz1234567890
   ```

### OpenAI API Key（可选 - 用于专利撰写）

1. **访问OpenAI Platform**
   - 网址：https://platform.openai.com/api-keys

2. **创建API密钥**
   - 点击"Create new secret key"
   - 输入密钥名称（如：patent-agent）
   - 复制生成的密钥（以`sk-`开头）

3. **格式示例**
   ```
   OPENAI_API_KEY=sk-1a2b3c4d5e6f7g8h9i0jklmnopqrstuvwxyz1234567890
   ```

## ✅ 验证配置

### 方法1：运行测试脚本

```bash
python test_ai_drawing.py
```

预期输出：
```
✅ Gemini-2.5-Pro AI模型初始化成功（从.env文件加载）
```

### 方法2：Python代码测试

```python
import os
from dotenv import load_dotenv

# 加载.env文件
load_dotenv()

# 检查API密钥
api_key = os.getenv("GOOGLE_API_KEY")
if api_key and api_key != "your_gemini_api_key_here":
    print("✅ Google API Key 已配置")
else:
    print("❌ Google API Key 未配置")
```

## 🛡️ 安全注意事项

### ✅ 应该做的
- 使用`.env`文件存储敏感信息
- 将`.env`添加到`.gitignore`中（已配置）
- 定期轮换API密钥
- 为不同环境使用不同的密钥

### ❌ 不应该做的
- 不要将API密钥提交到Git
- 不要在代码中硬编码密钥
- 不要与他人共享API密钥
- 不要在公共场所展示密钥

## 📁 文件结构

```
patent_agent/
├── .env                 # 您的私有配置文件（不提交到Git）
├── .env.example         # 配置模板（可提交到Git）
├── .env.local           # 本地开发配置（可选）
└── .gitignore          # 已包含.env文件排除规则
```

## 🔧 高级配置

### 环境变量优先级

1. **系统环境变量**（最高优先级）
   ```bash
   export GOOGLE_API_KEY=your_key
   python script.py
   ```

2. **.env文件**（中等优先级）
   ```bash
   # 在.env文件中
   GOOGLE_API_KEY=your_key
   ```

3. **默认值**（最低优先级）
   ```python
   api_key = os.getenv("GOOGLE_API_KEY", "default_key")
   ```

### 多环境配置

创建不同环境的配置文件：

```bash
.env.development    # 开发环境
.env.staging        # 测试环境
.env.production     # 生产环境
```

使用时指定环境文件：

```python
from dotenv import load_dotenv

# 加载指定环境的配置
load_dotenv('.env.development')
```

## ❓ 常见问题

### Q1：API密钥无效或过期？

**A：** 检查以下几点：
- 密钥是否正确复制（无额外空格）
- 密钥是否仍在有效期内
- 是否已启用相关API服务
- 网络连接是否正常

### Q2：提示"未设置GOOGLE_API_KEY"？

**A：** 按以下步骤排查：
1. 确认`.env`文件位于项目根目录
2. 确认文件名为`.env`（不是`.env.txt`）
3. 确认文件内容格式正确（无多余空格或引号）
4. 重新启动Python解释器

### Q3：如何查看当前加载的环境变量？

**A：** 运行此代码：

```python
import os
from dotenv import load_dotenv

load_dotenv()

# 查看所有环境变量（谨慎使用，生产环境请删除）
print("所有环境变量：", dict(os.environ))

# 只查看相关变量
print("GOOGLE_API_KEY:", os.getenv("GOOGLE_API_KEY")[:10] + "..." if os.getenv("GOOGLE_API_KEY") else "未设置")
```

### Q4：可以同时使用.env文件和系统环境变量吗？

**A：** 可以，系统环境变量优先级更高。

## 📞 技术支持

如果遇到配置问题：

1. **检查日志**
   - 查看Python控制台输出的错误信息
   - 检查是否正确加载了.env文件

2. **验证API密钥**
   - 确认API密钥格式正确
   - 确认API密钥有效且未过期

3. **查看文档**
   - Google AI文档：https://ai.google.dev/
   - OpenAI文档：https://platform.openai.com/docs/

## 📝 更新日志

| 日期 | 版本 | 更新内容 |
|------|------|----------|
| 2025-10-30 | v1.0 | 初始版本，集成.env配置 |

---

**配置完成后，您的系统将能够：**
- ✅ 使用Gemini-2.5-Pro生成高质量专利附图
- ✅ 支持AI驱动的智能布局
- ✅ 自动加载API密钥（无需手动设置环境变量）
- ✅ 安全存储敏感信息

🎉 **祝您使用愉快！**
