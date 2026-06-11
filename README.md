# 📝 A-llm-paper-agent: 基于 LangChain + DeepSeek 的多智能体论文写作系统

本项目是一款基于大模型多智能体（Multi-Agent）架构的自动化中文学术论文写作辅助系统。通过集成 LangChain 框架与 DeepSeek 强大的推理模型，系统能够模拟“大纲拟定、文献检索、内容扩写、润色微调”等多个科研角色，并提供开箱即用的 Streamlit 网页交互界面。

---

## 🚀 功能特性

* **多智能体协同 (Multi-Agent):** 内置大纲架构师、内容撰写员、学术润色官等多个独立 Agent，分工明确。
* **DeepSeek 强力驱动:** 深度适配 DeepSeek API，提供高性价比、高质量的文本生成与逻辑推理能力。
* **极简网页界面:** 基于 Streamlit 构建，无需复杂的配置，一键启动，在浏览器中即可完成整篇大纲与内容的生成。
* **全自动依赖管理:** 规范化配置 `requirements.txt` 与 `.env` 密钥分离机制，确保生产安全。

## 📦 项目结构

```text
llm_paper_agent/
├── agent_paper_writer.py   # 多智能体核心逻辑与链式调用
├── app.py                  # Streamlit 网页端前端界面
├── requirements.txt        # 项目环境依赖清单
└── .gitignore              # Git 忽略文件（已自动屏蔽敏感密钥与虚拟环境）


