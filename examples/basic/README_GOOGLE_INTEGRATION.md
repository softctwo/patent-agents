# Google Gemini + OpenAI Agents SDK 完整配置

本示例展示了如何配置和使用 Google Gemini 模型与 OpenAI Agents SDK。

## 📋 配置摘要

### ✅ 已验证的工作流程

1. **LiteLLM 已安装** - 用于连接 Google Gemini
2. **OpenAI Agents SDK 已安装** - 核心框架
3. **示例脚本已创建** - 3 种不同的使用方式
4. **配置验证脚本已创建** - 用于检查配置状态

## 📁 文件结构

```
examples/basic/
├── hello_world_fake_model.py          # 使用模拟模型的测试（无需 API 密钥）
├── hello_world_google.py              # 使用 LiteLLM 内置支持（简单方式）
├── hello_world_google_litellm.py      # 使用 LitellmModel（灵活配置）
├── test_google_config.py              # 配置验证脚本
├── GOOGLE_SETUP_GUIDE.md              # 详细配置指南
└── README_GOOGLE_INTEGRATION.md       # 本文件
```

## 🚀 快速开始

### 步骤 1：获取 Google API Key

1. 访问 [Google AI Studio](https://aistudio.google.com/app/apikey)
2. 登录您的 Google 账户
3. 点击 "Create API Key"
4. 复制生成的 API Key

### 步骤 2：设置环境变量

```bash
export GOOGLE_API_KEY="your_actual_api_key_here"
```

### 步骤 3：验证配置

```bash
python examples/basic/test_google_config.py
```

### 步骤 4：运行示例

#### 方式 1：使用 LiteLLM 前缀（推荐）
```bash
python examples/basic/hello_world_google.py
```

#### 方式 2：使用 LitellmModel
```bash
python examples/basic/hello_world_google_litellm.py
```

#### 方式 3：使用 uv（项目推荐）
```bash
export GOOGLE_API_KEY="your_api_key_here"
uv run examples/model_providers/litellm_provider.py --model gemini/gemini-2.0-flash
```

## 💡 使用示例

### 基本示例（Haiku 模式）

```python
import asyncio
from agents import Agent, Runner, set_tracing_disabled

set_tracing_disabled(disabled=True)

async def main():
    agent = Agent(
        name="Assistant",
        instructions="You only respond in haikus.",
        model="gemini/gemini-2.0-flash",  # 使用 LiteLLM 前缀
    )

    result = await Runner.run(agent, "Tell me about recursion.")
    print(result.final_output)

asyncio.run(main())
```

### 使用工具函数的示例

```python
import asyncio
from agents import Agent, Runner, function_tool

@function_tool
def get_weather(city: str):
    return f"The weather in {city} is sunny."

async def main():
    agent = Agent(
        name="Assistant",
        instructions="You only respond in haikus.",
        model="gemini/gemini-2.0-flash",
        tools=[get_weather],
    )

    result = await Runner.run(agent, "What's the weather in Tokyo?")
    print(result.final_output)

asyncio.run(main())
```

### 使用 LitellmModel 的示例

```python
import asyncio
from agents import Agent, Runner
from agents.extensions.models.litellm_model import LitellmModel

async def main():
    model = LitellmModel(
        model="gemini/gemini-2.0-flash",
        api_key="your_api_key_here"
    )

    agent = Agent(
        name="Assistant",
        instructions="You are a helpful assistant.",
        model=model,
    )

    result = await Runner.run(agent, "Hello!")
    print(result.final_output)

asyncio.run(main())
```

## 🔧 故障排除

### 问题 1：API Key 未设置

**错误信息：**
```
错误：请设置 GOOGLE_API_KEY 环境变量
```

**解决方案：**
```bash
export GOOGLE_API_KEY="your_api_key_here"
```

### 问题 2：API Key 无效

**错误信息：**
```
Error: 401 Unauthorized
```

**解决方案：**
1. 检查 API Key 是否正确
2. 访问 [Google AI Studio](https://aistudio.google.com/app/apikey) 重新生成
3. 确保 API Key 没有过期

### 问题 3：模型不存在

**错误信息：**
```
Error: Model not found
```

**解决方案：**
使用以下支持的模型之一：
- `gemini/gemini-2.0-flash` （推荐）
- `gemini/gemini-1.5-pro`
- `gemini/gemini-pro`

### 问题 4：LiteLLM 未安装

**错误信息：**
```
ImportError: No module named 'litellm'
```

**解决方案：**
```bash
pip install litellm
# 或者
uv add litellm
```

## 📊 支持的 Google 模型

| 模型 | 描述 | 特点 | 推荐场景 |
|------|------|------|----------|
| `gemini/gemini-2.0-flash` | 最新高性能模型 | 快速、低延迟 | 实时交互、快速响应 |
| `gemini/gemini-1.5-pro` | 长上下文模型 | 大上下文窗口 | 文档分析、复杂推理 |
| `gemini/gemini-pro` | 标准模型 | 平衡性能 | 一般任务 |

## 🎯 测试验证

运行 `test_google_config.py` 脚本可以验证：

- ✅ LiteLLM 是否正确安装
- ✅ Google API Key 是否设置
- ✅ OpenAI Agents SDK 是否可用
- ✅ 模型连接是否正常

## 📚 参考资源

- [Google AI Studio](https://aistudio.google.com/app/apikey)
- [OpenAI Agents SDK 文档](https://openai.github.io/openai-agents-python/)
- [LiteLLM 文档](https://docs.litellm.ai/docs/)
- [支持的模型列表](https://docs.litellm.ai/docs/providers)

## 🆘 需要帮助？

1. 查看配置验证输出：
   ```bash
   python examples/basic/test_google_config.py
   ```

2. 查看详细配置指南：
   - `examples/basic/GOOGLE_SETUP_GUIDE.md`

3. 运行模拟测试（无需 API 密钥）：
   ```bash
   python examples/basic/hello_world_fake_model.py
   ```

---

**注意**：本配置基于 [OpenAI Agents SDK LiteLLM 支持](https://openai.github.io/openai-agents-python/models/litellm/)
