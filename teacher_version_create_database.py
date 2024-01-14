from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader


def create_database(loader_path, save_db=False, database_directory=""):
#函数：创建数据库
#输入：loader_path,列表，每一项为文件名；save_db，是否保存数据库。database_directory保存路径
    # 1. 加载 PDF
    docs = []#PDF对象
    if str(type(loader_path)) == "<class 'list'>":
        for loader in loader_path:#读取PDF
            loader=PyPDFLoader(loader)
            docs.extend(loader.load())
    else:
        loader = PyPDFLoader(loader_path)
        docs.extend(loader.load())
    # 2. 分割文本
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 1000,  #每个文本块的大小
        chunk_overlap = 150  #文本块之间的重叠部分。
    )
    splits = text_splitter.split_documents(docs)#分割文本

    # 3. 向量化工具设置
    embedding = OpenAIEmbeddings()

    # 4. 创建向量数据库
    if save_db == False:
        db = Chroma.from_documents(#创建向量数据库
            documents=splits,#文档采用分割后的文档版本
            embedding=embedding,#向量化对象设置
        )
    else:
        db=Chroma.from_documents(#创建向量数据库
            documents=splits,#文档采用分割后的文档版本
            embedding=embedding,#向量化对象设置
            persist_directory=database_directory

        )
    print("创建成功，数据库规模：", db._collection.count())
    return db

if __name__ == '__main__':
    # 实验用数据库配置
    # database_directory = 'docs/chroma/matplotlib/'  # 数据库路径
    # loader_path = [
    #         # 故意添加重复文档，使数据混乱
    #         PyPDFLoader("docs/matplotlib/第一回：Matplotlib初相识.pdf"),
    #         PyPDFLoader("docs/matplotlib/第一回：Matplotlib初相识.pdf"),
    #         PyPDFLoader("docs/matplotlib/第二回：艺术画笔见乾坤.pdf"),
    #         PyPDFLoader("docs/matplotlib/第三回：布局格式定方圆.pdf")
    #     ]#PDF地址列表
    loader_path = [
        "docs/matplotlib/第一回：Matplotlib初相识.pdf",
        "docs/matplotlib/第二回：艺术画笔见乾坤.pdf",
        "docs/matplotlib/第三回：布局格式定方圆.pdf"
    ]  # PDF地址列表
    # loader_path="temp.pdf"
    #项目配置
    # database_directory = "docs/chroma/python_learning/"# 数据库路径
    # loader_path = [
    #     "docs/python_learning/《流畅的Python》高清官方中文版.pdf" # PDF地址列表
    # ]
    #
    create_database(loader_path=loader_path,save_db=True,database_directory='docs/chroma/matplotlib/')

