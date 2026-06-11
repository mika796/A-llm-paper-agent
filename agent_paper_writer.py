import os
from dotenv import load_dotenv
from langchain_deepseek import ChatDeepSeek
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# 1. 加载环境变量
load_dotenv()

# 2. 初始化 DeepSeek 模型
# 调研和常规生成使用 V3 (deepseek-chat)
llm_v3 = ChatDeepSeek(
    model="deepseek-chat",
    temperature=0.3
)

# 如果涉及到深度逻辑推理，可以换成 R1 (deepseek-reasoner)
# llm_r1 = ChatDeepSeek(model="deepseek-reasoner")


print("🤖 系统初始化成功，正在构建智能体管线...")

# 3. 定义【文献调研智能体】的 Prompt 和 Chain
researcher_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一名资深的学术调研员。请针对用户给出的论文题目，列出 3 个核心的研究痛点/研究方向，并提供一段简要的背景综述。请使用严谨的中文学术语言。"),
    ("human", "论文题目：{topic}")
])
# 组装调研链
researcher_chain = researcher_prompt | llm_v3 | StrOutputParser()


# 4. 定义【论文撰写智能体】的 Prompt 和 Chain
writer_prompt = ChatPromptTemplate.from_messages([
    ("system", "你别是一名擅长中文学术写作的教授。请根据调研员提供的【研究背景与痛点】，为论文题目《{topic}》撰写一份详细的论文大纲（包含引言、相关工作、核心方法、实验设计）。大纲必须逻辑严密，结构清晰。"),
    ("human", "调研员提供的材料：\n{research_result}")
])
# 组装撰写链
writer_chain = writer_prompt | llm_v3 | StrOutputParser()



# 5. 串联智能体工作流 (Workflow)
def run_paper_writer_flow(paper_topic):
    print(f"\n🚀 [Step 1] 正在指派 调研智能体 针对课题 《{paper_topic}》 进行分析...")
    research_output = researcher_chain.invoke({"topic": paper_topic})
    
    print("\n💡 [调研员报告生成完毕] 报告摘要如下：")
    print("-" * 40)
    print(research_output[:200] + "...\n(此处省略部分内容)")
    print("-" * 40)
    
    print("\n✍️ [Step 2] 正在指派 撰写智能体 根据调研报告构建论文大纲...")
    final_outline = writer_chain.invoke({
        "topic": paper_topic,
        "research_result": research_output
    })
    
    return final_outline

# 6. 运行测试
if __name__ == "__main__":
    # 你可以替换成你想写的任意论文题目
    target_topic = "基于深度学习的中文文本情感分析研究"
    
    result = run_paper_writer_flow(target_topic)
    
    print("\n✨✨ [最终生成结果] 论文大纲 ✨✨")
    print("=" * 60)
    print(result)
    print("=" * 60)