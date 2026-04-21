import streamlit as st

st.set_page_config(page_title="当前状态人格测试", page_icon="🧠")

# 初始化 session_state
if "step" not in st.session_state:
    st.session_state.step = 0
if "answers" not in st.session_state:
    st.session_state.answers = []
if "started" not in st.session_state:
    st.session_state.started = False
if "finished" not in st.session_state:
    st.session_state.finished = False

# 题目数据：每道题的选项对应不同类型加分
# 类型编号: 0=稳定蓄力型, 1=外表摆烂内心紧绷型, 2=短时爆发型, 3=低耗能求生型
questions = [
    {
        "question": "周末临时空出半天，你更想……",
        "options": [
            ("在家安静休息充电", [3, 1, 0, 2]),
            ("出门见朋友或逛逛", [0, 2, 3, 1]),
        ]
    },
    {
        "question": "面对一件拖了很久的事情，你通常会……",
        "options": [
            ("找个时间集中搞定", [1, 0, 3, 2]),
            ("能拖就拖，实在不行再说", [2, 3, 1, 0]),
        ]
    },
    {
        "question": "最近几天如果状态不错，你更容易……",
        "options": [
            ("趁机多完成一些任务", [0, 1, 3, 2]),
            ("享受当下，轻松度过", [3, 2, 0, 1]),
        ]
    },
    {
        "question": "当别人对你有期待时，你会……",
        "options": [
            ("感到压力，想做好但有点焦虑", [1, 3, 0, 2]),
            ("把它当作动力，全力以赴", [0, 1, 3, 2]),
        ]
    },
    {
        "question": "你觉得自己最近的能量状态更接近……",
        "options": [
            ("平稳但有点低沉", [3, 1, 0, 2]),
            ("时而高时而低，起伏较大", [0, 3, 2, 1]),
        ]
    },
    {
        "question": "如果可以自由安排明天，你倾向于……",
        "options": [
            ("列个 todo 清单效率做事", [0, 1, 3, 2]),
            ("随便走走，看看会发生什么", [2, 3, 1, 0]),
        ]
    },
    {
        "question": "当你感到累的时候，更常见的情况是……",
        "options": [
            ("身体累，想睡觉", [3, 0, 1, 2]),
            ("心累，什么都不想干", [1, 3, 0, 2]),
        ]
    },
    {
        "question": "别人眼中的你最近状态是……",
        "options": [
            ("看起来挺正常的", [3, 1, 2, 0]),
            ("好像有点忙或有点丧", [0, 3, 1, 2]),
        ]
    },
]

# 结果类型数据
result_types = [
    {
        "name": "稳定蓄力型",
        "description": "你目前处于一个相对稳定的状态，虽然不是最高能量，但保持着平稳的节奏。你懂得给自己留空间，不会过度勉强自己。这种状态虽然看起来不够\"活跃\"，实际上是一种成熟的自我管理方式。保持这种节奏，偶尔给自己一点小挑战会更好。",
        "suggestion": "建议：可以尝试设定一些小型目标，感受完成的成就感。"
    },
    {
        "name": "外表摆烂内心紧绷型",
        "description": "你表面上可能看起来轻松，但实际上内心戏很丰富，想很多事情。可能对自己有一定期待，但又有点纠结或焦虑。你的内心有着潜在的动力，只是暂时没有完全释放出来。别给自己太大压力，接受当下的状态也是可以的。",
        "suggestion": "建议：试着把想法写下来，或者找人说说话，缓解内心压力。"
    },
    {
        "name": "短时爆发型",
        "description": "你有着不错的能量储备，状态好的时候效率很高，但可能持续性不太强。你适合突击式的工作方式，在短时间内集中精力完成目标。关键是找到能让你持续保持兴趣的方法，让爆发力更持久一些。",
        "suggestion": "建议：把大任务拆分成小目标，利用你的爆发力一个个完成。"
    },
    {
        "name": "低耗能求生型",
        "description": "你最近可能比较累或者处于一个低谷期，能量值较低。这没什么不好，有时候低谷就是为了更好地回升。你需要的是足够的休息和自我照顾，不要对自己要求太高。允许自己慢下来，这本身就是一种智慧。",
        "suggestion": "建议：好好休息，做一些让自己舒服的小事，给身心充电。"
    },
]

def calculate_result(answers):
    """计算结果：统计每种类型的得分"""
    scores = [0, 0, 0, 0]  # 四种类型
    for answer_idx in answers:
        scores[answer_idx] += 1
    
    # 找出最高分
    max_score = max(scores)
    # 如果有并列，取第一个（也可以用其他规则）
    result_idx = scores.index(max_score)
    return result_idx, scores

def reset_test():
    """重置测试"""
    st.session_state.step = 0
    st.session_state.answers = []
    st.session_state.started = False
    st.session_state.finished = False

# 首页
if not st.session_state.started:
    st.title("🧠 当前状态人格测试")
    st.markdown("通过几个简单问题，看看你最近更接近哪一种状态人格")
    st.write("")
    
    if st.button("开始测试", type="primary"):
        st.session_state.started = True
        st.rerun()

# 答题页面
elif st.session_state.started and not st.session_state.finished:
    current = st.session_state.step
    total = len(questions)
    
    st.progress(current / total)
    st.caption(f"第 {current + 1} 题 / 共 {total} 题")
    
    q = questions[current]
    st.subheader(q["question"])
    
    choice = st.radio("请选择：", options=[opt[0] for opt in q["options"]], key=f"q_{current}")
    
    if st.button("下一题"):
        # 获取选择索引
        selected_idx = [opt[0] for opt in q["options"]].index(choice)
        st.session_state.answers.append(selected_idx)
        st.session_state.step += 1
        
        if st.session_state.step >= total:
            st.session_state.finished = True
        
        st.rerun()

# 结果页面
elif st.session_state.finished:
    result_idx, scores = calculate_result(st.session_state.answers)
    result = result_types[result_idx]
    
    st.title("🎯 测试结果")
    st.write("")
    
    # 显示得分详情（可选）
    type_names = [r["name"] for r in result_types]
    
    # 结果卡片
    st.success(f"你是：**{result['name']}**")
    
    st.info(f"📝 {result['description']}")
    
    st.warning(f"💡 {result['suggestion']}")
    
    st.write("")
    st.markdown("---")
    
    if st.button("重新测试"):
        reset_test()
        st.rerun()