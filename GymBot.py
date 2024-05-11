import google.generativeai as genai
import re

################################ CONFIGURAÇÕES ##############################################

from key import getkey
from embedding import escolhaMenu
from botIA import chatbot, dietabot, treinobot
GOOGLE_API_KEY = getkey() #COLE SUA CHAVE AQUI
genai.configure(api_key=GOOGLE_API_KEY)

########################################## INTERFACE ##############################################

print("   \033[1m=====Seja Bem vindo(a) ao GymBot, seu robô de auxílio fitness=====\033[0m\n\n")
print ("\033[1mInsira suas informações:\033[0m")

nome= input("Insira seu nome\n=>")
while True:  
  sexo= input("SEXO: 1- Masculino, 2- Feminino\n=>")
  if sexo =="1":
    print("Sexo selecionado: Masculino")
    sexo = "homem"
    break
  if sexo=="2":
    print("Sexo selecionado: Feminino")
    sexo = "mulher"
    break
  else:
    print ("Opção inválida. Digite 1 para Masculino ou 2 para Feminino.")

altura = input("Insira sua altura em metros:\n=>")
idade = input ("Quantos anos você tem?\n=>")
peso = input ("Insira seu peso:\n=>")

while True:
  print(f"\033[1mBem vindo(a) {nome}\n\nAgora com seus dados cadastrado, escolha qual opção você deseja utilizar:\033[0m")
  escolha = escolhaMenu()
  if escolha == "DIETA":
    print("VOCE ESCOLHEU DIETA")
    dietabot(sexo=sexo, altura=altura, peso= peso, idade=idade)
    
  if escolha == "TREINO":
    print("VOCE ESCOLHEU TREINO")
    treinobot (sexo=sexo, altura=altura, peso=peso, idade=idade)

  if escolha == "CHATBOT":
    print ("VOCE CONVERSARÁ COM NOSSO CHATBOT\n\n")
    chatbot()
  if escolha == "SAIR":
    print("\033[1mObrigado por utilizar nosso serviço!\033[0m")
    break
    
#########################################################################################################




