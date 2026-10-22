"""案例04·结构化输出：让模型的输出从"一段话"变成"可编程的数据"。

掌握点：with_structured_output + Pydantic 模型——
字段名和描述就是给模型看的"输出说明书"。
"""
import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parent.parent))

from pydantic import BaseModel, Field

from common import init_llm


class StockBrief(BaseModel):
    """模型被要求按这个结构输出——字段描述写得越清楚，输出越准。"""

    name: str = Field(description="股票名称")
    sentiment: str = Field(description="情绪判断：看多/看空/中性")
    reasons: list[str] = Field(description="判断理由，最多3条")
    confidence: float = Field(description="置信度0到1")


llm = init_llm()
structured = llm.with_structured_output(StockBrief)

brief = structured.invoke("近期新能源板块大跌，宁德时代单日跌超10%，请分析")
print("【结构化】", type(brief).__name__)          # 直接拿到Python对象
print(f"  结论: {brief.sentiment}  置信度: {brief.confidence:.0%}")
for r in brief.reasons:
    print("  -", r)

# 拿到对象后就能直接进业务逻辑：入库、判断、触发……
if brief.confidence > 0.7:
    print("【下游逻辑】置信度达标，可进入自动流程")
