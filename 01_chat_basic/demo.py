"""案例01·基础对话：模型接入的三种调用方式。

掌握点：invoke(单次) / stream(流式) / batch(并行批量)。
"""
import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parent.parent))

from common import init_llm

llm = init_llm()

# 1. invoke：最基本的单次调用
resp = llm.invoke("用一句话解释什么是大语言模型")
print("【invoke】", resp.content)

# 2. stream：流式输出（打字机效果，适合做产品）
print("【stream】", end="", flush=True)
for chunk in llm.stream("用30字给A股新手一句忠告"):
    print(chunk.content, end="", flush=True)
print()

# 3. batch：并行批量（一次发多个互不依赖的请求）
results = llm.batch(["1+1=?", "2+2=?", "3+3=?"])
print("【batch】", [r.content for r in results])
