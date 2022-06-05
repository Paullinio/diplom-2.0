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


def UI(df):
	def change_window(current_state, input_id):
		try:
			st.session_state['current_input'] = st.session_state.input
		except:
			pass
		st.session_state['current_state'] = current_state
		st.session_state['current_job'] = input_id
	if 'current_state' not in st.session_state:
		st.session_state['current_state'] = 'welcome_window'
	if 'current_job' not in st.session_state:
		st.session_state['current_job'] = 0
	if 'current_input' not in st.session_state:
		st.session_state['current_input'] = ''
	top = rec_list(df)
	dataset = st.container()
	with dataset:
		#st.write(st.session_state)
		if st.session_state['current_state'] == 'welcome_window':
			st.header('Job searcher')
			st.subheader('This is where you can find the job of your dream')
			with st.container():
				input_col, search_col = st.columns([6,1])
				with input_col:
					input_text = st.text_input('Your dream job', key = 'input', on_change = change_window, args = ['list_of_jobs', st.session_state['current_job']])
		elif st.session_state['current_state'] == 'list_of_jobs':
			
			with st.container():
				with st.container():
					input_col, back_col = st.columns([9,4])
					with input_col:
						input_text = st.text_input('Your dream job', st.session_state['current_input'], key = 'input', on_change = change_window, args = ['list_of_jobs', st.session_state['current_job']])
						st.session_state['current_input'] = input_text 
					with back_col:
						st.text('Go back')
						back_butt = st.button('Back to homescreen', on_click = change_window, args = ['welcome_window', st.session_state['current_job']])
			find_smth = False
			for index, row in df.iterrows():
				if input_text.lower() in row['Business Title'].lower() or input_text.lower() in row['Agency'].lower():
					with st.form(key = 'search_job' + str(index)):
							st.header(row['Business Title'])
							st.subheader(row['Agency'])
							st.form_submit_button('See more', on_click = change_window, args = ['job', row['Job ID']])
					find_smth = True
			if not find_smth:
				st.header('Oops! ☹️')
				st.subheader('Sorry, we could not find ' + input_text + ' for you. Try something else')
				if input_text.lower() == 'gay porn' or input_text.lower() == 'гей порно' or input_text.lower() == 'gachi' or input_text.lower() == 'гачи':
					st.text('Це вже по нашому! Welcome to the club, buddy! 💪')

				elif sum([word in input_text.lower() for word in ['cock', 'dick', 'pussy', 'penis', 'porn', 'хуй', 'пизда', 'залупа', 'вагина', 'ебать', 'порно',  'жопа', 'дупа']]):
					st.text('І не соромно тобі тут таке шукати?')
		
		elif st.session_state['current_state'] == 'job':
			current_job = df[df['Job ID'] == st.session_state['current_job']].iloc[0]
			st.title(current_job['Business Title'])
			st.subheader(current_job['Agency'])
			st.subheader('Salary: ' + str(current_job['Salary Range From']) + ' - ' + str(current_job['Salary Range To']))
			st.header('Description')
			with st.container():
				st.write(current_job['Job Description'])
			st.header('Requirements')
			with st.container():
				st.write(current_job['Minimum Qual Requirements'])
			st.header('Similar vacancies')
			for job in top[current_job['Job ID']][:5]:
				with st.form(key = 'top_job' + str(job)):
					st.header(df[df['Job ID'] == job].iloc[0]['Business Title'])
					st.subheader(df[df['Job ID'] == job].iloc[0]['Agency'])
					st.form_submit_button('See more', on_click = change_window, args = ['job', job])
			
			back_butt = st.button('Back to list', key = 'search_form' , on_click = change_window, args = ['list_of_jobs', st.session_state['current_job']])



UI(df)







