# 专利附图绘制Agent

## 📐 概述

专利附图绘制Agent是一个专门用于生成符合专利审查指南要求的附图的AI智能体。该Agent能够自动创建各种类型的专利附图，包括机械结构图、电路图、流程图、示意图等，确保生成的附图完全符合专利申请的标准要求。

## ✨ 主要特性

### 🎯 核心特性

- **符合标准**：严格遵循专利审查指南的制图要求
- **多种类型**：支持5种主要附图类型
- **自动布局**：智能布局和标记系统
- **高质量输出**：300DPI分辨率，黑白线条图
- **标记清楚**：自动添加参考标记和组件列表

### 📋 支持的附图类型

| 类型 | 说明 | 适用场景 |
|------|------|----------|
| **机械结构图** | 展示产品的机械结构和部件关系 | 机械发明、实用新型 |
| **电路图** | 显示电子电路结构 | 电子发明 |
| **流程图** | 展示操作流程和步骤 | 方法发明 |
| **示意图** | 简化表示整体结构 | 综合发明 |
| **构造图** | 展示内部构造细节 | 结构发明 |

### 📏 符合专利审查指南

✅ **基本要求**
- 线条清晰，粗细均匀（0.3-0.7mm）
- 黑色线条绘制，不得着色
- 分辨率至少300DPI
- 附图与说明书内容一致

✅ **标记规范**
- 使用阿拉伯数字标记
- 标记位于部件附近
- 字体大小适中（2.5-5mm）
- 避免与线条重叠

✅ **布局要求**
- 居中排列
- 比例协调
- 适当边距（10-15mm）
- 避免拥挤

## 🚀 快速开始

### 安装依赖

```bash
pip install Pillow pydantic
```

### 基本用法

#### 方法1：通过Agent调用

```python
from agents import Runner
from drawing_agent import patent_drawing_agent

# 创建机械结构图
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

#### 方法2：直接使用工具函数

```python
from drawing_agent import create_mechanical_drawing

# 直接调用绘图函数
result = create_mechanical_drawing(
    invention_title="一种便于携带的折叠式收纳盒",
    product_description="收纳盒采用可折叠设计，方便携带和存储",
    components="盒体, 折叠铰链, 卡扣固定装置, 侧壁加强筋",
    output_path="my_drawing.png"
)

print(result)
```

## 📖 详细使用说明

### 1. 机械结构图

适用于机械发明和实用新型，展示产品的机械结构。

```python
result = await Runner.run(
    patent_drawing_agent,
    """
    请创建一份机械结构图：

    发明名称：一种防滑折叠梯子
    产品描述：折叠梯子采用双向锁定机制，底部有可调节支撑脚
    组件：梯体, 踏板, 防滑垫片, 折叠机构, 安全锁扣, 伸缩支撑杆
    """
)
```

### 2. 电路图

适用于电子发明，展示电路结构。

```python
result = await Runner.run(
    patent_drawing_agent,
    """
    请创建一份电路图：

    发明名称：一种带温度显示的智能水杯
    产品描述：双层真空结构，内置温度传感器和LED显示屏
    组件：温度传感器, LED显示屏, 主控芯片, 电池, 连接线
    """
)
```

### 3. 流程图

适用于方法发明，展示操作流程。

```python
result = await Runner.run(
    patent_drawing_agent,
    """
    请创建一份流程图：

    发明名称：自动售货机的操作流程
    产品描述：自动售货机的标准操作流程
    流程步骤：投币; 选择商品; 确认订单; 取商品; 找零; 结束
    """
)
```

### 4. 示意图

展示产品的整体外观和结构。

```python
result = await Runner.run(
    patent_drawing_agent,
    """
    请创建一份示意图：

    发明名称：一种带指纹识别的区块链硬件钱包
    产品描述：椭圆形的便携式硬件钱包，内置指纹识别和显示屏
    组件：椭圆形外壳体, OLED显示屏, 指纹识别模块, PCB主板
    """
)
```

## 🔧 工具函数

### 主要工具

#### `create_patent_drawing()`

创建通用专利附图

```python
create_patent_drawing(
    invention_title="发明名称",
    drawing_type="mechanical",  # mechanical, circuit, flowchart, schematic, structure
    product_description="产品描述",
    key_components="组件1, 组件2, 组件3",  # 可选
    structure_details="结构详情",  # 可选
    output_path="output.png"  # 可选
)
```

#### `create_mechanical_drawing()`

创建机械结构图

```python
create_mechanical_drawing(
    invention_title="发明名称",
    product_description="产品描述",
    components="盒体, 折叠铰链, 卡扣固定装置",
    output_path="output.png"
)
```

#### `create_circuit_drawing()`

创建电路图

```python
create_circuit_drawing(
    invention_title="发明名称",
    product_description="产品描述",
    components="主控芯片, 传感器, 显示屏",
    output_path="output.png"
)
```

#### `create_flowchart()`

创建流程图

```python
create_flowchart(
    invention_title="发明名称",
    product_description="产品描述",
    flow_steps="步骤1; 步骤2; 步骤3; 结束",
    output_path="output.png"
)
```

#### `create_schematic_drawing()`

创建示意图

```python
create_schematic_drawing(
    invention_title="发明名称",
    product_description="产品描述",
    components="组件1, 组件2, 组件3",
    output_path="output.png"
)
```

### 辅助工具

#### `get_drawing_guidelines()`

获取专利附图绘制指导

```python
result = get_drawing_guidelines()
print(result)  # 返回详细的绘制指导文档
```

#### `validate_drawing_quality()`

验证附图质量

```python
result = validate_drawing_quality("drawing.png")
print(result)  # 返回质量验证报告
```

## 📊 输出格式

### 附图信息

Agent返回的附图信息包含：

```
专利附图已成功生成！

