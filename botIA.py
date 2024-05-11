"""
At the command line, only need to run once to install the package via pip:

$ pip install google-generativeai
"""

import google.generativeai as genai
import re


from key import getkey
GOOGLE_API_KEY = getkey() #COLE SUA CHAVE AQUI
genai.configure(api_key=GOOGLE_API_KEY)



######################### CONFIGURAÇÕES ###########################################

genConfig = {
    "candidate_count": 1, #gemini 1.0 pro só permite a criação de 1 por vez
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1
}
safeSett = {
    "HARASSMENT": "BLOCK_NONE",
    "HATE": "BLOCK_NONE",
    "SEXUAL": "BLOCK_NONE",
    "DANGEROUS": "BLOCK_NONE",
}

model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest", generation_config=genConfig, safety_settings=safeSett)

############################# FUNÇÕES ############################################

def formataResposta(texto):
  resposta_formatada =  re.sub(r"\*\*(.*?)\*\*", r"\033[1m\1\033[0m", texto) ## deixa os textos em negrito
  resposta_formatada = re.sub(r"^\*\s*", "• ", resposta_formatada, flags=re.MULTILINE) ## substitui os asteriscos por bullet points
  return resposta_formatada


def chatbot():
  sysInstr = "Escreva as informações como se fossem para um aplicativo de auxilio para pessoas querendo melhorar seu estilo de vida; você tirará duvidas a respeito de dietas e treinos assim como auxiliar as pessoas a realizar exercícios; Dê repostas diretas ao auxiliar pessoas com exercícios; Qualquer pergunta fora da área de nutrição / atividade física, não deve ser respondida"
  model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest", generation_config=genConfig, safety_settings=safeSett, system_instruction=sysInstr)
  chat = model.start_chat(history=[])
  print ("\033[1mBEM-VINDO AO CHATBOT \033[1m")
  print ("\033[38;5;235mEscreva duvidas sobre exercícios, alimentos na sua dieta ou dicas para uma vida mais saudável\033[0m")
  prompt = input("\nO que posso fazer por você? (digite \"sair\" para encerrar):\n" + "\033[1m=>\033[0m ")
  while (prompt != "sair"):
      response = chat.send_message(prompt)
      resposta = formataResposta(response.text)
      print(resposta)
      prompt = input("\nPosso fazer mais alguma dúvida? (digite \"sair\" para encerrar):\n" + "\033[1m=>\033[0m ")
  print ("Espero que tenha ajudado!")
  while True:
     historico = input("Deseja receber todo o histórico de sua conversa com nosso bot?(Sim ou Não)\n\n=>")
     if historico == "sim" or "Sim":
        for message in chat.history: ##erro presente só no VisualStudio
          if (message.role == "user"):
             message.role= "Usuário"
          if (message.role == "model"):
             message.role = "ChatBot"
          resposta = formataResposta(f'**{message.role}**: {message.parts[0].text}')
          print (resposta)
          print('-'*100)
        print ("Fim do chat.")
        break
     if historico == "não" or "nao" or "Não" or "Nao":
        break

