import google.generativeai as genai
import pandas as pd
import numpy as np

from key import getkey

############################# CONFIGURAÇÕES ##############################################
GOOGLE_API_KEY = getkey() #COLE SUA CHAVE AQUI
genai.configure(api_key=GOOGLE_API_KEY)

MODEL = "models/embedding-001"


################################### DADOS ###############################################

Doc1= {
    "Titulo": "DIETA",
    "Conteudo": "Criação de uma dieta com alimentação personalizada"
}
Doc2= {
    "Titulo": "TREINO",
    "Conteudo": "Criação de um treino de musculação personalizado"
}
Doc3= {
    "Titulo": "SAIR",
    "Conteudo": "Sair; Encerrar o programa; fechar"
}
Doc4= {
    "Titulo": "CHATBOT",
    "Conteudo": "Tirar duvidas com o chatbot; conversar;"
}
DOCUMENTS = [Doc1, Doc2, Doc3, Doc4]

df = pd.DataFrame(DOCUMENTS)
df.columns= ["Título", "Conteúdo"]

################################ FUNÇÕES ################################################

def embed_fn(title, text):
    return genai.embed_content  (model=MODEL, 
                                 content=text, 
                                 title=title, 
                                 task_type="RETRIEVAL_DOCUMENT")["embedding"] #gera embedding da consulta

def gerar_e_buscar_consulta(consulta, base, modelo):
    embedding_consulta = genai.embed_content  (model=modelo, 
                                 content=consulta,
                                 task_type="RETRIEVAL_QUERY")["embedding"]
    produtos_escalares = np.dot(np.stack(df["embeddings"]),embedding_consulta) #compara a relevancia entre a busca e as linhas da lista

    indice = np.argmax(produtos_escalares) #localiza qual posição tem maior relevancia
    return df.iloc[indice]["Título"] #retorna o conteudo do indice com maior relevancia

def escolhaMenu ():
    df["embeddings"] = df.apply(lambda row: embed_fn(row["Título"],row["Conteúdo"]),axis=1)
    busca = input("> Crie uma dieta personalizada\n> Crie um treino personalizado\n> Converse a respeito de seu treino/dieta com nosso assistente virtual\n> Sair\n\n"+ "\033[1m=>\033[1m")
    resposta = gerar_e_buscar_consulta(busca, df, MODEL)
    return resposta

#########################################################################################################


