"""案例07·对话记忆：跨轮次与多会话的记忆管理。

掌握点：RunnableWithMessageHistory + 会话隔离（session_id）。
记忆不是模型的魔法，是历史消息的组装与持久化。
"""
import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parent.parent))

from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables.history import RunnableWithMessageHistory

from common import init_llm

store: dict[str, InMemoryChatMessageHistory] = {}  # 会话仓库（生产换Redis/DB）

prompt = ChatPromptTemplate.from_messages([
    ("system", "你是耐心的助理，能记住对话中说过的信息。"),
    ("placeholder", "{history}"),   # 历史消息注入位
    ("human", "{input}"),
])
chain = prompt | init_llm()

with_history = RunnableWithMessageHistory(
    chain,
    get_session_history=lambda sid: store.setdefault(sid, InMemoryChatMessageHistory()),
    input_messages_key="input",
    history_messages_key="history",
)

# 同一会话两轮：第二轮能记住第一轮的信息
cfg = {"configurable": {"session_id": "user-001"}}
r1 = with_history.invoke({"input": "我叫老胡，重仓持有葵花药业"}, config=cfg)
print("【第1轮】", r1.content)
r2 = with_history.invoke({"input": "我叫什么？持有什么票？"}, config=cfg)
print("【第2轮】", r2.content)   # 记住了！

# 换会话：记忆隔离，各聊各的
cfg_b = {"configurable": {"session_id": "user-002"}}
r3 = with_history.invoke({"input": "我叫什么？"}, config=cfg_b)
print("【新会话】", r3.content)  # 不知道——隔离生效
