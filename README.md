<<<<<<< HEAD
# OpenAI Agents SDK [![PyPI](https://img.shields.io/pypi/v/openai-agents?label=pypi%20package)](https://pypi.org/project/openai-agents/)

The OpenAI Agents SDK is a lightweight yet powerful framework for building multi-agent workflows. It is provider-agnostic, supporting the OpenAI Responses and Chat Completions APIs, as well as 100+ other LLMs.

<img src="https://cdn.openai.com/API/docs/images/orchestration.png" alt="Image of the Agents Tracing UI" style="max-height: 803px;">

> [!NOTE]
> Looking for the JavaScript/TypeScript version? Check out [Agents SDK JS/TS](https://github.com/openai/openai-agents-js).

### Core concepts:

1. [**Agents**](https://openai.github.io/openai-agents-python/agents): LLMs configured with instructions, tools, guardrails, and handoffs
2. [**Handoffs**](https://openai.github.io/openai-agents-python/handoffs/): A specialized tool call used by the Agents SDK for transferring control between agents
3. [**Guardrails**](https://openai.github.io/openai-agents-python/guardrails/): Configurable safety checks for input and output validation
4. [**Sessions**](#sessions): Automatic conversation history management across agent runs
5. [**Tracing**](https://openai.github.io/openai-agents-python/tracing/): Built-in tracking of agent runs, allowing you to view, debug and optimize your workflows

Explore the [examples](examples) directory to see the SDK in action, and read our [documentation](https://openai.github.io/openai-agents-python/) for more details.

## Get started

To get started, set up your Python environment (Python 3.9 or newer required), and then install OpenAI Agents SDK package.

### venv

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install openai-agents
```

For voice support, install with the optional `voice` group: `pip install 'openai-agents[voice]'`.

For Redis session support, install with the optional `redis` group: `pip install 'openai-agents[redis]'`.

### uv

If you're familiar with [uv](https://docs.astral.sh/uv/), using the tool would be even similar:

```bash
uv init
uv add openai-agents
```

For voice support, install with the optional `voice` group: `uv add 'openai-agents[voice]'`.

For Redis session support, install with the optional `redis` group: `uv add 'openai-agents[redis]'`.

## Hello world example

```python
from agents import Agent, Runner

agent = Agent(name="Assistant", instructions="You are a helpful assistant")

result = Runner.run_sync(agent, "Write a haiku about recursion in programming.")
print(result.final_output)

# Code within the code,
# Functions calling themselves,
# Infinite loop's dance.
```

(_If running this, ensure you set the `OPENAI_API_KEY` environment variable_)

(_For Jupyter notebook users, see [hello_world_jupyter.ipynb](examples/basic/hello_world_jupyter.ipynb)_)

## Handoffs example

```python
from agents import Agent, Runner
import asyncio

spanish_agent = Agent(
    name="Spanish agent",
    instructions="You only speak Spanish.",
)

english_agent = Agent(
    name="English agent",
    instructions="You only speak English",
)

triage_agent = Agent(
    name="Triage agent",
    instructions="Handoff to the appropriate agent based on the language of the request.",
    handoffs=[spanish_agent, english_agent],
)


async def main():
    result = await Runner.run(triage_agent, input="Hola, ¿cómo estás?")
    print(result.final_output)
    # ¡Hola! Estoy bien, gracias por preguntar. ¿Y tú, cómo estás?


if __name__ == "__main__":
    asyncio.run(main())
```

## Functions example

```python
import asyncio

from agents import Agent, Runner, function_tool


@function_tool
def get_weather(city: str) -> str:
    return f"The weather in {city} is sunny."


agent = Agent(
    name="Hello world",
    instructions="You are a helpful agent.",
    tools=[get_weather],
)


async def main():
    result = await Runner.run(agent, input="What's the weather in Tokyo?")
    print(result.final_output)
    # The weather in Tokyo is sunny.


if __name__ == "__main__":
    asyncio.run(main())
```

## The agent loop

When you call `Runner.run()`, we run a loop until we get a final output.

1. We call the LLM, using the model and settings on the agent, and the message history.
2. The LLM returns a response, which may include tool calls.
3. If the response has a final output (see below for more on this), we return it and end the loop.
4. If the response has a handoff, we set the agent to the new agent and go back to step 1.
5. We process the tool calls (if any) and append the tool responses messages. Then we go to step 1.

There is a `max_turns` parameter that you can use to limit the number of times the loop executes.

### Final output

Final output is the last thing the agent produces in the loop.

1.  If you set an `output_type` on the agent, the final output is when the LLM returns something of that type. We use [structured outputs](https://platform.openai.com/docs/guides/structured-outputs) for this.
2.  If there's no `output_type` (i.e. plain text responses), then the first LLM response without any tool calls or handoffs is considered as the final output.

As a result, the mental model for the agent loop is:

1. If the current agent has an `output_type`, the loop runs until the agent produces structured output matching that type.
2. If the current agent does not have an `output_type`, the loop runs until the current agent produces a message without any tool calls/handoffs.

## Common agent patterns

The Agents SDK is designed to be highly flexible, allowing you to model a wide range of LLM workflows including deterministic flows, iterative loops, and more. See examples in [`examples/agent_patterns`](examples/agent_patterns).

## Tracing

The Agents SDK automatically traces your agent runs, making it easy to track and debug the behavior of your agents. Tracing is extensible by design, supporting custom spans and a wide variety of external destinations, including [Logfire](https://logfire.pydantic.dev/docs/integrations/llms/openai/#openai-agents), [AgentOps](https://docs.agentops.ai/v1/integrations/agentssdk), [Braintrust](https://braintrust.dev/docs/guides/traces/integrations#openai-agents-sdk), [Scorecard](https://docs.scorecard.io/docs/documentation/features/tracing#openai-agents-sdk-integration), and [Keywords AI](https://docs.keywordsai.co/integration/development-frameworks/openai-agent). For more details about how to customize or disable tracing, see [Tracing](http://openai.github.io/openai-agents-python/tracing), which also includes a larger list of [external tracing processors](http://openai.github.io/openai-agents-python/tracing/#external-tracing-processors-list).

## Long running agents & human-in-the-loop

You can use the Agents SDK [Temporal](https://temporal.io/) integration to run durable, long-running workflows, including human-in-the-loop tasks. View a demo of Temporal and the Agents SDK working in action to complete long-running tasks [in this video](https://www.youtube.com/watch?v=fFBZqzT4DD8), and [view docs here](https://github.com/temporalio/sdk-python/tree/main/temporalio/contrib/openai_agents).

## Sessions

The Agents SDK provides built-in session memory to automatically maintain conversation history across multiple agent runs, eliminating the need to manually handle `.to_input_list()` between turns.

### Quick start

```python
from agents import Agent, Runner, SQLiteSession

# Create agent
agent = Agent(
    name="Assistant",
    instructions="Reply very concisely.",
)

# Create a session instance
session = SQLiteSession("conversation_123")

# First turn
result = await Runner.run(
    agent,
    "What city is the Golden Gate Bridge in?",
    session=session
)
print(result.final_output)  # "San Francisco"

# Second turn - agent automatically remembers previous context
result = await Runner.run(
    agent,
    "What state is it in?",
    session=session
)
print(result.final_output)  # "California"

# Also works with synchronous runner
result = Runner.run_sync(
    agent,
    "What's the population?",
    session=session
)
print(result.final_output)  # "Approximately 39 million"
```

### Session options

-   **No memory** (default): No session memory when session parameter is omitted
-   **`session: Session = DatabaseSession(...)`**: Use a Session instance to manage conversation history

```python
from agents import Agent, Runner, SQLiteSession

# SQLite - file-based or in-memory database
session = SQLiteSession("user_123", "conversations.db")

# Redis - for scalable, distributed deployments
# from agents.extensions.memory import RedisSession
# session = RedisSession.from_url("user_123", url="redis://localhost:6379/0")

agent = Agent(name="Assistant")

# Different session IDs maintain separate conversation histories
result1 = await Runner.run(
    agent,
    "Hello",
    session=session
)
result2 = await Runner.run(
    agent,
    "Hello",
    session=SQLiteSession("user_456", "conversations.db")
)
```

### Custom session implementations

You can implement your own session memory by creating a class that follows the `Session` protocol:

```python
from agents.memory import Session
from typing import List

class MyCustomSession:
    """Custom session implementation following the Session protocol."""

    def __init__(self, session_id: str):
        self.session_id = session_id
        # Your initialization here

    async def get_items(self, limit: int | None = None) -> List[dict]:
        # Retrieve conversation history for the session
        pass

    async def add_items(self, items: List[dict]) -> None:
        # Store new items for the session
        pass

    async def pop_item(self) -> dict | None:
        # Remove and return the most recent item from the session
        pass

    async def clear_session(self) -> None:
        # Clear all items for the session
        pass

# Use your custom session
agent = Agent(name="Assistant")
result = await Runner.run(
    agent,
    "Hello",
    session=MyCustomSession("my_session")
)
```

## Development (only needed if you need to edit the SDK/examples)

0. Ensure you have [`uv`](https://docs.astral.sh/uv/) installed.

```bash
uv --version
```

1. Install dependencies

```bash
make sync
```

2. (After making changes) lint/test

```
make check # run tests linter and typechecker
```

Or to run them individually:

```
make tests  # run tests
make mypy   # run typechecker
make lint   # run linter
make format-check # run style checker
```

## Acknowledgements

We'd like to acknowledge the excellent work of the open-source community, especially:

-   [Pydantic](https://docs.pydantic.dev/latest/) (data validation) and [PydanticAI](https://ai.pydantic.dev/) (advanced agent framework)
-   [LiteLLM](https://github.com/BerriAI/litellm) (unified interface for 100+ LLMs)
-   [MkDocs](https://github.com/squidfunk/mkdocs-material)
-   [Griffe](https://github.com/mkdocstrings/griffe)
-   [uv](https://github.com/astral-sh/uv) and [ruff](https://github.com/astral-sh/ruff)

We're committed to continuing to build the Agents SDK as an open source framework so others in the community can expand on our approach.
=======
# 专利撰写和审查 Agent 系统

基于 OpenAI Agents SDK 的智能专利工作流系统，提供专利撰写、预审、附图审查和检索功能。

## 系统架构

本系统采用多 Agent 架构设计，主要包括：

### 核心组件

1. **专利撰写 Agent**
   - 根据发明描述自动生成专利申请文件
   - 支持多种专利类型（发明、实用新型、外观设计）
   - 生成标准格式的申请文档

2. **专利预审 Agent**
   - 审查专利申请文件的完整性和规范性
   - 可配置的审查规则
   - 生成详细的审查报告

3. **附图审查 Agent**
   - 审查附图格式、质量和规范
   - 检查附图引用的一致性
   - 确保符合专利局要求

4. **专利检索 Agent**
   - 集成多个专利数据库
   - 智能相似度计算
   - 生成检索分析报告

### 系统特性

- ✅ **模块化设计**：各功能模块独立，可灵活组合
- ✅ **可配置规则**：审查规则可根据需求自定义
- ✅ **多数据库支持**：支持 CNIPA、Google Patents、Espacenet 等
- ✅ **标准化输出**：符合专利局格式要求
- ✅ **完整工作流**：支持端到端的专利申请流程

## 安装和使用

### 环境要求

- Python 3.9+
- OpenAI Agents SDK

### 安装依赖

```bash
pip install pydantic agents
```

### 快速开始

#### 1. 撰写专利申请文件

```python
from agents import Runner
from examples.patent_agent import patent_agent

async def write_patent():
    prompt = """
    请撰写一份关于"基于机器学习的智能诊断系统"的发明专利申请文件。
    技术领域：人工智能、医疗诊断
    发明描述：该系统通过深度学习算法分析医疗影像...
    申请人：北京医疗科技有限公司
    """

    result = await Runner.run(patent_agent, prompt)
    print(result.final_output)
```

#### 2. 检索现有技术

```python
async def search_patents():
    prompt = """
    请检索与"人工智能诊断"相关的专利，重点关注深度学习和医疗影像领域。
    """

    result = await Runner.run(patent_agent, prompt)
    print(result.final_output)
```

#### 3. 审查申请文件

```python
async def review_application():
    # 假设已有申请文件
    application_text = "专利申请文件内容..."

    prompt = f"""
    请审查以下专利申请文件：
    {application_text}
    """

    result = await Runner.run(patent_agent, prompt)
    print(result.final_output)
```

#### 4. 审查附图

```python
async def review_figures():
    prompt = """
    请审查以下专利附图：
    - 附图1：系统架构图（300 DPI，PNG格式）
    - 附图2：算法流程图（300 DPI，PNG格式）
    - 附图3：界面示意图（300 DPI，PNG格式）
    """

    result = await Runner.run(patent_agent, prompt)
    print(result.final_output)
```

#### 5. 配置审查规则

```python
async def configure_rules():
    # 查看当前规则
    prompt = "请显示所有可用的审查规则"

    # 启用/禁用规则
    prompt = "请启用规则 PRE001"
```

## 运行演示

系统提供了完整的演示程序：

```bash
cd /Users/zhangyanlong/workspaces/openai-agents-python/examples/patent_agent
python demo.py
```

演示包括：
1. 专利撰写功能
2. 专利检索功能
3. 专利预审功能
4. 附图审查功能
5. 规则配置功能
6. 完整工作流

## 系统架构详解

### 数据模型

#### 专利申请文件 (PatentApplication)

```python
{
    "title": "专利标题",
    "patent_type": "invention|utility_model|design",
    "applicant": {
        "name": "申请人姓名",
        "address": "地址",
        "country": "国家"
    },
    "inventors": [{"name": "发明人"}],
    "technical_field": "技术领域",
    "background_tech": "背景技术",
    "invention_content": "发明内容",
    "beneficial_effects": "有益效果",
    "claims": [{"claim_number": 1, "content": "权利要求"}],
    "figures": [{"figure_number": 1, "description": "附图说明"}]
}
```

#### 审查规则 (ReviewRule)

```python
{
    "rule_id": "PRE001",
    "name": "标题长度检查",
    "severity": "warning|error|info",
    "check_logic": {
        "type": "length|required|compound|claims",
        "field": "字段名",
        "min": 5,
        "max": 50
    }
}
```

### 工具模块

#### 1. PatentWriter

专利撰写工具，负责根据需求生成专利申请文件。

**主要方法：**
- `generate_patent_application()`: 生成专利申请文件
- `format_application()`: 格式化输出
- `export_to_xml()`: 导出 XML 格式

#### 2. PatentSearchTool

专利检索工具，支持多数据库检索。

**主要方法：**
- `search_patents()`: 执行专利检索
- `calculate_similarity()`: 计算相似度
- `generate_report()`: 生成检索报告

**支持的数据源：**
- CNIPA（中国专利数据库）
- Google Patents
- Espacenet（欧洲专利数据库）

#### 3. PatentPreReviewer

专利预审工具，检查申请文件的完整性和规范性。

**主要方法：**
- `review_application()`: 执行预审
- `generate_report()`: 生成审查报告

**检查项目：**
- 标题长度检查
- 技术领域完整性
- 背景技术检查
- 发明内容检查
- 权利要求书检查
- 附图说明检查

#### 4. PatentFigureReviewer

附图审查工具，确保附图符合要求。

**主要方法：**
- `review_figures()`: 执行附图审查
- `generate_report()`: 生成审查报告

**检查项目：**
- 图片清晰度检查
- 图片格式检查
- 图号标注检查
- 附图引用检查
- 附图标记检查

### 审查规则系统

系统支持可配置的审查规则，可根据不同需求定制：

#### 预审规则示例

```python
ReviewRule(
    rule_id="PRE001",
    name="标题长度检查",
    severity=ReviewSeverity.WARNING,
    check_logic={
        "type": "length",
        "field": "title",
        "min": 5,
        "max": 50
    }
)
```

#### 附图审查规则示例

```python
ReviewRule(
    rule_id="FIG001",
    name="图片清晰度检查",
    severity=ReviewSeverity.ERROR,
    check_logic={
        "type": "image_quality",
        "min_dpi": 300,
        "check_sharpness": True
    }
)
```

## 高级功能

### 1. 自定义审查规则

```python
from examples.patent_agent.config import RuleManager, ReviewRule, ReviewSeverity

rule_manager = RuleManager()

# 添加自定义规则
custom_rule = ReviewRule(
    rule_id="CUSTOM001",
    name="自定义检查项",
    severity=ReviewSeverity.ERROR,
    check_logic={...}
)
rule_manager.add_rule("pre_review", custom_rule)

# 启用/禁用规则
rule_manager.enable_rule("pre_review", "PRE001", False)
```

### 2. 多引擎检索

```python
from examples.patent_agent.tools import PatentSearchTool

search_tool = PatentSearchTool()

# 使用特定搜索引擎
result = await search_tool.search_patents(
    query,
    use_engines=["cnipa", "google_patents"]
)

# 配置检索参数
search_tool.config["min_similarity_score"] = 0.8
```

### 3. 批量处理

```python
# 批量撰写专利
requests = [draft_request_1, draft_request_2, ...]
for req in requests:
    application = patent_writer.generate_patent_application(req)
    # 保存或处理

# 批量检索
keywords_list = [
    ["人工智能", "推荐系统"],
    ["区块链", "身份认证"],
    ...
]
for keywords in keywords_list:
    result = await search_tool.search_patents(PatentSearchQuery(keywords=keywords))
```

## 输出格式

### 1. 专利申请文件格式

系统支持多种输出格式：

- **文本格式**：易于阅读和编辑
- **XML 格式**：符合专利局标准
- **JSON 格式**：便于程序处理

```python
# 文本格式
formatted_text = patent_writer.format_application(application)

# XML 格式
xml_content = patent_writer.export_to_xml(application)
```

### 2. 审查报告格式

- **结构化报告**：包含问题统计、详细问题、建议
- **评分系统**：0-100 分评分
- **严重程度分级**：错误、警告、提示

### 3. 检索报告格式

- **统计信息**：总结果数、相关性分布
- **分析内容**：新颖性分析、相似性分析
- **检索结果**：按相似度排序的相关专利
- **建议**：基于结果的改进建议

## 最佳实践

### 1. 专利撰写

- **详细描述**：提供尽可能详细的发明描述
- **技术领域**：明确技术领域和分类
- **背景技术**：分析现有技术问题
- **技术方案**：清晰描述解决方案
- **有益效果**：突出发明的优势

### 2. 专利检索

- **关键词策略**：使用多种关键词组合
- **多数据库检索**：交叉验证检索结果
- **相关度阈值**：设置合适的相似度阈值
- **定期更新**：及时更新检索策略

### 3. 审查流程

- **预审优先**：先进行预审发现问题
- **附图审查**：确保附图符合要求
- **规则配置**：根据专利类型调整规则
- **迭代改进**：根据审查结果持续优化

## 常见问题

### Q1: 如何提高专利撰写的质量？

**A**: 提供详细的发明描述，包括：
- 技术背景和问题
- 具体的技术方案
- 有益效果和优势
- 附图说明

### Q2: 检索结果不准确怎么办？

**A**: 可以尝试：
- 调整关键词组合
- 使用同义词和相关术语
- 修改相似度阈值
- 增加检索数据库

### Q3: 如何自定义审查规则？

**A**: 使用 `RuleManager`：
```python
rule_manager = RuleManager()
rule_manager.add_rule(rule_type, custom_rule)
```

### Q4: 系统支持哪些专利类型？

**A**: 支持：
- 发明专利 (invention)
- 实用新型 (utility_model)
- 外观设计 (design)

## 扩展开发

### 添加新的审查规则

1. 在 `config/review_rules.py` 中定义规则
2. 在 `tools/patent_reviewer.py` 中实现检查逻辑
3. 重新加载规则管理器

### 集成新的专利数据库

1. 继承 `PatentSearchEngine` 类
2. 实现 `search()` 方法
3. 添加到搜索引擎列表

### 自定义输出格式

1. 扩展 `PatentWriter` 类
2. 添加新的格式化方法
3. 在主 agent 中暴露新工具

## 技术支持

如有问题或建议，请联系开发团队。

## 许可证

本项目采用 MIT 许可证。

## 更新日志

### v1.0.0
- 初始版本
- 实现基本专利撰写、检索、审查功能
- 支持可配置审查规则
- 多数据库检索支持
>>>>>>> a46b91673a146d22130f83bd68806f0d3bd5013c