def dietabot(sexo, altura, peso, idade):
  #Recebendo dados
  print ("\033[1mBEM-VINDO A NOSSA CRIAÇÃO DE RECEITAS \033[1m")
  while True:
      objetivo = input ("\nQual seu objetivo com a dieta?\n1- Ganhar Massa Muscular\n2- Perder Gordura\n=> ")
      if (objetivo == "1"):
         objetivo = "Ganhar Massa Muscular"
         break
      if (objetivo =="2"):
         objetivo= "Perder Gordura"
         break
      else: print("Escolha invalida!!!")
  while True:
    carb = input ("Como deseja sua dieta?\n1- High Carb\n2- Mid Carb \n3- Low Carb\n=>")
    if (carb == "1"):
        carb = "High"
        break
    if (carb =="2"):
        carb= "Mid"
        break
    if (carb =="3"):
        carb= "Low"
        break
    else: print("Escolha invalida!!!")
  while True:
    alimentacoes = input("Quantas refeições diárias voce deseja ter em sua dieta?\n=> ")
    alimentacoes = int(alimentacoes)
    if (alimentacoes>2 and alimentacoes<=7):
       break
    else:
       print("Favor escolher um valor mais saudável!")
  while True:
      suplementos = input ("Deseja fazer uso de suplementos? \n1- Sim\n2- Não\n=> ")
      if suplementos == "1":
        suplementos = "e uso de suplementos"
        break
      if suplementos == "2":
          suplementos = ""
          break  
      else:
         print("Valor invalido!!!")  

  #Criando Prompt

  dieta = f"Crie pra mim uma dieta,  para um {sexo} de {idade} anos com {altura}m e pesa atualmente {peso}kg, {carb} carb, com o objetivo de {objetivo}; coloque {alimentacoes} alimentações diárias, {suplementos}; "
  print ("Gerando Dieta...")

  prompt_parts = [
  "Escreva as informações como se fossem para um aplicativo de nutrição, você criará dietas personalizadas com base nas informações lhe dadas",
  "input: Crie pra mim uma dieta, mid carb, para uma homem de 19 anos, com o objetivo de perder gordura; coloque 4 alimentações diárias, além de suplementos; O homem tem 1,69m e pesa atualmente 82kg",
  "output: **Objetivo:** Perda de gordura\n**Altura:** 1,69m\n**Peso atual:** 82kg\n**Refeições:** 4 por dia\n**Carboidratos:** Moderados\n\n**Suplementos Sugeridos:**\n\n• Whey Protein (após o treino)\n• Creatina (pré ou pós-treino)\n• Multivitamínico (diariamente)\n\n**Refeição 1 (Café da Manhã):**\n\n• **Opção 1:** 2 ovos mexidos + 50g de queijo branco + 1 fatia de pão integral (30g) + ½ abacate.\n• **Opção 2:** Omelete com 2 ovos + 30g de peito de peru + espinafre + 1 fatia de pão integral (30g).\n• **Opção 3:** 1 xícara de iogurte grego (170g) + 30g de granola sem açúcar + ½ xícara de frutas vermelhas.\n\n**Refeição 2 (Almoço):**\n\n• **Opção 1:** 150g de frango grelhado + 1 xícara de arroz integral (180g) + salada de folhas verdes com tomate e pepino.\n• **Opção 2:** 150g de peixe assado + 1 batata doce média (150g) + brócolis cozido no vapor.\n• **Opção 3:** Salada com 100g de atum + 1 xícara de grão-de-bico (160g) + mix de folhas verdes e vegetais coloridos.\n\n**Refeição 3 (Lanche):**\n\n• **Opção 1:** Shake de proteína com whey protein + 1 banana + água/leite. \n• **Opção 2:** Mix de castanhas (30g) + 1 maçã. \n• **Opção 3:** 2 fatias de pão integral (60g) com pasta de amendoim (2 colheres de sopa).\n\n**Refeição 4 (Jantar):**\n\n• **Opção 1:** 150g de carne moída magra + salada de folhas verdes + ½ xícara de quinoa (90g).\n• **Opção 2:** Omelete com 2 ovos + 50g de queijo cottage + salada de folhas verdes.\n• **Opção 3:** Sopa de legumes com frango desfiado + 1 fatia de pão integral (30g).\n\n**Dicas Adicionais:**\n\n• Beba bastante água ao longo do dia.\n• Priorize alimentos integrais e não processados.\n• Evite alimentos ricos em açúcar e gorduras saturadas.\n• Pratique atividades físicas regularmente.\n• Consulte um nutricionista para um acompanhamento personalizado.",
  "input: Crie pra mim uma dieta low carb, para uma mulher de 27 anos, com o objetivo de perder gordura; coloque 5 alimentações diárias; a mulher tem 1,63 e pesa 70kg" ,
  "output: **Objetivo:** Perda de gordura\n**Idade:** 27 anos\n**Altura:** 1,63m\n**Peso atual:** 70kg\n**Refeições:** 5 por dia \n**Carboidratos:** Baixos\n\n**Refeição 1 (Café da Manhã):**\n\n• **Opção 1:** 2 ovos mexidos com espinafre e tomate + 1 fatia de queijo minas (40g).       \n• **Opção 2:** Omelete com 2 ovos + cogumelos + 1 fatia de presunto magro (50g).\n• **Opção 3:** Iogurte grego natural (170g) com chia e mix de sementes (2 colheres de sopa).\n\n**Refeição 2 (Lanche da Manhã):**\n\n• **Opção 1:** 1 punhado de mix de castanhas (30g).\n• **Opção 2:** 1 fatia de queijo minas (40g) com ½ abacate.\n• **Opção 3:** Palitinhos de pepino e cenoura com patê de atum.\n\n**Refeição 3 (Almoço):**\n\n• **Opção 1:** Salada de frango grelhado (150g) com folhas verdes, tomate cereja e abacate.\n• **Opção 2:** Salmão grelhado (150g) com brócolis e couve-flor no vapor.\n• **Opção 3:** Carne moída magra (150g) refogada com legumes variados (abobrinha, pimentão, berinjela).\n\n**Refeição 4 (Lanche da Tarde):**\n\n• **Opção 1:** Shake proteico com whey protein + morangos + leite de amêndoas.\n• **Opção 2:** 2 ovos cozidos.\n• **Opção 3:** 1 fatia de queijo minas (40g) com palitinhos de pepino.\n\n**Refeição 5 (Jantar):**\n\n• **Opção 1:** Omelete com 2 ovos + queijo + espinafre e cogumelos.\n• **Opção 2:** Sopa de abóbora com gengibre e frango desfiado.\n• **Opção 3:** Salada de atum com folhas verdes, tomate cereja e azeitonas.\n\n**Dicas Adicionais:**\n\n• Beba bastante água ao longo do dia (2-3 litros).\n• Priorize alimentos integrais e não processados.\n• Evite açúcares, farinhas refinadas e alimentos processados.\n• Inclua gorduras saudáveis (abacate, azeite, castanhas).\n• Pratique atividades físicas regularmente.",
  f"input: {dieta}",  
  "output: "]

  #Recebendo Resposta
  response = model.generate_content(prompt_parts)
  resposta =formataResposta(response.text) #Formatando
  print (resposta)

  #Pause
  print ("Pressione Enter para continuar")
  input()

