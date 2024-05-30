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

df_matematica = pd.read_excel("dados\Matemática.xlsx") # carregando planilha e transformando em dataframe
df_matematica['DISCIPLINA'] = "Matemática" # adicionando coluna com nome da disciplina

df_portugues = pd.read_excel("dados\Português.xlsx")
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

df["NOTA"] = df[['AV1', 'AV2', 'AV3']].mean(axis=1).apply(lambda x: f"{x:.2f}").astype(float) # criando uma coluna que recebe a média das AVs

st.write("")

with st.sidebar:  # Cria uma barra lateral no aplicativo Streamlit
    st.header("Filtros")  # Adiciona um cabeçalho "Filtros" na barra lateral

    df_ordenado_por_matricula = df.sort_values(by="MATRÍCULA")  # Ordena o DataFrame pela coluna "MATRÍCULA"
    opcoes_matricula = df_ordenado_por_matricula["MATRÍCULA"].tolist()  # Cria uma lista de matrículas a partir do DataFrame ordenado
    opcoes_matricula.insert(0, 'Todas')  # Insere a opção "Todas" no início da lista de matrículas

    input_matricula = st.selectbox("Matrícula", opcoes_matricula, key="sidebar_input_matricula")  # Cria uma caixa de seleção para matrícula com as opções da lista

    opcoes_genero = st.multiselect(
        "Gênero",
        df["GÊNERO"].unique(), default=df["GÊNERO"].unique(), key="sidebar_multi_genero"
    )  # Cria uma caixa de seleção múltipla para gênero com as opções únicas da coluna "GÊNERO" do DataFrame

    opcoes_disciplina = st.multiselect(
        "Disciplina",
        df["DISCIPLINA"].unique(), default=df["DISCIPLINA"].unique(), key="sidebar_multi_disciplina"
    )  # Cria uma caixa de seleção múltipla para disciplina com as opções únicas da coluna "DISCIPLINA" do DataFrame

    opcoes_internet = st.multiselect(
        "Acesso à internet",
        df["INTERNET"].unique(), default=df["INTERNET"].unique(), key="sidebar_multi_internet"
    )  # Cria uma caixa de seleção múltipla para acesso à internet com as opções únicas da coluna "INTERNET" do DataFrame

    df_ordenado_por_idade = df.sort_values(by="IDADE")  # Ordena o DataFrame pela coluna "IDADE"
    opcoes_idade = df_ordenado_por_idade["IDADE"].tolist()  # Cria uma lista de idades a partir do DataFrame ordenado

    min_opcoes_idade, max_opcoes_idade = st.select_slider(
        "Faixa etária", 
        options=opcoes_idade, 
        value=(min(opcoes_idade), max(opcoes_idade)), 
        key="sidebar_slider_idade"
    )  # Cria um seletor deslizante para faixa etária com o valor mínimo e máximo da lista de idades

    df_ordenado_por_notas = df.sort_values(by="NOTA")  # Ordena o DataFrame pela coluna "NOTA"
    opcoes_notas = df_ordenado_por_notas["NOTA"].tolist()  # Cria uma lista de notas a partir do DataFrame ordenado

    min_opcoes_notas, max_opcoes_notas = st.select_slider(
        "Faixa de nota", 
        options=opcoes_notas, 
        value=(min(opcoes_notas), max(opcoes_notas)), 
        key="sidebar_slider_notas"
    )  # Cria um seletor deslizante para faixa de notas com o valor mínimo e máximo da lista de notas

    df_ordenado_por_faltas = df.sort_values(by="FALTAS")  # Ordena o DataFrame pela coluna "FALTAS"
    opcoes_faltas = df_ordenado_por_faltas["FALTAS"].tolist()  # Cria uma lista de faltas a partir do DataFrame ordenado

    min_opcoes_faltas, max_opcoes_faltas = st.select_slider(
        "Quantidade de faltas", 
        options=opcoes_faltas, 
        value=(min(opcoes_faltas), max(opcoes_faltas)), 
        key="sidebar_slider_faltas"
    )  # Cria um seletor deslizante para quantidade de faltas com o valor mínimo e máximo da lista de faltas

    df_ordenado_por_reprovacoes = df.sort_values(by="REPROVAÇÕES")  # Ordena o DataFrame pela coluna "REPROVAÇÕES"
    opcoes_reprovacoes = df_ordenado_por_reprovacoes["REPROVAÇÕES"].tolist()  # Cria uma lista de reprovações a partir do DataFrame ordenado

    min_opcoes_reprovacoes, max_opcoes_reprovacoes = st.select_slider(
        "Quantidade de reprovações", 
        options=opcoes_reprovacoes, 
        value=(min(opcoes_reprovacoes), max(opcoes_reprovacoes)), 
        key="sidebar_slider_reprovacoes"
    )  # Cria um seletor deslizante para quantidade de reprovações com o valor mínimo e máximo da lista de reprovações

    aplicar_filtros = st.button("Aplicar", use_container_width=True, key="btn_aplicar_sidedar")  # Cria um botão para aplicar os filtros

    if aplicar_filtros:  # Verifica se o botão "Aplicar" foi pressionado
        if input_matricula == "Todas":  # Verifica se a opção "Todas" foi selecionada para matrícula
            df_filtrado = df[
                (df["GÊNERO"].isin(opcoes_genero)) & 
                (df["DISCIPLINA"].isin(opcoes_disciplina)) & 
                (df["INTERNET"].isin(opcoes_internet)) & 
                (df["IDADE"] >= min_opcoes_idade) & (df["IDADE"] <= max_opcoes_idade) & 
                (df["NOTA"] >= min_opcoes_notas) & (df["NOTA"] <= max_opcoes_notas) & 
                (df["FALTAS"] >= min_opcoes_faltas) & (df["FALTAS"] <= max_opcoes_faltas) & 
                (df["REPROVAÇÕES"] >= min_opcoes_reprovacoes) & (df["REPROVAÇÕES"] <= max_opcoes_reprovacoes)
            ]  # Filtra o DataFrame de acordo com os filtros selecionados
        else:
            df_filtrado = df[
                (df["MATRÍCULA"] == input_matricula) &
                (df["GÊNERO"].isin(opcoes_genero)) & 
                (df["DISCIPLINA"].isin(opcoes_disciplina)) & 
                (df["INTERNET"].isin(opcoes_internet)) & 
                (df["IDADE"] >= min_opcoes_idade) & (df["IDADE"] <= max_opcoes_idade) & 
                (df["NOTA"] >= min_opcoes_notas) & (df["NOTA"] <= max_opcoes_notas) & 
                (df["FALTAS"] >= min_opcoes_faltas) & (df["FALTAS"] <= max_opcoes_faltas) & 
                (df["REPROVAÇÕES"] >= min_opcoes_reprovacoes) & (df["REPROVAÇÕES"] <= max_opcoes_reprovacoes)
            ]  # Filtra o DataFrame de acordo com os filtros selecionados, incluindo a matrícula específica
    else:
        df_filtrado = df.copy()  # Se o botão "Aplicar" não foi pressionado, cria uma cópia do DataFrame original

