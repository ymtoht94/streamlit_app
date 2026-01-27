import streamlit as st
import pandas as pd
import plotly.express as px

st.title('子どもの学校別学習費調査')

# データの読み込み
df = pd.read_csv('school_cost_01.csv')

with st.sidebar:
    st.subheader('抽出条件')
    
    # 1. 学習費区分（合計、学校教育費など）を選択
    category = st.selectbox('学習費区分を選択してください', 
                            df['学習費区分'].unique())
    
    # 2. 項目（授業料、遠足費など）を複数選択 
    items = st.multiselect('表示する項目を選択してください（複数選択可）', 
                           df[df['学習費区分'] == category]['項目'].unique(),
                           default=df[df['学習費区分'] == category]['項目'].unique()[0])

    st.subheader('表示設定')
    # 3. 比較したい学校種別を選択（列名から取得）
    schools = st.multiselect('比較する学校種別を選択してください',
                             df.columns[2:].tolist(),
                             default=df.columns[2:4].tolist())

# データのフィルタリング
df_filtered = df[(df['学習費区分'] == category) & (df['項目'].isin(items))]

# Plotlyで扱いやすいように、横持ちのデータを縦持ち（Long format）に変換
df_melted = df_filtered.melt(id_vars=['学習費区分', '項目'], 
                             value_vars=schools,
                             var_name='学校種別', 
                             value_name='学習費')

# グラフの作成（棒グラフ）
# 元のコードの px.scatter を、カテゴリ比較に適した px.bar に変更しています
fig = px.bar(df_melted, 
             x='項目', 
             y='学習費',
             color='学校種別',
             barmode='group',
             labels={'学習費':'学習費 (円)', '項目':'調査項目'},
             title=f'{category}の内訳比較'
            )

# グラフの表示
st.plotly_chart(fig)

# データテーブルの表示（オプション）
if st.checkbox('詳細データを表示'):
    st.dataframe(df_filtered)