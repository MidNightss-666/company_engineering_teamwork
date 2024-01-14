# from langchain.vectorstores import Chroma
# from langchain.embeddings.openai import OpenAIEmbeddings
# from langchain_community.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain

from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import Chroma
#参数设置
llm_name="gpt-3.5-turbo"#模型名

#函数：创建大语言模型
def create_llmmodel(llmname=llm_name):
    # 大语言模型（API),model_name为模型名，temperature（0-1）为随机性
    llm = ChatOpenAI(model_name=llm_name, temperature=0)
    return llm

#1. 导入向量数据库
#函数：根据给定directory导入数据库
def import_database(directory = 'docs/chroma/matplotlib/'):
    embedding = OpenAIEmbeddings()
    vectordb = Chroma(persist_directory=directory, embedding_function=embedding)
    print("数据库导入成功，数据库规模：",vectordb._collection.count())
    return vectordb

#2. 测试向量检索
#函数：根据输入的问题question在给定数据库vectordb中检索
def search_data(vectordb,question="这节课的主要话题是什么",k=3):
    datas = vectordb.similarity_search(question, k=k)
    return datas

# 3.记忆功能
#函数：创建记忆库
# def create_memory():
#     chat_memory = ConversationBufferMemory(
#         memory_key="chat_history",  # 与 prompt 的输入变量保持一致。
#         return_messages=True  # 将以消息列表的形式返回聊天记录，而不是单个字符串
#     )
#     return chat_memory

#4. 问答链
#函数：构建简单问答链，可以根据数据库中的相关知识来回答问题
def get_simple_qachain(vectordb,llm):
    qa_chain = RetrievalQA.from_chain_type(
        llm,
        retriever=vectordb.as_retriever()
    )#使用数据库和vectordb构建检索式问答链
    return qa_chain

#函数：构建提示词问答链，可以根据数据库中的相关知识来回答问题，相对简单问答链答案更加稳定和简洁
def get_prompt_qachain(vectordb,llm):
    template = """使用以下上下文片段来回答最后的问题。如果你不知道答案，只需说不知道，不要试图编造答案。尽量简明扼要地回答。在回答的最后一定要说"感谢您的提问！"
    {context}
    问题：{question}
    有用的回答："""#格式化prompt，可以使模型阅读相关资料和问题后根据资料和自己的参数来给出答案
    #qa_prompt = PromptTemplate.from_template(template)#构建提示词对象
    qa_prompt = PromptTemplate(input_variables=["context", "question"], template=template, )
    qa_chain = RetrievalQA.from_chain_type(
        llm,
        retriever=vectordb.as_retriever(),
        return_source_documents=True,
        chain_type_kwargs={"prompt": qa_prompt}
    )#构建问答链
    return qa_chain

#函数：创建带记忆问答链，可以从之前对话的语境和数据库中搜索问题相关内容
def get_memory_qachain(vectordb,llm,chain_type='stuff',k=4):
    # chat_memory = ConversationBufferMemory(
    #         memory_key="chat_history",  # 与 prompt 的输入变量保持一致。
    #         return_messages=True  # 将以消息列表的形式返回聊天记录，而不是单个字符串
    #     )#创建mem
    # retriever = vectordb.as_retriever()
    # qa_chain = ConversationalRetrievalChain.from_llm(
    #     llm,
    #     retriever=retriever,
    #     memory=chat_memory
    # )#创建问答链
    # 初始化，vectordb为使用get_simple_qachain根据地址生成的数据库对象，llm为create_llmmodel生成
    # 的大模型对象，k为每次搜索取前k个结果
    #创建检索器和问答链
    retriever = vectordb.as_retriever(search_type="similarity", search_kwargs={"k": k})
    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=ChatOpenAI(model_name=llm_name, temperature=0),
        chain_type=chain_type,
        retriever=retriever,
        return_source_documents=True,
        return_generated_question=True,
    )
    return qa_chain

class memory_qachain:#类类型的问答链
    def __init__(self,vectordb,llm,chain_type='stuff',k=4):
        #初始化，vectordb为使用get_simple_qachain根据地址生成的数据库对象，llm为create_llmmodel生成
        #的大模型对象，k为每次搜索取前k个结果
        self.chat_memory = ConversationBufferMemory(
            memory_key="chat_history",  # 与 prompt 的输入变量保持一致。
            return_messages=True  # 将以消息列表的形式返回聊天记录，而不是单个字符串
        )  # 创建mem
        self.retriever = vectordb.as_retriever(search_type="similarity", search_kwargs={"k": k})
        self.qa_chain = ConversationalRetrievalChain.from_llm(
            llm,
            retriever=self.retriever,
            memory=self.chat_memory
        )  # 创建问答链
    def __call__(self,question= "这节课的主要话题是什么"):
        result = self.qa_chain({"question": question})
        return result['answer']



#5. 获得答案
def get_answer(qa_chain,question= "这节课的主要话题是什么"):
    if(str(type(qa_chain)) == "<class 'langchain.chains.conversational_retrieval.base.ConversationalRetrievalChain'>"):
        result = qa_chain({"question": question})
        return result['answer']
    else:
        result = qa_chain({"query": question})
        return result.get('result')


if __name__ == '__main__':
    vectordb = import_database()
    llm=create_llmmodel(llm_name)
    #测试import_database和search_data
    # datas=search_data(vectordb)
    # print(len(datas))
    #测试get_answer_simple_qachain
    # chain = get_simple_qachain(vectordb,llm)
    # 测试get_answer_simple_qachain
    # chian = get_prompt_qachain(vectordb,llm)
    #测试get_memory_qachain
    # chain=get_memory_qachain(vectordb,llm)
    # answer=get_answer(chain,question="这门课会学习 Python 吗？")
    # print(answer)
    # answer = get_answer(chain, question="为什么这门课需要这个前提？")
    # print(answer)
    #测试memory_qachain类
    chain=memory_qachain(vectordb,llm)
    print(chain("这门课会学习 Python 吗？"))
    print(chain("为什么这门课需要这个前提？"))
