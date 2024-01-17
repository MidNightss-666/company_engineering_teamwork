# 企业工程实践大作业——chatGPT3.5的外围工程

运行环境：anaconda+pycharm（社区版和专业版应该都可以）
# 1部署工程
## 1.1 python环境部署：
python版本：3.9.18亲测可以跑通，其他不保证
尽量在anaconda开虚拟环境安装，以防库之间依赖冲突。
1. 可以使用pip install -r requirePackage.txt安装所需依赖包
2. 如果批量下载出错，可以逐一下载以下包：
   openai
  tensorflow
  pypdf
  langchain
  langchain-community
  chromadb
  chardet
  panel
  param
  tiktoken
  pip install -U langchain-openai
  以下两个包尽量使用conda下载，可以减少C++环境依赖报错的概率。下载时如果使用清华源等国内镜像，需要关闭梯子
  conda install -c conda-forge chromadb
  conda install -c conda-forge "langchain[docarray]"

注1：如果下载时报错缺少C++环境依赖如下：
```
        Building wheel for hnswlib (pyproject.toml) did not run successfully.
            exit code: 1
        
            [5 lines of output]
            running bdist_wheel
            running build
            running build_ext
            building 'hnswlib' extension
            error: Microsoft Visual C++ 14.0 or greater is required. Get it with "Microsoft C++ Build Tools": Microsoft C++ Build Tools - Visual Studio
            [end of output]
```
需要到https://visualstudio.microsoft.com/zh-hans/visual-cpp-build-tools/下载visual studio，在下载栏选择C++桌面开发工具，sdk选择自己电脑Windows系统的版本。之后重启终端即可。
## 1.2 环境变量配置
参照如下教程在本机配置openai_api_key环境变量，之后重启终端。
https://zhuanlan.zhihu.com/p/627665725
注：openai.api_key在envs.txt
## 1.3 服务器部署
panel包的GUI界面需要依赖服务器启动，这里使用X服务器。
下载和安装Xming：前往Xming的官方网站（https://sourceforge.net/projects/xming/）下载安装程序。
下载完毕后，运行安装程序并按照提示进行安装。
转到项目的“Edit Configurations”（运行配置）窗口，在“Environment”（环境）选项卡中，添加一个新的环境变量：DISPLAY，将其值设置为localhost:0.0。
点击“Apply”（应用）然后点击“OK”（确定）以保存配置更改。
## 1.4 运行
直接运行text.py即可，simplechat还有地方需要修改，暂时跑不通
1. 运行项目时需要和openai的服务器交互，所以需要保持网络连接，梯子打开，以免报retry和HTTPCONNECTEXPECTION
2. 为了打开GUI界面，运行时需要保持Xming服务器开启。（如果打不开GUI界面）

# 2.项目概况
docs文件夹:存放项目的数据库和基础文件。chroma文件夹存放数据库，imgs存放GUI素材，其余文件夹存放的PDF用于生成数据库
envs.txt:项目配置的信息，和本文档基本一致
readme.md:说明文档
requirements.txt：依赖环境清单
teacher_version_create_database.py:用于从指定文件创建数据库
teacher_version_QAchain.py:用于生成和测试逻辑链，导入数据库和LLM，测试数据库检索。
teacher_version_simplechat.py:项目主文件，运行此文件以启动服务，生成GUI界面
temp.pdf:项目运行时下载的用户文件
test.py:项目构建时使用的测试文件，会在最后提交时删除



