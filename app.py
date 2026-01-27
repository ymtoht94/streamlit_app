import streamlit as st
import pandas as pd
import plotly.express as px
import time

with st.spinner("データを読み込み中...", show_time=True):
    time.sleep(0.5)
if st.button("再読み込み"):
    st.rerun()

st.title('子どもの学校別学習費調査')

df1 = pd.read_csv('school_cost_01.csv')
df2 = pd.read_csv('school_cost_02.csv')

with st.sidebar:
    st.subheader('抽出条件')

    category = st.selectbox(
        '学習費区分を選択してください',
        df1['学習費区分'].unique()
    )

    item_candidates = df1[df1['学習費区分'] == category]['項目'].unique()

    items = st.multiselect(
        '表示する項目を選択してください（複数選択可）',
        item_candidates,
    )

    st.subheader('表示設定')
    school_cols = df1.columns[2:].tolist()

    schools = st.multiselect(
        '比較する学校種を選択してください',
        school_cols,
    )

    st.subheader('金額段階（構成比）')

    money_categories = df2['区分'].unique().tolist()

    money_index = st.slider(
        '表示する金額区分',
        0,
        len(money_categories) - 1,
        len(money_categories) - 1
    )

    selected_money = money_categories[money_index]
    st.caption(f'選択中：{selected_money}')

df1_filtered = df1[
    (df1['学習費区分'] == category) &
    (df1['項目'].isin(items))
]

df1_melted = df1_filtered.melt(
    id_vars=['学習費区分', '項目'],
    value_vars=schools,
    var_name='学校種',
    value_name='学習費'
)

fig1_01 = px.bar(
    df1_melted,
    x='項目',
    y='学習費',
    color='学校種',
    barmode='group',
    labels={
        '学習費': '学習費（円）',
        '項目': '調査項目',
        '学校種': '学校種'
    },
    title=f'{category}の内訳比較（棒グラフ）'
)

total_cost = df1_melted['学習費'].sum()
st.metric(label='選択条件の学習費合計', value=f'{total_cost:,.0f}円')

fig1_02 = px.area(
    df1_melted,
    x='項目',
    y='学習費',
    color='学校種',
    labels={
        '学習費': '学習費（円）',
        '項目': '調査項目',
        '学校種': '学校種'
    },
    title=f'{category}の内訳比較（面グラフ）'
)

tab1, tab2 = st.tabs(['棒グラフ', '面グラフ'])

with tab1:
    st.plotly_chart(fig1_01, use_container_width=True)

with tab2:
    st.plotly_chart(fig1_02, use_container_width=True)

df2_filtered = df2[df2['区分'] == selected_money]

df2_melted = df2_filtered.melt(
    id_vars='区分',
    var_name='学校種',
    value_name='割合'
)

fig2 = px.line(
    df2_melted,
    x='学校種',
    y='割合',
    title=f'金額区分「{selected_money}」の構成比',
    labels={'割合': '割合（%）'}
)

st.plotly_chart(fig2, use_container_width=True)

if st.checkbox('詳細データを表示'):
    st.dataframe(df1_filtered.reset_index(drop=True))
    st.dataframe(df2_filtered.reset_index(drop=True))

if st.checkbox('解釈や説明'):
    st.write('')

st.subheader('使用したWebサイトのURL')
col = st.columns(2)
col[0].link_button('参考資料1', 'https://www.e-stat.go.jp/dbview?sid=0003368823')
col[1].link_button('参考資料2', 'https://www.e-stat.go.jp/dbview?sid=0003368814')