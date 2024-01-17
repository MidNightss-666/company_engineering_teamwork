from teacher_version_QAchain import *
from teacher_version_create_database import create_database

def open_book(path, db):
    global vectordb
    global llm
    global chain
    vectordb = create_database(path, True, db)
    llm = create_llmmodel(llm_name)
    chain = get_simple_qachain(vectordb, llm)

def get_score(max_score, keywords, answer):
    score = 0
    for keyword in keywords:
        point = 0
        for i in keyword.split('|'):
            if i in answer:
                point = 1
                break
        score += point
    return score / max_score * 100

def known_question(q, keywords):
    print(q)
    ans = get_answer(chain, q)
    print(ans)
    score = get_score(len(keywords), keywords, ans)
    print(score)
    print()
    return score

def unknown_question(q):
    print(q)
    vectordb = import_database('./db1/')
    llm = create_llmmodel(llm_name)
    chain = get_simple_qachain(vectordb, llm)
    ans = get_answer(chain, q)
    print(ans)
    user_message = f"""请你根据《局外人》这本小说和指定的提问，对下面的回答打分，范围为0到100分。请只回答一个整数代表分数，不回答其他无关信息。以下是数据：
[问题]: {q}
[回答]: {ans}"""
    ans = get_answer(chain, user_message)
    print(ans)
    print()
    score = float(ans)
    return score

scores = []

open_book(r'docs\test\局外人.pdf', './db1/')
scores.append(unknown_question("回答主人公经历了哪些转折点，这些转折点如何影响了他的命运？"))
open_book(r'docs\test\局外人.pdf', './db2/')
scores.append(unknown_question("回答主人公的冷漠和超然态度在小说中扮演了什么样的角色？"))
open_book(r'docs\test\局外人.pdf', './db3/')
scores.append(unknown_question("回答结尾揭示的主人公对于死亡的态度和他对生命的理解如何为小说的主题和哲学观点提供了深刻的意义？"))

print('无标准答案问题平均分数：', sum(scores) / len(scores))

scores = []

open_book(r'docs\test\Liu_Towards_Implicit_Text-Guided_3D_Shape_Generation_CVPR_2022_paper.pdf', './db4/')
scores.append(known_question("Who's the first author of this paper", ['Liu']))
open_book(r'docs\test\Liu_Towards_Implicit_Text-Guided_3D_Shape_Generation_CVPR_2022_paper.pdf', './db5/')
scores.append(known_question("What's the background of this paper", ['generation|generate', '3D', 'text|natural language', 'color']))
open_book(r'docs\test\Liu_Towards_Implicit_Text-Guided_3D_Shape_Generation_CVPR_2022_paper.pdf', './db6/')
scores.append(known_question("本文的创新点有哪些", ['loss|损失', '解耦|decouple|decoupled', 'word-level|词级|字级', 'IMLE', '处理|manipulation']))

open_book(r'docs\test\Liu_Towards_Implicit_Text-Guided_3D_Shape_Generation_CVPR_2022_paper.pdf', './db7/')
ans = get_answer(chain, "本文中介绍的模型是否是一种end to end的模型")
print(ans)
score = 0 if '不是' in ans or 'not' in ans else 100
print(score)
scores.append(score)

open_book(r'docs\test\Liu_Towards_Implicit_Text-Guided_3D_Shape_Generation_CVPR_2022_paper.pdf', './db8/')
scores.append(known_question("作者做了哪些实验", ['Dataset|数据集', '已有工作|现成工作|existing works', 'manipulation|处理|操纵|编辑', '消融|ablation']))

print('有标准答案问题平均分数：', sum(scores) / len(scores))