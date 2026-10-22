# langchain-lab

LangChain 渐进式练习集：8 个案例从基础对话走到 Agent 与评估，每个目录一个可运行脚本，配中文注释。

**学习路径**：每个案例聚焦一个核心概念，后一个建立在前一个之上——按编号顺序学就是完整入门。

| # | 案例 | 核心概念 |
|---|------|---------|
| 01 | chat_basic | 模型接入：invoke / stream / batch 三种调用 |
| 02 | prompts | 提示词模板：变量注入、角色消息、few-shot |
| 03 | lcel_chains | LCEL 链式组合：管道 \| 、RunnableParallel、RunnablePassthrough |
| 04 | structured_output | 结构化输出：Pydantic + with_structured_output |
| 05 | rag | RAG 全链路：切块/向量库/检索器/上下文注入（零成本可跑） |
| 06 | agent | 工具与 Agent：@tool 装饰器 + tool-calling（真实行情工具） |
| 07 | memory | 对话记忆：RunnableWithMessageHistory、会话隔离 |
| 08 | eval | 评估：batch + 断言式检查（最朴素可靠的评估） |

## 运行

```bash
python3.11 -m venv venv
venv/bin/pip install -r requirements.txt        # 国内建议: -i https://pypi.tuna.tsinghua.edu.cn/simple

export OPENAI_BASE_URL=https://open.bigmodel.cn/api/paas/v4   # 任意 OpenAI 兼容服务
export OPENAI_API_KEY=***
export LANGCHAIN_MODEL=glm-4.5-flash

venv/bin/python 01_chat_basic/demo.py            # 在仓库根目录运行
```

每个脚本自包含，从任意目录均可运行（脚本自动定位仓库根的 `common.py`）。

## 环境说明

- 模型通过 `common.py` 统一初始化，`ChatOpenAI` 走 OpenAI 兼容协议——**换厂商只改环境变量**
- 05_rag 使用确定性假向量（`FakeEmbeddings`）保证零成本离线跑通；接真实检索时替换为 `OpenAIEmbeddings` 即可（脚本内有注释标注）
- 06_agent 的行情工具复用 [astock-mcp-go](https://github.com/Hunte123/astock-mcp-go) 项目同款新浪/腾讯数据源思路

## 关于这套练习的设计观点

框架的价值在"不会写的人能快速用"。这套案例的目标是**每一步都看得见**——读完 8 个脚本，LangChain 的核心抽象（Runnable、Prompt、Chain、Retriever、Tool、History）就都有体感了。

配套自研实现（无框架版）见 [go-agent-lab](https://github.com/Hunte123/go-agent-lab) 与 [go-rag-memory-lab](https://github.com/Hunte123/go-rag-memory-lab)：同一套概念，一手框架一手内核，对照着看理解最深。

## License

MIT
