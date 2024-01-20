import panel as pn
import teacher_version_QAchain
import param
import openai
import json
import teacher_version_create_database
from panel.chat import ChatInterface

class simple_chat(param.Parameterized):#chat封装类
    chat_history = param.List([])#历史记录
    answer = param.String("")#答案
    db_query = param.String("")#问题集
    db_response = param.List([])#回应集
    moderation = param.String("")#审查结果
    loaded_file="python"#默认载入的文件
    dir='docs/chroma/python_learning_saved'#默认数据库地址
    #初始化函数
    def __init__(self, directory=dir,llmname="gpt-3.5-turbo",**params):
        super(simple_chat, self).__init__(**params)
        self.panels = []#可视化页面存储
        # 导入数据库
        self.vectordb = teacher_version_QAchain.import_database(directory=directory)
        # 创建LLM
        self.llm = teacher_version_QAchain.create_llmmodel(llmname=llmname)
        # 创建问答链
        self.qa = teacher_version_QAchain.get_memory_qachain(vectordb=self.vectordb,llm=self.llm)
        # self.loaded_file = "docs/matplotlib/第一回：Matplotlib初相识.pdf"
        # self.qa = load_db(self.loaded_file, "stuff", 4)

    #函数：将文档加载到聊天机器人中，count为总启动次数
    def load_db(self, count):
        if count == 0 or file_input.value is None:  # 初始化或未指定文件，报默认文件
            return pn.pane.Markdown(f"目前文件: {self.loaded_file}")
        else:
            file_input.save("temp.pdf")  #下载上传文件
            self.loaded_file = file_input.filename#更新加载文件名
            button_load.button_style = "outline"#更新按钮
            #更新数据库和问答链
            self.vectordb=teacher_version_create_database.create_database(loader_path="temp.pdf")
            self.qa = teacher_version_QAchain.get_memory_qachain(vectordb=self.vectordb,llm=self.llm)
            button_load.button_style = "solid"
        self.clr_history()#更换了数据库，也要去除历史信息以免干扰
        return pn.pane.Markdown(f"目前文件: {self.loaded_file}")#更新目前加载文件名

    #函数：处理对话链，输入问题query，输出结果
    def convchain(self, contents, user, instance):
        if contents:
            result = self.qa({"question": contents, "chat_history": self.chat_history})
            self.chat_history.extend([(contents, result["answer"])])
            self.db_query = result["generated_question"]
            self.db_response = result["source_documents"]
            self.answer = result['answer']
            inp.value = ''  # 清除时清除装载指示器
            return self.answer

    # 获取最后发送到数据库的问题，答案和对答案的合法性评估
    @param.depends('db_query ', )
    def get_lquest(self):
        if not self.db_query:#如果还没有提问，给出最后一个问题
            return pn.Column(
                pn.Row(pn.pane.Markdown(f"最近问题:", styles={'background-color': '#F6F6F6'})),
                pn.Row(pn.pane.Str("暂无检索结果"))
            )
        #input_json = json.dumps({"text": self.answer})  #将 self.db_response 转换为 JSON 格式
        #response1 = openai.Moderation.create(input=input_json)  #使用转换后的 JSON 作为输入获得审查结果
        #self.moderation = response1["results"][0]  #从 response1 中提取出“results”列表的第一个元素
        return pn.Column(#从问题集中找到最新的问题返回到GUI
            pn.Row(pn.pane.Markdown(f"最近问题:", styles={'background-color': '#F6F6F6'})),
            pn.pane.Str(self.db_query),
            #pn.Row(pn.pane.Markdown(f"回复:", styles={'background-color': '#F6F6F6'})),
            #pn.pane.Str(self.answer),
            # pn.Row(pn.pane.Markdown(f"审查结果:", styles={'background-color': '#F6F6F6'})),
            #pn.pane.Str(self.moderation)
        )

    # 获取数据库返回的源文件
    @param.depends('db_response', )
    def get_sources(self):
        if not self.db_response:#如果还没有回复，置空
            return
        rlist = [pn.Row(pn.pane.Markdown(f"数据库检索结果:", styles={'background-color': '#F6F6F6'}))]
        for doc in self.db_response:#把回复的对应源文件打印出来
            rlist.append(pn.Row(pn.pane.Str(doc)))
        return pn.WidgetBox(*rlist, width=600, scroll=True)
    # 获取当前聊天记录
    @param.depends('convchain', 'clr_history')
    def get_chats(self):
        if not self.chat_history:#如果没有历史记录，报错GUI
            return pn.WidgetBox(pn.Row(pn.pane.Str("目前没有历史记录")), width=600, scroll=True)
        rlist = [pn.Row(pn.pane.Markdown(f"对话记录：", styles={'background-color': '#F6F6F6'}))]
        for exchange in self.chat_history:#打印聊天记录
            rlist.append(pn.Row(pn.pane.Str(exchange)))
        return pn.WidgetBox(*rlist, width=600, scroll=True)
    # 清除聊天记录
    def clr_history(self, count=0):
        self.chat_history = []
        return


if __name__=='__main__':
    #初始化聊天机器人
    cb = simple_chat()
    #定义界面的小部件
    file_input = pn.widgets.FileInput(accept='.pdf')  #PDF文件的文件输入小部件
    button_load = pn.widgets.Button(name="加载数据库", button_type='primary')  #加载数据库的按钮
    button_clearhistory = pn.widgets.Button(name="清除历史", button_type='warning')  #清除聊天记录的按钮
    button_clearhistory.on_click(cb.clr_history)  #将清除历史记录功能绑定到按钮上
    inp = pn.widgets.TextInput(placeholder='请输入文本...')  #用于用户查询的文本输入小部件

    # 将加载数据库和对话的函数绑定到相应的部件上
    bound_button_load = pn.bind(cb.load_db, button_load.param.clicks)
    conversation = pn.bind(cb.convchain, inp)

    # 使用 Panel 定义界面布局
    tab2 = pn.Column(#显示搜索文本
        pn.panel(cb.get_lquest),
        pn.layout.Divider(),
        pn.panel(cb.get_sources),
    )
    tab3 = pn.Column(#显示chat记录
        pn.panel(cb.get_chats),
        pn.layout.Divider(),
    )
    tab4 = pn.Column(#载入PDF
        pn.Row(file_input, button_load, bound_button_load),
        pn.Row(button_clearhistory, pn.pane.Markdown("清除历史记录以开启一个新对话")),
        pn.layout.Divider(),
    )
    #将所有选项卡合并为一个菜单
    # 将所有选项卡合并为一个仪表盘
    dashboard = pn.Row(pn.Column(
        pn.Row(pn.pane.Markdown('# Hello,Chat!')),
        pn.Tabs(('数据库', tab2), ('聊天记录', tab3), ('配置', tab4)),
        width=800,
        styles=dict(background='#696969'),
        sizing_mode='stretch_height'),
        ChatInterface(
            user='User',
            callback=cb.convchain
        )
    )

    #启动GUI
    dashboard.show()