附图信息：
- 发明名称：xxx
- 附图类型：mechanical
- 组件数量：5
- 生成时间：2025-10-30 15:30:00

附图已保存到：output.png

符合专利审查指南要求：
✓ 线条清晰，粗细均匀
✓ 标记清楚，与说明书一致
✓ 格式标准，分辨率300DPI
✓ 黑白线条图，无色彩
```

### 图像规格

- **分辨率**：300 DPI
- **色彩模式**：灰度（Grayscale）
- **格式**：PNG
- **画布大小**：A4 (210mm × 297mm)
- **边距**：50px

## 🧪 测试

### 运行基本测试

```bash
cd /Users/zhangyanlong/workspaces/openai-agents-python/examples/patent_agent/drawing_agent
python test_patent_drawing.py
```

### 运行集成测试

```bash
cd /Users/zhangyanlong/workspaces/openai-agents-python/examples/patent_agent
python test_drawing_integration.py
```

### 测试用例

测试脚本包含以下测试用例：

1. ✅ 获取绘制指导
2. ✅ 创建机械结构图
3. ✅ 创建电路图
4. ✅ 创建流程图
5. ✅ 创建示意图
6. ✅ 集成测试（专利撰写+附图绘制）

## 🔍 与专利撰写Agent集成

### 完整工作流程

1. **撰写专利申请文件**：使用`utility_model_agent`
2. **生成附图**：使用`patent_drawing_agent`
3. **质量验证**：使用`validate_drawing_quality`

```python
# 步骤1：撰写专利
patent_result = await Runner.run(
    utility_model_agent,
    "请撰写一份实用新型专利..."
)

# 步骤2：生成附图
drawing_result = await Runner.run(
    patent_drawing_agent,
    """
    请创建一份机械结构图：
    发明名称：xxx
    产品描述：xxx
    组件：xxx
    """
)

# 步骤3：验证质量
validation = validate_drawing_quality("drawing.png")
print(validation)
```

## 📈 最佳实践

### 1. 明确产品描述

提供详细的产品描述有助于生成更准确的附图：

```
好：收纳盒采用可折叠设计，盒体可以180度展开或折叠，方便携带和存储
差：收纳盒可折叠
```

### 2. 列出关键组件

明确列出所有关键组件：

```
好：盒体, 折叠铰链, 卡扣固定装置, 侧壁加强筋, 底部支撑结构
差：各种部件
```

### 3. 标准化命名

使用标准化的组件命名：

```
好：温度传感器, LED显示屏, 主控芯片
差：那个传感器, 小屏幕, 芯片
```

### 4. 合理选择附图类型

根据发明内容选择合适的附图类型：

- **机械结构图**：机械装置、构造
- **电路图**：电子设备、电路
- **流程图**：操作方法、步骤
- **示意图**：整体结构、外观
- **构造图**：内部结构、细节

## ❓ 常见问题

### Q: 生成的附图不符合要求怎么办？

A: 请检查以下方面：
1. 产品描述是否足够详细
2. 组件列表是否完整
3. 附图类型是否合适
4. 可以使用`get_drawing_guidelines()`查看详细要求

### Q: 可以自定义附图样式吗？

A: 当前版本使用标准样式，符合专利审查指南要求。如需自定义，可以修改`patent_drawing_tool.py`中的样式参数。

### Q: 支持哪些输出格式？

A: 当前支持PNG格式，分辨率300DPI。可以在工具中扩展支持TIFF等格式。

### Q: 可以批量生成多个附图吗？

A: 可以通过循环调用来批量生成多个附图。

### Q: 如何验证生成的附图质量？

A: 使用`validate_drawing_quality()`工具函数，可以得到详细的质量验证报告。

## 📚 相关文档

- [专利审查指南 - 附图要求](http://www.cnipa.gov.cn/)
- [PIL图像处理文档](https://pillow.readthedocs.io/)
- [Pydantic数据验证](https://docs.pydantic.dev/)

## 📞 支持与反馈

如有问题或建议，请联系开发团队。

## 📄 许可证

本项目采用MIT许可证。

---

**版本**：v1.0
**更新日期**：2025-10-30
**兼容性**：Python 3.7+
