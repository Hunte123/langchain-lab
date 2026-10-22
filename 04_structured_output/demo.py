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

# 实战提醒：部分模型对 function-calling 式结构化输出支持不稳（如返回纯文本），
# 生产代码通常带提示词式JSON解析兜底——这也是LangChain的经典姿势之一。
def analyze(text: str) -> StockBrief:
    try:
        return structured.invoke(text)
    except Exception:
        from langchain_core.output_parsers import JsonOutputParser
        from langchain_core.prompts import ChatPromptTemplate
        parser = JsonOutputParser(pydantic_object=StockBrief)
        prompt = ChatPromptTemplate.from_template(
            "{text}\n\n{format_instructions}\n只输出JSON，不要其他内容。")
        chain = prompt | llm | JsonOutputParser()
        data = chain.invoke({"text": text, "format_instructions": parser.get_format_instructions()})
        return StockBrief(**data)

brief = analyze("近期新能源板块大跌，宁德时代单日跌超10%，请分析")
print("【结构化】", type(brief).__name__)          # 直接拿到Python对象
print(f"  结论: {brief.sentiment}  置信度: {brief.confidence:.0%}")
for r in brief.reasons:
    print("  -", r)

# 拿到对象后就能直接进业务逻辑：入库、判断、触发……
if brief.confidence > 0.7:
    print("【下游逻辑】置信度达标，可进入自动流程")