c1, c2, c3, c4, c5 = st.columns(5, gap='large') # definindo um "espaço" que será dividido em 5 colunas, para receber as métricas
with c1:
    qtd_estudantes = df_filtrado['MATRÍCULA'].nunique() # contando quantidade de estudantes
    st.metric("Quantidade de estudantes", qtd_estudantes) # exibindo a quantidade de estudantes
with c2:
    soma_reprovacoes = df_filtrado['REPROVAÇÕES'].sum() # somando todas as quantidades de reprovações
    st.metric("Total de reprovações", soma_reprovacoes) # exibindo a quantidade de reprovações
with c3:
    total_faltas = df_filtrado['FALTAS'].sum() # somando todas as quantidades de faltas
    st.metric("Total de faltas", total_faltas) # exibindo a quantidade de faltas
with c4:
    qtd_estudantes_mat = df_filtrado[df_filtrado['DISCIPLINA'] == 'Matemática']['MATRÍCULA'].nunique() # contando quantidade de estudantes na disciplina de Matemática
    soma_notas_mat = df_filtrado[df_filtrado['DISCIPLINA'] == 'Matemática']['NOTA'].sum() # somando todas as notas dos estudantes na disciplina de Matemática
    media_geral_mat = soma_notas_mat / qtd_estudantes_mat # calculando a média geral da disciplina de Matemática
    st.metric("Média geral de Matemática", f"{media_geral_mat:.2f}") # exibindo a média formatada
