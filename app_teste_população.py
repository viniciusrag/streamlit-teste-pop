import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ------------------------------
# Função para exibir a página de gráfico
# ------------------------------
def pagina_graficos(df):
    st.header("📊 Visualização de População por Cidade")

    cidades_selecionadas = st.multiselect(
        "Selecione as cidades:",
        options=df["Cidade"].tolist(),
        default=df["Cidade"].tolist()
    )

    df_filtrado = df[df["Cidade"].isin(cidades_selecionadas)]

    if df_filtrado.empty:
        st.warning("Nenhuma cidade selecionada.")
        return

    # Estatísticas
    st.subheader("📌 Estatísticas")
    cidade_max = df_filtrado.loc[df_filtrado["População"].idxmax()]
    cidade_min = df_filtrado.loc[df_filtrado["População"].idxmin()]

    col1, col2, col3 = st.columns(3)
    col1.metric("População Total", f"{df_filtrado['População'].sum():,}")
    col2.metric("Cidade mais populosa", f"{cidade_max['Cidade']} ({cidade_max['População']:,})")
    col3.metric("Cidade menos populosa", f"{cidade_min['Cidade']} ({cidade_min['População']:,})")

    # Tipo de gráfico
    tipo_grafico = st.radio("Escolha o tipo de gráfico:", ["Barras", "Linha", "Pizza"])

    # Gráfico
    st.subheader("📈 Gráfico")
    fig, ax = plt.subplots()
    if tipo_grafico == "Barras":
        ax.bar(df_filtrado["Cidade"], df_filtrado["População"], color="royalblue")
    elif tipo_grafico == "Linha":
        ax.plot(df_filtrado["Cidade"], df_filtrado["População"], marker="o", color="green")
    elif tipo_grafico == "Pizza":
        ax.pie(df_filtrado["População"], labels=df_filtrado["Cidade"], autopct="%1.1f%%", startangle=90)
        ax.axis("equal")
    st.pyplot(fig)

    # Tabela
    st.subheader("📋 Tabela de Dados")
    st.dataframe(df_filtrado.reset_index(drop=True))

# ------------------------------
# Função para exibir a página de edição
# ------------------------------
def pagina_edicao(df):
    st.header("📝 Adicionar Nova Cidade")

    with st.form("form_adicao"):
        nova_cidade = st.text_input("Nome da cidade")
        nova_populacao = st.number_input("População", min_value=0, step=1000)
        enviar = st.form_submit_button("Adicionar")

        if enviar and nova_cidade.strip():
            df.loc[len(df)] = [nova_cidade.strip(), nova_populacao]
            st.success(f"Cidade '{nova_cidade}' adicionada com sucesso!")

    st.subheader("📋 Cidades Atuais")
    st.dataframe(df.reset_index(drop=True))

# ------------------------------
# Início do App
# ------------------------------
st.set_page_config(page_title="População por Cidade", layout="centered")

# Dados iniciais
if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame({
        "Cidade": ["Florianópolis", "Blumenau", "Joinville", "Chapecó", "Criciúma"],
        "População": [508826, 361261, 616323, 224013, 219393]
    })

# Menu lateral
pagina = st.sidebar.selectbox("Navegar para:", ["📊 Visualização Gráfica", "📝 Edição de Dados"])

# Roteamento
if pagina == "📊 Visualização Gráfica":
    pagina_graficos(st.session_state.df)
elif pagina == "📝 Edição de Dados":
    pagina_edicao(st.session_state.df)
