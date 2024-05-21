# importando bibliotecas
import streamlit as st 
import pandas as pd

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

df_matematica = pd.read_excel("data\Matemática.xlsx", engine="openpyxl") # carregando planilha e transformando em dataframe
df_matematica['DISCIPLINA'] = "Matemática" # adicionando coluna com nome da disciplina

df_portugues = pd.read_excel("data\Português.xlsx", engine="openpyxl")
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

st.dataframe(df, use_container_width=True) # exibindo o dataframe