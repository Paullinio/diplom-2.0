import pandas as pd
import numpy as np
import string
import math
import streamlit as st

df = pd.read_csv('nyc-jobs-1.csv')[['Job ID','Agency','Business Title','Salary Range From','Salary Range To','Job Description','Minimum Qual Requirements','Preferred Skills']].drop_duplicates().head(250)
df.fillna('')
@st.cache
def rec_list(df):
    def cos(x, y):
        v1 = np.array(list(x.values()))
        v2 = np.array(list(y.values()))
        return(np.dot(v1, v2)/(np.linalg.norm(v1)*np.linalg.norm(v2)))
    def get_rec(vacancy):
        vac_list = set(df['Job ID'][df['Job ID'] != vacancy])
        top = dict()
        for vac in vac_list:
            top[vac] = cos(TF_IDF[vacancy], TF_IDF[vac])
        top = {k: v for k, v in sorted(top.items(), key=lambda item: item[1], reverse = True)}
        #return dict(zip(list(top.keys())[:5], list(top.values())[:5]))
        lst = top.keys()
        st = set(lst)
        return list(lst)
    df['clear'] = df['Job Description'].str.lower().str.translate(str.maketrans('', '', string.punctuation))
    Bag = dict(zip(df['Job ID'], [i.split() for i in df['clear']]))
    all_words = set().union(*Bag.values())
    IDF = dict()
    for word in all_words:
        count = sum([word in descr for descr in df['clear']])
        IDF[word] = math.log(len(df)/count)
    TF_IDF = dict()
    for key in Bag.keys():
        for word in all_words:
            DF = Bag[key].count(word)/len(Bag[key])
            if key in TF_IDF.keys():
                TF_IDF[key][word] = DF*IDF[word]
            else:
                TF_IDF[key] = {word : DF*IDF[word]}
    rec_dict = dict()
    for id in df['Job ID']:
        rec_dict[id] = get_rec(id)
    return rec_dict





def ui2(df):
    side = st.sidebar
    dataset = st.container()
    top = rec_list(df)
    if 'current_job' not in st.session_state:
        st.session_state['current_job'] = df.iloc[0]
    with side:
        search = st.text_input('Search')
        for index, row in df.iterrows():
            try:
                title = row['Business Title'] + ' in ' + row['Agency']
                if search.lower() in title.lower():
                    cont = st.button(title)
                else:
                    continue
            except:
                continue
            if cont:
                st.session_state.current_job = row
    def new_job(j):
        st.session_state.current_job = df[df['Job ID'] == j].iloc[0]

    with dataset:
        st.title(st.session_state.current_job['Business Title'])
        st.subheader(st.session_state.current_job['Agency'])
        st.subheader('Salary: ' + str(st.session_state.current_job['Salary Range From']) + ' - ' + str(st.session_state.current_job['Salary Range To']))
        st.header('Description')
        with st.container():
            st.write(st.session_state.current_job['Job Description'])
        st.header('Requirements')
        with st.container():
            st.write(st.session_state.current_job['Minimum Qual Requirements'])
      #  if len(st.session_state.current_job['Preferred Skills']) != 0:
   #         st.header('Preferred Skills')
    #        with st.container():
     #           st.write(st.session_state.current_job['Preferred Skills'])
        st.header('Similar vacancies')
        count = 0
        for j in top[st.session_state.current_job['Job ID']]:
            title = str(df[df['Job ID'] == j].iloc[0]['Business Title']) + ' in ' + df[df['Job ID'] == j].iloc[0]['Agency']
            try:
                button = st.button(title, key = 'new_job_offer' ,on_click=new_job, args=[j])
                count += 1
            except: continue
            if count == 5: break


ui2(df)





