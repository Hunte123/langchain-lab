"""共用配置：所有案例通过本模块初始化模型。

模型走 OpenAI 兼容协议，任何厂商（GLM/DeepSeek/Kimi/Ollama…）
通过环境变量即可切换：

    OPENAI_BASE_URL  API地址（如 https://open.bigmodel.cn/api/paas/v4）
    OPENAI_API_KEY   密钥
    LANGCHAIN_MODEL  模型名（如 glm-4.5-flash）
"""
import os

from langchain_openai import ChatOpenAI

DEFAULT_MODEL = "glm-4.5-flash"


def init_llm(temperature: float = 0.7, **kwargs) -> ChatOpenAI:
    """初始化对话模型：读环境变量，任何 OpenAI 兼容服务即插即用。"""
    return ChatOpenAI(
        model=os.getenv("LANGCHAIN_MODEL", DEFAULT_MODEL),
        base_url=os.getenv("OPENAI_BASE_URL"),
        api_key=os.getenv("OPENAI_API_KEY"),
        temperature=temperature,
        **kwargs,
    )
