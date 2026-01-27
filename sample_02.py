import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="子どもの学校別学習費調査", layout="wide")
st.title("子どもの学校別学習費調査")

df1 = pd.read_csv("school_cost_01.csv")
df2 = pd.read_csv("school_cost_02.csv")

with st.sidebar:
    st.header("抽出条件")

    category = st.selectbox(
        "学習費区分を選択",
        df1["学習費区分"].unique()
    )

    items = st.multiselect(
        "表示する項目",
        df1[df1["学習費区分"] == category]["項目"].unique(),
        default=df1[df1["学習費区分"] == category]["項目"].unique()[0]
    )

    schools = st.multiselect(
        "比較する学校種",
        df1.columns[2:].tolist(),
        default=df1.columns[2:4].tolist()
    )

    st.header("金額段階（構成比）")

    money_categories = df2["区分"].unique().tolist()

    money_index = st.slider(
        "表示する金額区分",
        0,
        len(money_categories) - 1,
        len(money_categories) - 1
    )

    selected_money = money_categories[money_index]
    st.caption(f'選択中：{selected_money}')

df1_filtered = df1[
    (df1["学習費区分"] == category) &
    (df1["項目"].isin(items))
]

df1_melted = df1_filtered.melt(
    id_vars=["学習費区分", "項目"],
    value_vars=schools,
    var_name="学校種",
    value_name="学習費"
)

df2_filtered = df2[df2["区分"] == selected_money]

df2_melted = df2_filtered.melt(
    id_vars="区分",
    var_name="学校種",
    value_name="割合"
)

col1, col2 = st.columns(2)

with col1:
    fig1 = px.bar(
        df1_melted,
        x="項目",
        y="学習費",
        color="学校種",
        barmode="group",
        labels={"学習費": "学習費（円）"},
        title=f"{category} の内訳比較"
    )
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    fig2 = px.bar(
        df2_melted,
        x="学校種",
        y="割合",
        labels={"割合": "割合（%）"},
        title=f"{selected_money} の構成比"
    )
    st.plotly_chart(fig2, use_container_width=True)

if st.checkbox("データを表示"):
    st.subheader("学習費データ")
    st.dataframe(df1_filtered)
    st.subheader("構成比データ")
    st.dataframe(df2_filtered)