with c5:
    quantidade_portugues = df_filtrado[df_filtrado['DISCIPLINA'] == 'Português']['MATRÍCULA'].nunique() # contando quantidade de estudantes na disciplina de Português
    soma_notas_port = df_filtrado[df_filtrado['DISCIPLINA'] == 'Português']['NOTA'].sum() # somando todas as notas dos estudantes na disciplina de Português
    media_geral_port = soma_notas_port / quantidade_portugues # calculando a média geral da disciplina de Português
    st.metric("Média geral de Português", f"{media_geral_port:.2f}") # exibindo a média formatada

st.write("")

t1, t2 = st.tabs(["Dashboard", "Tabelas"]) # cria duas abas chamadas "Dashboard" e "Tabelas"

with t1: # com o conteúdo da aba "Dashboard"

    c1, c2 = st.columns(2, gap='large') # cria duas colunas dentro da aba com um grande espaço entre elas

    with c1: # com o conteúdo da coluna c1
        def criar_grafico_pizza(df_filtrado):  # define uma função para criar um gráfico de pizza/rosca
            fig = px.pie(df_filtrado, names='DISCIPLINA', hole=0.5) # cria um gráfico de rosca usando Plotly Express com base na coluna 'DISCIPLINA'
            fig.update_traces(textposition='inside', textinfo='value+percent')  # atualiza a posição do texto e as informações exibidas no gráfico
            fig.update_layout(title_text="Estudantes por Disciplinas") # define o título do gráfico
            return fig # retorna o gráfico criado
        st.plotly_chart(criar_grafico_pizza(df_filtrado)) # exibe o gráfico no Streamlit

        def criar_grafico_barras_agrupadas(df_filtrado): # define uma função para criar um gráfico de barras agrupadas
            df_grafico_barras_agrupadas_2 = df_filtrado.groupby(["GÊNERO", "IDADE"], as_index=False).sum() # agrupa os dados por 'GÊNERO' e 'IDADE' e soma as colunas numéricas
            fig = px.bar(df_grafico_barras_agrupadas_2, x='IDADE', y='FALTAS', text='FALTAS', barmode='group', color='GÊNERO') # cria um gráfico de barras usando Plotly Express
            fig.update_layout(title_text="Faltas por Idade e Gênero") # define o título do gráfico
            return fig # retorna o gráfico criado
        st.plotly_chart(criar_grafico_barras_agrupadas(df_filtrado)) # exibe o gráfico no Streamlit

    with c2: # com o conteúdo da coluna c2
        def criar_grafico_barras_vertical(df_filtrado): # define uma função para criar um gráfico de barras na vertical
            df_grafico_barras = df_filtrado.groupby(["INTERNET"]).size().reset_index(name='QUANTIDADE') # agrupa os dados pela coluna 'INTERNET' e conta as ocorrências
            fig = px.bar(df_grafico_barras, x='INTERNET', y='QUANTIDADE', text=df_grafico_barras["QUANTIDADE"]) # cria um gráfico de barras usando Plotly Express
            fig.update_traces(texttemplate='%{text}', textposition='auto') # atualiza o template e a posição do texto no gráfico
            fig.update_layout(title_text="Estudantes por Acesso à Internet") # define o título do gráfico
            return fig # retorna o gráfico criado
        st.plotly_chart(criar_grafico_barras_vertical(df_filtrado)) # exibe o gráfico no Streamlit

        def criar_grafico_barras_horizontal(df_filtrado): # define uma função para criar um gráfico de barras na horizontal por disciplina
            df_grafico_barras_agrupadas = df_filtrado.groupby(['DISCIPLINA'], as_index=False).sum() # agrupa os dados pela coluna 'DISCIPLINA' e soma as colunas numéricas (REPROVAÇÕES)
            fig = px.bar(df_grafico_barras_agrupadas, x='REPROVAÇÕES', y='DISCIPLINA', text='REPROVAÇÕES', color='DISCIPLINA') # cria um gráfico de barras usando Plotly Express
            fig.update_layout(title_text="Reprovações por Disciplina") # define o título do gráfico
            return fig # retorna o gráfico criado
        st.plotly_chart(criar_grafico_barras_horizontal(df_filtrado)) # exibe o gráfico no Streamlit

    def criar_grafico_linhas(df_filtrado): # define uma função para criar um gráfico de linhas
        df_grafico_linhas = df_filtrado.groupby(['GÊNERO', 'IDADE']).size().reset_index(name='QUANTIDADE') # agrupa os dados por 'GÊNERO' e 'IDADE' e conta as ocorrências
        fig = px.line(df_grafico_linhas, x='IDADE', y='QUANTIDADE', color='GÊNERO', text="QUANTIDADE") # cria um gráfico de barras usando Plotly Express
        fig.update_traces(texttemplate='%{text}', textposition='top right') # atualiza o template e a posição do texto no gráfico
        fig.update_layout(title_text="Estudantes por Idade e Gênero") # define o título do gráfico
        return fig # retorna o gráfico criado
    st.plotly_chart(criar_grafico_linhas(df_filtrado), use_container_width=True) # exibe o gráfico no Streamlit, usando toda largura do containers

