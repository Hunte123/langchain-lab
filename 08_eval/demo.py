"""案例08·评估：给链的质量上计量。

掌握点：batch批量跑 + 断言式检查（最朴素也最可靠的评估）。
LangSmith（设环境变量即可接入）用于可视化追踪，本例离线自评。
"""
import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parent.parent))

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from common import init_llm

llm = init_llm(temperature=0)
chain = (
    ChatPromptTemplate.from_template("把下面的股票新闻压缩成不超过{max_words}字的摘要：\n{news}")
    | llm | StrOutputParser()
)

cases = [
    {"news": "宁德时代今日放量大跌10.32%，主力资金净流出创年内新高，市场传闻与产能过剩担忧有关。", "max_words": "15"},
    {"news": "央行宣布降准25个基点，释放长期资金约5000亿元，利好银行与地产板块。", "max_words": "15"},
]

# 断言式评估：字数上限 + 关键信息保留
results = chain.batch(cases)
passed = 0
for c, r in zip(cases, results):
    ok_len = len(r) <= int(c["max_words"]) * 2  # 中文一字一符，留缓冲
    print(f"{'✅' if ok_len else '❌'} 摘要({len(r)}字): {r}")
    passed += ok_len
print(f"\n通过 {passed}/{len(cases)}——评估的意义：改了prompt立刻知道是变好还是变坏")
