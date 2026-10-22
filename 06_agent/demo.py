"""案例06·工具与Agent：让模型自己决定何时调用什么工具。

掌握点：@tool 装饰器（docstring即工具说明书）+ tool-calling Agent。
工具复用自 mcp 项目的行情查询——同样的能力换个协议壳。
"""
import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parent.parent))

import re
import subprocess

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool

from common import init_llm


@tool
def get_quote(code: str) -> str:
    """查询A股实时行情。code支持600519或sh600519格式；指数如sz399001。盘前返回昨收。"""

    m = re.search(r"\d{6}", code)  # 容错：Agent传参可能带杂质，提取6位数字
    if m:
        c = m.group(0)
        code = ("sh" if c.startswith("6") else "sz") + c
    else:
        code = code.strip()
    r = subprocess.run(
        ["curl", "-s", "-m", "10", "-H", "Referer: https://finance.sina.com.cn",
         f"https://hq.sinajs.cn/list={code}"],
        capture_output=True, timeout=15)
    text = r.stdout.decode("gbk", "ignore")
    m = re.search(r'="([^"]+)"', text)
    if not m or not m.group(1):
        return f"未查到 {code}"
    p = m.group(1).split(",")
    return f"{p[0]}（{code}）最新价 {p[3]}（昨收 {p[2]}）"


llm = init_llm(temperature=0)
tools = [get_quote]

# 现代Agent写法：create_agent（langgraph内核）
from langchain.agents import create_agent
agent = create_agent(
    llm,
    tools,
    system_prompt="你是行情助手，需要行情数据时必须调用工具获取，禁止编造价格。",
)
print("【Agent】直接查:", agent.invoke({"messages": [("user", "查一下600519的股价")]})["messages"][-1].content)
print()
print("【Agent】推理+查:", agent.invoke({"messages": [("user", "深证成指现在多少点？")]})["messages"][-1].content)