with t2: # com o conteúdo da aba "Tabelas"
    st.write("")

    c1, c2 = st.columns(2, gap='large')  # Cria duas colunas com um grande espaçamento entre elas
    with c1:  # Trabalha com a primeira coluna
        st.markdown("##### Top 5 - Notas mais baixas em Português")  # Adiciona um título para a tabela de notas baixas em Português
        ranking_notas_baixas_portugues = df_filtrado[df_filtrado['DISCIPLINA'] == 'Português']  # Filtra o DataFrame para selecionar apenas as notas de Português
        ranking_notas_baixas_portugues = ranking_notas_baixas_portugues.nsmallest(5, 'NOTA')[['MATRÍCULA', 'DISCIPLINA', 'NOTA']].reset_index(drop=True)  # Seleciona as 5 menores notas de Português e redefine os índices
        ranking_notas_baixas_portugues['NOTA'] = ranking_notas_baixas_portugues['NOTA'].apply(lambda x: f"{x:.2f}")  # Formata as notas para 2 casas decimais
        st.dataframe(ranking_notas_baixas_portugues, use_container_width=True)  # Exibe o DataFrame formatado na coluna, ajustando à largura do container

    with c2:  # Trabalha com a segunda coluna
        st.markdown("##### Top 5 - Notas mais baixas em Matemática")  # Adiciona um título para a tabela de notas baixas em Matemática
        ranking_notas_baixas_matematica = df_filtrado[df_filtrado['DISCIPLINA'] == 'Matemática']  # Filtra o DataFrame para selecionar apenas as notas de Matemática
        ranking_notas_baixas_matematica = ranking_notas_baixas_matematica.nsmallest(5, 'NOTA')[['MATRÍCULA', 'DISCIPLINA', 'NOTA']].reset_index(drop=True)  # Seleciona as 5 menores notas de Matemática e redefine os índices
        ranking_notas_baixas_matematica['NOTA'] = ranking_notas_baixas_matematica['NOTA'].apply(lambda x: f"{x:.2f}")  # Formata as notas para 2 casas decimais
        st.dataframe(ranking_notas_baixas_matematica, use_container_width=True)  # Exibe o DataFrame formatado na coluna, ajustando à largura do container
    
    st.dataframe(df_filtrado, use_container_width=True) # exibindo o dataframe

    df_csv = df_filtrado.to_csv(index=False)  # Converte o DataFrame filtrado para o formato CSV, sem incluir o índice

    st.download_button(
        label="Download",  # Texto do rótulo do botão
        data=df_csv,  # Dados a serem baixados (conteúdo do arquivo CSV)
        file_name="performance_estudantes",  # Nome do arquivo para download
        mime="text/csv"  # Tipo MIME do arquivo, indicando que é um arquivo CSV
    )  # Cria um botão para download do arquivo CSV com o conteúdo do DataFrame filtrado