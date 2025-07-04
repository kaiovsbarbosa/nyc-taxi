import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("Dashboard de Análise de Corridas")

@st.cache_data
def load_data():
    fato = pd.read_csv("data_warehouse/fato_corrida.csv")
    dim_tempo = pd.read_csv("data_warehouse/dim_tempo.csv")
    dim_pagamento = pd.read_csv("data_warehouse/dim_pagamento.csv")
    dim_tarifa = pd.read_csv("data_warehouse/dim_tarifa.csv")

    df = fato.merge(dim_tempo, on="dim_tempo_id", how="left") \
             .merge(dim_pagamento, on="dim_pagamento_id", how="left", suffixes=('', '_pagto')) \
             .merge(dim_tarifa, on="dim_tarifa_id", how="left", suffixes=('', '_tarifa'))

    df["tem_gorjeta"] = df["tip_amount"] > 0
    return df

df = load_data()

col1, col2 = st.columns(2)

with col1:
    st.header("Volume diário de corridas")
    corridas_por_dia = df.groupby("day")["corrida_id"].count().reset_index()
    
    fig1, ax1 = plt.subplots(figsize=(8, 4))
    ax1.bar(corridas_por_dia["day"], corridas_por_dia["corrida_id"])
    ax1.set_title("Volume diário de corridas no mês")
    ax1.set_xlabel("Dia")
    ax1.set_ylabel("Corridas")
    ax1.set_xticks(corridas_por_dia["day"])
    ax1.grid(axis='y')
    plt.tight_layout()
    st.pyplot(fig1)

    st.header("Formas de pagamento mais utilizadas")
    ranking_pagamento = df.groupby("descricao")["corrida_id"].count().reset_index().sort_values(by="corrida_id", ascending=False)

    fig3, ax3 = plt.subplots(figsize=(8, 4))
    ax3.bar(ranking_pagamento["descricao"], ranking_pagamento["corrida_id"])
    ax3.set_title("Formas de pagamento mais utilizadas")
    ax3.set_xlabel("Forma de pagamento")
    ax3.set_ylabel("Corridas")
    plt.tight_layout()
    st.pyplot(fig3)


with col2:
    st.header("Duração média por dia da semana")
    duracao_por_dia_semana = df.groupby("day_of_week")["trip_duration"].mean().reset_index()
    
    fig2, ax2 = plt.subplots(figsize=(8, 4))
    ax2.plot(duracao_por_dia_semana["day_of_week"], duracao_por_dia_semana["trip_duration"], marker='o')
    ax2.set_title("Duração média das corridas por dia da semana")
    ax2.set_xlabel("Dia da semana (1=Dom, 7=Sáb)")
    ax2.set_ylabel("Duração média (min)")
    ax2.grid(True)
    plt.tight_layout()
    st.pyplot(fig2)

    st.header("Proporção de corridas com gorjeta")
    gorjeta_analise = df.groupby("tem_gorjeta")["corrida_id"].count()
    
    fig4, ax4 = plt.subplots(figsize=(6, 4))
    labels = ["Sem gorjeta", "Com gorjeta"]
    ax4.pie(gorjeta_analise, labels=labels, autopct='%1.1f%%', startangle=140)
    ax4.set_title("Proporção de corridas com e sem gorjeta")
    plt.tight_layout()
    st.pyplot(fig4)

if st.checkbox("Mostrar dados brutos"):
    st.subheader("Dados Consolidados")
    st.dataframe(df)