"""案例03·LCEL链式组合：LangChain的表达式语言（核心中的核心）。

掌握点：| 管道组合、RunnableParallel 并行、RunnablePassthrough 传参。
这一课的思维方式贯穿整个 LangChain——一切皆 Runnable。
"""
import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parent.parent))

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough

from common import init_llm

llm = init_llm() | StrOutputParser()  # 链的起点先接好输出解析

# 1. 基础管道：模板 | 模型 | 解析器
joke = ChatPromptTemplate.from_template("讲一个关于{topic}的冷笑话") | llm
print("【管道】", joke.invoke({"topic": "程序员"}))

# 2. RunnableParallel：多路并行再汇合（比如正反两方观点同时生成）
parallel = RunnableParallel(
    多头=ChatPromptTemplate.from_template("用一句话论证明天大盘看涨") | llm,
    空头=ChatPromptTemplate.from_template("用一句话论证明天大盘看跌") | llm,
)
result = parallel.invoke({})
print("【并行】多头:", result["多头"].strip())
print("       空头:", result["空头"].strip())

# 3. RunnablePassthrough：原样透传输入（组装RAG上下文的常用零件）
passthrough = RunnableParallel(origin=RunnablePassthrough(), upper=lambda x: x.upper())
print("【透传】", passthrough.invoke("abc"))
