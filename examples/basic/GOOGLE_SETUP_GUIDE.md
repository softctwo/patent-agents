# OpenAI Agents SDK + Google Gemini 配置指南

本指南将帮助您配置和使用 Google Gemini 模型与 OpenAI Agents SDK。

## 前提条件

1. **获取 Google API Key**
   - 访问 [Google AI Studio](https://aistudio.google.com/app/apikey)
   - 点击 "Create API Key"
   - 复制生成的 API Key

2. **确保安装了 litellm**
   ```bash
   pip install litellm
   ```

## 配置方法

### 方法 1：使用环境变量（推荐）

1. **设置环境变量**
   ```bash
   export GOOGLE_API_KEY="your_actual_api_key_here"
   ```

2. **运行示例脚本**
   ```bash
   python examples/basic/hello_world_google.py
   ```

### 方法 2：使用 LitellmModel 直接配置

1. **运行带参数的脚本**
   ```bash
   python examples/basic/hello_world_google_litellm.py
   ```

2. **按提示输入您的 Google API Key**

### 方法 3：使用 uv（项目推荐方式）

1. **设置环境变量**
   ```bash
   export GOOGLE_API_KEY="your_actual_api_key_here"
   ```

2. **运行示例**
   ```bash
   uv run examples/model_providers/litellm_provider.py --model gemini/gemini-2.0-flash
   ```

## 支持的 Google 模型

| 模型名称 | 描述 | 推荐使用场景 |
|---------|------|-------------|
| `gemini/gemini-2.0-flash` | 最新高性能模型 | 快速响应、一般任务 |
| `gemini/gemini-1.5-pro` | 长上下文模型 | 复杂推理、长文档 |
| `gemini/gemini-pro` | 标准模型 | 平衡性能和速度 |

更多模型信息请参考 [LiteLLM 文档](https://docs.litellm.ai/docs/providers)

## 示例输出

配置成功后，您应该看到类似输出：

```
正在运行 Google Gemini 2.0 Flash 模型...
输入：Tell me about recursion in programming.

输出：
Functions calling themselves,
Recursion like nested dolls,
Beauty in the pattern.

✅ 测试成功完成！
```

## 常见错误

### 错误 1：API Key 未设置
```
错误：请设置 GOOGLE_API_KEY 环境变量
```
**解决方案**：按照上面的步骤设置环境变量

### 错误 2：API Key 无效
```
Error: 401 Unauthorized
```
**解决方案**：
1. 检查 API Key 是否正确
2. 确保 API Key 没有过期
3. 检查 Google Cloud Console 中的 API 访问权限

### 错误 3：模型不存在
```
Error: Model not found
```
**解决方案**：
1. 检查模型名称是否正确
2. 确保您的 Google 账户有权限访问该模型
3. 尝试使用 `gemini/gemini-2.0-flash` 作为默认模型

## 高级配置

### 使用自定义模型参数

```python
from agents import Agent
from agents.extensions.models.litellm_model import LitellmModel

model = LitellmModel(
    model="gemini/gemini-2.0-flash",
    api_key="your_api_key",
    # 添加其他参数...
)

agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant.",
    model=model,
)
```

### 使用工具函数

```python
from agents import Agent, Runner, function_tool

@function_tool
def get_weather(city: str):
    return f"The weather in {city} is sunny."

agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant.",
    model="gemini/gemini-2.0-flash",
    tools=[get_weather],
)

result = await Runner.run(agent, "What's the weather in Tokyo?")
```

## 故障排除

1. **检查环境变量**
   ```bash
   echo $GOOGLE_API_KEY
   ```

2. **验证 litellm 安装**
   ```bash
   pip show litellm
   ```

3. **测试 API 连接**
   ```python
   import litellm
   response = litellm.completion(
       model="gemini/gemini-2.0-flash",
       messages=[{"role": "user", "content": "Hello"}],
       api_key="your_api_key"
   )
   print(response)
   ```

## 参考资源

- [Google AI Studio](https://aistudio.google.com/app/apikey)
- [OpenAI Agents SDK 文档](https://openai.github.io/openai-agents-python/)
- [LiteLLM 文档](https://docs.litellm.ai/docs/)
- [支持的模型列表](https://docs.litellm.ai/docs/providers)
