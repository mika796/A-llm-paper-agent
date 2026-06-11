import os
import streamlit as st
from dotenv import load_dotenv
# 导入 LangChain 的纯文本切分器（如果文件太大时备用）
from langchain_text_splitters import RecursiveCharacterTextSplitter

# 导入你之前的 Agent 逻辑
from agent_paper_writer import run_paper_writer_flow, researcher_chain, writer_chain

st.set_page_config(page_title="LLM 多智能体论文协同与分析系统", page_icon="📝", layout="centered")
load_dotenv()

if not os.getenv("DEEPSEEK_API_KEY"):
    st.error("❌ 未检测到 DEEPSEEK_API_KEY，请在 .env 文件中配置！")
    st.stop()

st.title("📝 LLM 多智能体论文协同与分析系统")
st.caption("已升级：支持多智能体协同大纲生成 + 本地论文/文献深度分析")

# 使用 Streamlit 的标签页（Tabs）功能，把功能分开
tab1, tab2 = st.tabs(["🚀 自动化大纲生成", "📂 上传论文/文献分析"])

# ================= TAB 1: 原有的生成大纲功能 =================
with tab1:
    topic = st.text_input("💡 输入你想撰写的论文题目：", placeholder="例如：基于深度学习的中文文本情感分析研究", key="tab1_topic")
    if st.button("🚀 开始自动化写作流", type="primary", key="tab1_btn"):
        if not topic.strip():
            st.warning("⚠️ 请先输入论文题目！")
        else:
            with st.status("🤖 多智能体正在协同作业中...", expanded=True) as status:
                final_result = run_paper_writer_flow(topic)
                status.update(label="✅ 论文大纲全流程构建完成！", state="complete")
            st.subheader("✨ 最终论文大纲结果")
            st.markdown(final_result)

# ================= TAB 2: 新增的上传文件分析功能 =================
with tab2:
    st.subheader("📁 上传你的论文或参考文件")
    st.markdown("上传长篇论文（目前支持 `.txt` 或 `.md` 格式，若要支持 PDF 可追加安装 pypdf），智能体团队将对文章进行深度解构。")
    
    # 1. 文件上传组件
    uploaded_file = st.file_uploader("选择文件", type=["txt", "md"])
    
    # 可选的分析意图
    analysis_task = st.selectbox(
        "🎯 请选择你希望智能体执行的分析任务：",
        ["全面剖析：提炼核心创新点、研究方法与实验结论", 
         "严厉审稿：指出本文的逻辑漏洞、语言不足与改进建议",
         "续写指引：基于本文现有工作，预测未来的 3 个研究方向"]
    )

    if uploaded_file is not None:
        # 2. 读取上传文件的文本内容
        try:
            bytes_data = uploaded_file.read()
            # 解决中文编码问题
            file_content = bytes_data.decode("utf-8")
            st.success(f"📖 成功读取文件：{uploaded_file.name}，共 {len(file_content)} 个字符。")
        except Exception as e:
            st.error(f"❌ 文件读取失败，请检查编码格式。错误信息: {e}")
            file_content = None

        # 3. 点击按钮开始分析
        if st.button("🧠 指派智能体开始分析", type="primary", key="tab2_btn") and file_content:
            with st.status("🕵️‍♂️ 智能体正在深度研读文献中...", expanded=True) as status:
                
                # 如果文章过长，截取前 30000 字（防止超出普通模型单次输入限制，DeepSeek官方API支持更长）
                context_text = file_content[:30000]
                
                st.write("🔄 调研员正在抽取文章核心逻辑...")
                
                # 动态构建一个专门针对具体文件分析的 Prompt
                analysis_prompt = f"""你是一名顶级学术期刊的审稿人和资深学者。
                        请针对以下用户上传的论文内容，执行任务：【{analysis_task}】。
                        请使用极其严谨、客观、一针见血的中文学术语言进行回复。
                        
                        --- 论文内容开始 ---
                        {context_text}
                        --- 论文内容结束 ---
                        """
                
                # 借用你已有的 researcher_chain 或直接用底层 llm 预测
                # 这里我们直接复用你已经导入的底层模型，因为这是一次性分析
                from agent_paper_writer import llm_v3
                response = llm_v3.invoke(analysis_prompt)
                
                status.update(label="✅ 文献分析报告生成完毕！", state="complete")
            
            # 展示分析结果
            st.subheader("📊 智能体文献分析报告")
            st.markdown(response.content)
            st.balloons() # 放个气球庆祝一下