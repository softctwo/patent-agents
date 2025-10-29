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
