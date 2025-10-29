# 🚀 快速启动卡片

## 1️⃣ 配置API密钥（30秒）

```bash
# 复制模板
cp .env.example .env

# 编辑文件，填入您的API密钥
GOOGLE_API_KEY=您的Gemini密钥
```

**获取密钥**：https://aistudio.google.com/app/apikey

---

## 2️⃣ 运行测试（10秒）

```bash
python test_ai_drawing.py
```

**预期输出**：
```
✅ Gemini-2.5-Pro AI模型初始化成功（从.env文件加载）
✅ 机械结构图生成成功
```

---

## 3️⃣ 开始绘图

```python
from drawing_agent.tools.ai_patent_drawing_tool import AIPatentDrawingTool

tool = AIPatentDrawingTool()
result = tool.create_drawing(request, "output.png")
```

---

## 📚 文档

- **完整配置**：ENV_CONFIGURATION.md
- **模型升级**：GEMINI_2.5_PRO_UPGRADE_NOTES.md
- **配置总结**：ENV_SETUP_SUMMARY.md

---

## 🎯 一句话总结

**复制.env模板 → 填入API密钥 → 运行测试 → 开始使用AI绘图**

---
*更新：2025-10-30*
