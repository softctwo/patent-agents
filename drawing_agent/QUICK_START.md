# 专利附图绘制Agent - 快速启动指南

## 🚀 5分钟快速上手

### 步骤1：安装依赖

```bash
pip install Pillow pydantic
```

### 步骤2：运行演示

```bash
cd /Users/zhangyanlong/workspaces/openai-agents-python/examples/patent_agent/drawing_agent
python demo_drawing.py
```

这将生成5种不同类型的专利附图演示。

### 步骤3：查看生成的附图

演示结束后，您会得到：
- `demo_1_机械结构图.png`
- `demo_2_电路图.png`
- `demo_3_流程图.png`
- `demo_4_示意图.png`
- `demo_5_构造图.png`

---

## 📝 简单使用示例

### 示例1：创建机械结构图

```python
from agents import Runner
from drawing_agent import patent_drawing_agent

result = await Runner.run(
    patent_drawing_agent,
    """
    请创建一份机械结构图：

    发明名称：一种便于携带的折叠式收纳盒
    产品描述：收纳盒采用可折叠设计，方便携带和存储
    组件：盒体, 折叠铰链, 卡扣固定装置, 侧壁加强筋
    输出路径：my_drawing.png
    """
)
print(result.final_output)
```

### 示例2：创建电路图

```python
result = await Runner.run(
    patent_drawing_agent,
    """
    请创建一份电路图：

    发明名称：一种带温度显示的智能水杯
    产品描述：双层真空结构，内置温度传感器和LED显示屏
    组件：温度传感器, LED显示屏, 主控芯片, 电池
    输出路径：circuit.png
    """
)
```

### 示例3：与专利撰写集成

```python
# 步骤1：撰写专利
patent_result = await Runner.run(
    utility_model_agent,
    "请撰写一份实用新型专利：一种智能水杯..."
)

# 步骤2：生成附图
drawing_result = await Runner.run(
    patent_drawing_agent,
    """
    请创建一份机械结构图：
    发明名称：一种带温度显示的智能水杯
    组件：水杯杯体, 温度传感器, LED显示屏, 杯盖密封圈
    """
)
```

---

## 🔧 常用工具函数

| 函数 | 用途 | 场景 |
|------|------|------|
| `create_mechanical_drawing()` | 机械结构图 | 机械发明 |
| `create_circuit_drawing()` | 电路图 | 电子发明 |
| `create_flowchart()` | 流程图 | 方法发明 |
| `create_schematic_drawing()` | 示意图 | 综合发明 |
| `get_drawing_guidelines()` | 获取指导 | 了解要求 |
| `validate_drawing_quality()` | 质量验证 | 检查质量 |

---

## 📊 支持的附图类型

1. **机械结构图** - 展示机械结构和部件关系
2. **电路图** - 显示电子电路结构
3. **流程图** - 展示操作流程
4. **示意图** - 简化表示整体结构
5. **构造图** - 展示内部构造细节

---

## ✅ 符合专利审查指南

- ✅ 线条清晰，粗细均匀
- ✅ 黑色线条，无色彩
- ✅ 300DPI分辨率
- ✅ 标记清楚，与说明书一致
- ✅ 布局合理，比例协调

---

## 🎯 最佳实践

### 提供详细的产品描述

```
✅ 好：收纳盒采用可折叠设计，盒体可以180度展开或折叠
❌ 差：收纳盒可折叠
```

### 明确列出关键组件

```
✅ 好：盒体, 折叠铰链, 卡扣固定装置, 侧壁加强筋
❌ 差：各种部件
```

### 选择合适的附图类型

- **机械装置** → 机械结构图
- **电子设备** → 电路图
- **操作方法** → 流程图
- **整体外观** → 示意图
- **内部结构** → 构造图

---

## 🧪 运行测试

### 基本功能测试

```bash
python test_patent_drawing.py
```

### 集成测试

```bash
cd /Users/zhangyanlong/workspaces/openai-agents-python/examples/patent_agent
python test_drawing_integration.py
```

---

## 📚 更多信息

- 完整文档：[README.md](README.md)
- 最终报告：[patent_drawing_agent_final_report.md](../patent_drawing_agent_final_report.md)
- 专利撰写Agent：[utility_model_agent.py](../utility_model_agent.py)

---

**开始使用吧！只需几分钟，您就能生成专业的专利附图！** 🎉
