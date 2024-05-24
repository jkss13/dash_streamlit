# importando bibliotecas
import streamlit as st 
import pandas as pd
import plotly.express as px

# configurações da página
st.set_page_config(
    page_title="Student Performance",
    page_icon="🎓", 
    layout="wide"
)

st.image("student.jpg", use_column_width=True) # imagem
st.title("Dashboad - Performance de Estudantes") # título
st.write("Análise de performance de estudantes nas disciplinas de Português e Matemática. 🤓") # descrição

st.write("") # espaço em branco

df_matematica = pd.read_excel("dados\Matemática.xlsx", engine="openpyxl") # carregando planilha e transformando em dataframe
df_matematica['DISCIPLINA'] = "Matemática" # adicionando coluna com nome da disciplina

df_portugues = pd.read_excel("dados\Português.xlsx", engine="openpyxl")
df_portugues['DISCIPLINA'] = "Português"

df = pd.concat([df_matematica, df_portugues], ignore_index=True) # juntando os dataframes

df.columns = df.columns.str.upper()  # colocando nome das colunas em maiúsculo

df['ID'] = df.index # criando uma coluna ID que recebe o índice do dataframe

df = df[['ID', 'DISCIPLINA', 'SEX', 'AGE', 'FAILURES', 'INTERNET', 'ABSENCES', 'G1', 'G2', 'G3']] # selecionando as colunas que vamos usar

df = df.rename(columns={'ID':'MATRÍCULA',
                        'SCHOOL':'ESCOLA',
                        'SEX':'GÊNERO',
                        'AGE':'IDADE',
                        'FAILURES':'REPROVAÇÕES',
                        'ABSENCES':'FALTAS',
                        'G1':'AV1',
                        'G2':'AV2',
                        'G3':'AV3'}) # renomeando as colunas para português

df['MATRÍCULA'] = df['MATRÍCULA'].astype(str).str.zfill(5) # adicionando zeros a esquerda na coluna que recebeu o índice, para dar ideia de um número de matrícula

df = df.replace({'yes':'Sim', 'no':'Não'}) # traduzindo para português valores que estão em inglês

colunas_notas = ['AV1', 'AV2', 'AV3'] # criando lista com colunas que possuem as notas

for col in df.columns:
    if col in colunas_notas:
        df[col] = (df[col] * 10) / 20 # modificando valores das AVs proporcionalmente de 20 para a nota máxima no Brasil, que é 10

df["NOTA"] = df[['AV1', 'AV2', 'AV3']].mean(axis=1) # criando uma coluna que recebe a média das AVs

c1, c2, c3, c4, c5 = st.columns(5, gap='large') # definindo um "espaço" que será dividido em 5 colunas, para receber as métricas
with c1:
    qtd_estudantes = df['MATRÍCULA'].nunique() # contando quantidade de estudantes
    st.metric("Quantidade de estudantes", qtd_estudantes) # exibindo a quantidade de estudantes
with c2:
    soma_reprovacoes = df['REPROVAÇÕES'].sum() # somando todas as quantidades de reprovações
    st.metric("Total de reprovações", soma_reprovacoes) # exibindo a quantidade de reprovações
with c3:
    total_faltas = df['FALTAS'].sum() # somando todas as quantidades de faltas
    st.metric("Total de faltas", total_faltas) # exibindo a quantidade de faltas
with c4:
    qtd_estudantes_mat = df[df['DISCIPLINA'] == 'Matemática']['MATRÍCULA'].nunique() # contando quantidade de estudantes na disciplina de Matemática
    soma_notas_mat = df[df['DISCIPLINA'] == 'Matemática']['NOTA'].sum() # somando todas as notas dos estudantes na disciplina de Matemática
    media_geral_mat = soma_notas_mat / qtd_estudantes_mat # calculando a média geral da disciplina de Matemática
    st.metric("Média geral de Matemática", f"{media_geral_mat:.2f}") # exibindo a média formatada
with c5:
    quantidade_portugues = df[df['DISCIPLINA'] == 'Português']['MATRÍCULA'].nunique() # contando quantidade de estudantes na disciplina de Português
    soma_notas_port = df[df['DISCIPLINA'] == 'Português']['NOTA'].sum() # somando todas as notas dos estudantes na disciplina de Português
    media_geral_port = soma_notas_port / quantidade_portugues # calculando a média geral da disciplina de Português
    st.metric("Média geral de Português", f"{media_geral_port:.2f}") # exibindo a média formatada

st.write("")

