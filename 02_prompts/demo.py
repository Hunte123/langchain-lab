"""案例02·提示词模板：把提示词从字符串变成可复用的组件。

掌握点：ChatPromptTemplate 变量注入、多消息角色、few-shot 示例。
"""
import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parent.parent))

from langchain_core.prompts import ChatPromptTemplate

from common import init_llm

llm = init_llm()

# 1. 变量模板：system定人设，user带变量
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一位{style}风格的A股分析师，回答务必简洁。"),
    ("user", "点评一下{stock}今天的走势"),
])
chain = prompt | llm
print("【犀利版】", chain.invoke({"style": "毒舌犀利", "stock": "贵州茅台"}).content)
print()
print("【温和版】", chain.invoke({"style": "温和劝导", "stock": "贵州茅台"}).content)

# 2. few-shot：给示例比给规则更有效
few_shot = ChatPromptTemplate.from_messages([
    ("system", "按示例的格式输出，不加多余内容。"),
    ("human", "茅台 1310"),
    ("ai", "贵州茅台(600519) 收盘价 1310 元"),
    ("human", "宁德 188"),
])
print("【few-shot】", (few_shot | llm).invoke({}).content)
