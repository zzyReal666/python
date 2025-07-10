import os
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate

# 打印环境变量
print(os.getenv("DASHSCOPE_API_KEY"))

# 创建LangChain的ChatOpenAI实例
llm = ChatOpenAI(
    model="qwen-plus",
    api_key="sk-730784af62d14bc6b5067a2e6633f096",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    temperature=0
)

prompt = PromptTemplate.from_template("你是一个起名字大师，请模仿实例起三个{country}名字，比如男孩名字经常叫做{boy_name}，女孩名字经常叫做{girl_name}")
message = prompt.format(country="中国特色的", boy_name="张三", girl_name="白洁")

print(message)

# 使用invoke方法替代predict
response = llm.invoke(message)
print(response.content)