t1, t2 = st.tabs(["Dashboard", "Tabelas"]) # cria duas abas chamadas "Dashboard" e "Tabelas"

with t1: # com o conteúdo da aba "Dashboard"

    c1, c2 = st.columns(2, gap='large') # cria duas colunas dentro da aba com um grande espaço entre elas

    with c1: # com o conteúdo da coluna c1
        def criar_grafico_pizza(df):  # define uma função para criar um gráfico de pizza/rosca
            fig = px.pie(df, names='DISCIPLINA', hole=0.5) # cria um gráfico de rosca usando Plotly Express com base na coluna 'DISCIPLINA'
            fig.update_traces(textposition='inside', textinfo='value+percent')  # atualiza a posição do texto e as informações exibidas no gráfico
            fig.update_layout(title_text="Estudantes por Disciplinas") # define o título do gráfico
            return fig # retorna o gráfico criado
        st.plotly_chart(criar_grafico_pizza(df)) # exibe o gráfico no Streamlit

        def criar_grafico_barras_agrupadas(df): # define uma função para criar um gráfico de barras agrupadas
            df_grafico_barras_agrupadas_2 = df.groupby(["GÊNERO", "IDADE"], as_index=False).sum() # agrupa os dados por 'GÊNERO' e 'IDADE' e soma as colunas numéricas
            fig = px.bar(df_grafico_barras_agrupadas_2, x='IDADE', y='FALTAS', text='FALTAS', barmode='group', color='GÊNERO') # cria um gráfico de barras usando Plotly Express
            fig.update_layout(title_text="Faltas por Idade e Gênero") # define o título do gráfico
            return fig # retorna o gráfico criado
        st.plotly_chart(criar_grafico_barras_agrupadas(df)) # exibe o gráfico no Streamlit

    with c2: # com o conteúdo da coluna c2
        def criar_grafico_barras_vertical(df): # define uma função para criar um gráfico de barras na vertical
            df_grafico_barras = df.groupby(["INTERNET"]).size().reset_index(name='QUANTIDADE') # agrupa os dados pela coluna 'INTERNET' e conta as ocorrências
            fig = px.bar(df_grafico_barras, x='INTERNET', y='QUANTIDADE', text=df_grafico_barras["QUANTIDADE"]) # cria um gráfico de barras usando Plotly Express
            fig.update_traces(texttemplate='%{text}', textposition='auto') # atualiza o template e a posição do texto no gráfico
            fig.update_layout(title_text="Estudantes por Acesso à Internet") # define o título do gráfico
            return fig # retorna o gráfico criado
        st.plotly_chart(criar_grafico_barras_vertical(df)) # exibe o gráfico no Streamlit

        def criar_grafico_barras_horizontal(df): # define uma função para criar um gráfico de barras na horizontal por disciplina
            df_grafico_barras_agrupadas = df.groupby(['DISCIPLINA'], as_index=False).sum() # agrupa os dados pela coluna 'DISCIPLINA' e soma as colunas numéricas (REPROVAÇÕES)
            fig = px.bar(df_grafico_barras_agrupadas, x='REPROVAÇÕES', y='DISCIPLINA', text='REPROVAÇÕES', color='DISCIPLINA') # cria um gráfico de barras usando Plotly Express
            fig.update_layout(title_text="Reprovações por Disciplina") # define o título do gráfico
            return fig # retorna o gráfico criado
        st.plotly_chart(criar_grafico_barras_horizontal(df)) # exibe o gráfico no Streamlit

    def criar_grafico_linhas(df): # define uma função para criar um gráfico de linhas
        df_grafico_linhas = df.groupby(['GÊNERO', 'IDADE']).size().reset_index(name='QUANTIDADE') # agrupa os dados por 'GÊNERO' e 'IDADE' e conta as ocorrências
        fig = px.line(df_grafico_linhas, x='IDADE', y='QUANTIDADE', color='GÊNERO', text="QUANTIDADE") # cria um gráfico de barras usando Plotly Express
        fig.update_traces(texttemplate='%{text}', textposition='top right') # atualiza o template e a posição do texto no gráfico
        fig.update_layout(title_text="Estudantes por Idade e Gênero") # define o título do gráfico
        return fig # retorna o gráfico criado
    st.plotly_chart(criar_grafico_linhas(df), use_container_width=True) # exibe o gráfico no Streamlit, usando toda largura do containers

with t2: # com o conteúdo da aba "Tabelas"
    st.dataframe(df, use_container_width=True) # exibindo o dataframe