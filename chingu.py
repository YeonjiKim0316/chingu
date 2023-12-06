import streamlit as st
import numpy as np
import pandas as pd
from io import BytesIO

st.image('https://i.imgur.com/rODJ5QF.jpg', use_column_width="always")

password = st.text_input('비밀번호를 입력하세요')

def filter_names(woori_ai, skipped_people):
    filtered_list = [name for name in woori_ai if name not in skipped_people]
    return filtered_list

def chingu(num, woori_ai):
    g_num = num
    woori_ai = np.array(woori_ai)
    left = []

    # 랜덤으로 팀 생성
    # 팀당 인원 수 = g_num
    groups = np.array(np.random.choice(woori_ai, (int(len(woori_ai)/g_num), g_num), replace=False))

    for i in woori_ai:
        if i not in groups:
            left.append(i)

    def make_tables(table):
        table = np.array(table)
        temp = [[] for j in range(len(table))]
        
        # len(table) == 5
        for j in range(len(table)):
            for i, s in enumerate(table.T):
                s = np.roll(s, i*j)
                # print(s, i, j, 'rolled s, i ,j')
                temp[j].append(list(s))
        tables = np.array(temp)
        return tables


    # 4x5=20 처럼 팀 인원 딱 안맞으면 빈자리에 None값 삽입
    if len(left) > 0:
        left = np.array([np.pad(left, (0, g_num), 'constant', constant_values=None)[:g_num]])
        groups = np.append(groups, left, axis=0)
    else:
        pass

    # 겹치지 않게 테이블 만들기
    temp_table = make_tables(groups)

    # 마지막 행렬 뒤집어서 추가
    temp = [[] for j in range(len(groups))]
    tables = []

    for i in range(len(temp_table)):
        temp[i] = temp_table[i].T
    temp.append(temp[-2].T)

    for k in temp:
        tables.append(k)

    return tables

if password == 'woorifisa2!':
    col1, col2 = st.columns(2)

    with col1:
        num = st.number_input('몇 명으로 한 조를 구성할까요?',  value=4)

        skipped_people = st.text_input('오늘 안 온 사람 이름을 띄어쓰기와 함께 입력하세요. 예: 신짱구 신짱아')
        woori_ai = ["김가영", "김광열", "김민준", "김세은", "김윤성", "김준우", "김찬기",\
                "류준규", "박명우", "박예선", "백성욱", "신연재", "우선주", "우준희", "윤종욱", \
                "이민수", "이한슬", "장유진", "장정우", "최현규", "한상민", "황지혜"]
        skipped_people = skipped_people.split(' ')
        
        result = filter_names(woori_ai, skipped_people)
        
        button = st.button("뽑기")
    
    with col2:
        if button:
            st.balloons()
            tables = chingu(num, woori_ai)

            show_table = pd.DataFrame(tables[0])
            st.data_editor(show_table)



