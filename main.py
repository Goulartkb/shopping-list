import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Tenta carregar o arquivo de compras ou cria um DataFrame vazio
try:
    dados = pd.read_csv("compras.csv")
except FileNotFoundError:
    dados = pd.DataFrame({"Produto": [], "Preco": []})
    dados.to_csv("compras.csv", index=False)

# Título do aplicativo
st.title("Controle de Gastos")

# Entrada do orçamento
orcamento = st.number_input("Orçamento:", min_value=0.0)

# Calcula o total gasto
total = dados["Preco"].sum() if not dados.empty else 0

# Formulário para adicionar novas compras
with st.form("nova_compra"):
    produto = st.text_input("Produto:")
    preco = st.number_input("Preço:", min_value=0.0)
    if st.form_submit_button("Adicionar"):
        if preco <= (orcamento - total):
            nova_linha = pd.DataFrame({"Produto": [produto], "Preco": [preco]})
            dados = pd.concat([dados, nova_linha], ignore_index=True)
            dados.to_csv("compras.csv", index=False)
            st.success("Compra adicionada!")
        else:
            st.error("Sem orçamento suficiente!")

# Exibe informações se o orçamento foi definido
if orcamento > 0:
    # Cria gráfico do tipo Donut
    fig, ax = plt.subplots(figsize=(8, 8))
    if not dados.empty:
        produtos = dados["Produto"].tolist()
        valores = dados["Preco"].tolist()
        restante = orcamento - total
        if restante > 0:
            produtos.append("Disponível")
            valores.append(restante)
        plt.pie(valores, labels=produtos, autopct='%1.1f%%', pctdistance=0.85)
        plt.title(f"Orçamento: {orcamento}€")

        # Cria o círculo interno para transformar o gráfico em um Donut
        centro = plt.Circle((0, 0), 0.70, fc='white')
        ax.add_artist(centro)

    st.pyplot(fig)

# Exibe os dados e informações adicionais
st.dataframe(dados)
st.write(f"Total gasto: {total}€")
st.write(f"Resta: {orcamento - total}€")
