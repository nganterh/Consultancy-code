import streamlit as st
import utils


st.set_page_config(page_title='Ganter-Investment', layout='wide')
col1, col2 = st.beta_columns(2)

entry_type = st.sidebar.selectbox('Menu', ['Home', 'Login', 'Register'], index=0)

if entry_type == 'Home':
    st.sidebar.write('hello world!')
    
else:
    username = st.sidebar.text_input('Username')
    password = st.sidebar.text_input('Password', type='password')

    button = st.sidebar.button('Send')

    if button == True:
        col1.write(utils.login(username, password, entry_type.lower()))