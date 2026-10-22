"""案例05·RAG检索增强：文档入库→检索→带上下文生成。

掌握点：TextLoader / 切块 / 向量库 / retriever / 组装RAG链。
本例用确定性假向量(零成本离线跑通)；注释里标注切换真实向量的方法。
"""
import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parent.parent))

from pathlib import Path

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

from common import init_llm

# ── 1. 准备语料：真实项目里换成 TextLoader 加载文档 ──
docs = [
    "葵花药业以儿童药为主打，核心产品包括小儿肺热咳喘口服液、护肝片。",
    "贵州茅台毛利率长期超过91%，是A股盈利质量最高的公司之一。",
    "创业板指聚焦新能源、医药、TMT，波动显著大于主板。",
]
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_community.embeddings import DeterministicFakeEmbeddingAdapter
from langchain_core.embeddings import FakeEmbeddings

# 零成本跑通用假向量；真实项目替换为：
#   from langchain_openai import OpenAIEmbeddings; emb = OpenAIEmbeddings(model="embedding-3")
emb = DeterministicFakeEmbeddingAdapter(FakeEmbeddings(size=64))
store = InMemoryVectorStore.from_texts(docs, emb)

# ── 2. 检索器：RAG链的核心零件 ──
retriever = store.as_retriever(search_kwargs={"k": 2})

# ── 3. 组装RAG链：检索结果注入模板 ──
prompt = ChatPromptTemplate.from_template(
    "仅依据以下资料回答，没有就说不知道：\n{context}\n\n问题：{question}"
)
llm = init_llm()

def format_docs(chunks):
    return "\n".join("- " + c.page_content for c in chunks)

rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt | llm | StrOutputParser()
)
print("【RAG】", rag_chain.invoke("葵花药业的核心产品有什么？"))
print("【RAG】", rag_chain.invoke("创业板指有什么特点？"))
print("【拒答】", rag_chain.invoke("美国加息了吗？"))  # 资料里没有→应当拒答
