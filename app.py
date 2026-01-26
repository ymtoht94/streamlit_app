<<<<<<< HEAD
import streamlit as st
import pandas as pd
import plotly.express as px

st.title('子どもの学校別学習費調査')

df = pd.read_csv('school_cost_01.csv')

with st.sidebar:
<<<<<<< HEAD
    st.subheader('抽出条件')

    category = st.selectbox('学習費区分を選択してください',
                            df['学習費区分'].unique())

    items = st.multiselect('表示する項目を選択してください（複数選択可）',
                           df[df['学習費区分'] == category]['項目'].unique(),
                           default=df[df['学習費区分'] == category]['項目'].unique()[0])

    st.subheader('')