def treinobot(sexo, altura, peso, idade):
  
  #Recebendo dados
  while True:
      objetivo = input ("\nQual seu objetivo com o treino?\n1- Ganhar Massa Muscular\n2- Perder Gordura\n=> ")
      if (objetivo == "1"):
         objetivo = "Ganhar Massa Muscular"
         break
      if (objetivo =="2"):
         objetivo= "Perder Gordura"
         break
      else: print("Escolha invalida!!!")
      
  while True:
    dias = input ("Quantos dias na semana você pretende treinar?\n=> ")
    if int(dias)<=7 and int(dias)>=1:
        break
    else:
        print ("Favor inserir um valor válido!")
  

  #criando Prompt
  treino = f"Crie pra mim uma rotina de musculação, para um {sexo} de {idade} anos com {altura}m e pesa {peso}kg, com o objetivo de {objetivo}; a pessoa treinará {dias} dias na semana"
  print ("Gerando Treino...")
  prompt_parts = [
  "Escreva as informações como se fossem para um aplicativo de nutrição, você criará treinos  personalizadas com base nas informações lhe dadas",
  "input: Crie pra mim uma rotina de musculação, para uma mulher de 45 anos com 1,60m e pesa 72kg, com o objetivo de perder gordura; a pessoa treinará 5 dias na semana;",
  "output: **Objetivo:** Perda de Gordura & Tonificação Muscular\n\n**Nível:** Iniciante-Intermediário\n\n**Frequência:** 5 dias por semana (exemplo: Segunda, Terça, Quarta, Sexta e Sábado, com descanso na Quinta e Domingo)\n\n**Duração:** 45-60 minutos por sessão\n\n**Observação:** É crucial consultar um profissional de educação física para adaptar a rotina às suas necessidades e capacidades individuais. \n\n**Estrutura da Rotina:**\n\nA estrutura abaixo segue um sistema de treino \"AB\", dividindo os grupos musculares em dois dias, garantindo um descanso adequado entre os treinos de cada músculo.\n\n**Dia A -  Foco em membros inferiores e Core (Segunda e Sexta)**\n\n* **Aquecimento:** 10 minutos de esteira ou bicicleta (intensidade leve)\n* **Exercício 1:** Agachamento (3 séries de 12-15 repetições)\n* **Exercício 2:** Afundo (3 séries de 12-15 repetições por perna)\n* **Exercício 3:** Step-ups (3 séries de 12-15 repetições por perna)\n* **Exercício 4:** Ponte (3 séries de 15-20 repetições)\n* **Exercício 5:** Prancha (3 séries de 30-60 segundos)\n* **Alongamento:** 5-10 minutos\n\n**Dia B -  Foco em membros superiores e Core (Terça e Sábado)**\n\n* **Aquecimento:** 10 minutos de  elíptico ou remador (intensidade leve)\n* **Exercício 1:** Supino (3 séries de 12-15 repetições)\n* **Exercício 2:** Remada sentada (3 séries de 12-15 repetições)\n* **Exercício 3:** Desenvolvimento de ombros (3 séries de 12-15 repetições)\n* **Exercício 4:** Rosca direta (3 séries de 12-15 repetições)\n* **Exercício 5:** Tríceps pulley (3 séries de 12-15 repetições)\n* **Exercício 6:** Prancha lateral (3 séries de 30-60 segundos por lado)\n* **Alongamento:** 5-10 minutos\n\n**Quarta - Treino Cardiovascular & Flexibilidade**\n\n* **Cardio:** 30-45 minutos de atividade moderada como caminhada, corrida leve, natação ou bicicleta.\n* **Flexibilidade:** 15-20 minutos de alongamentos dinâmicos e estáticos para melhorar a mobilidade e prevenir lesões.\n\n**Observações Importantes:**\n\n* **Progressão:** Aumente gradualmente o peso ou a resistência dos exercícios à medida que se sentir mais forte. \n* **Descanso:** Descanse 60-90 segundos entre as séries.\n* **Postura:** Concentre-se na técnica correta dos exercícios para evitar lesões.\n* **Nutrição:** Combine a rotina com uma dieta balanceada para melhores resultados.\n* **Hidratação:** Beba bastante água durante o dia, especialmente durante e após os treinos.",
  f"input: {treino}",  
  "output: "]

  #Recebendo Resposta
  response = model.generate_content(prompt_parts)
  resposta =formataResposta(response.text)
  print (resposta)
  
  #pause
  print ("Pressione Enter para continuar")
  input()
