import heapq
import os
from itertools import groupby

#Variáveis 
heuristica = 0
modelo = "A"
lang = "en"
objetivo = None
tamanho = 0
inicio = None
movimentos_originais = {}

# --- Dicionário de Traduções ---
textos = {
   "pt_br": {
      "lang_title": "GOTHIC LOCKPICK SOLVER",
      "lang_select": "Selecione o idioma / Select your language:",
      "opt_pt": "[1] Português (Brasil)",
      "opt_en": "[2] English",
      "err_lang": "* Opção inválida! Digite 1 ou 2.",
      "banner_sub": "Algoritimo de busca Dijkstra",
      "banner_author": "Desenvolvido por: FranciscoFernandesJr",
        
      # Tamanho
      "size_prompt": "Informe a quantidade de placas [4-7]: ",
      "size_err_num": "* ERRO! Digite apenas números inteiros válidos!\n",
      "size_err_range": "* ERRO! Tamanho deve ser entre 4 e 7!\n",
        
      # Estado Inicial
      "init_prompt": "Informe o estado inicial dos {tamanho} pinos (ex: 6 2 4 5): ",
      "init_err_len": "\n* ERRO! Quantidade esperada de números: {tamanho}. Quantidade digitada: {qtd}.",
      "init_err_char": "\n* ERRO! Caractere inválido detectado. Digite apenas números inteiros.",
      "init_err_range": "\n* ERRO! Os pinos devem estar entre [1-7].",
      
      # Movimentos
      "move_prompt": "Digite o movimento realizado pela {placa}ª placa (ex: 0 1 0 0 -1): ",
      "move_err_len": "\n* ERRO! Quantidade esperada de números: {tamanho}. Quantidade digitada: {qtd}.",
      "move_err_char": "\n* ERRO! Caractere inválido. Digite apenas -1, 0 ou 1.",
      "move_err_current": "\n* ERRO! A placa atual deve ser obrigatoriamente 1",
      "move_err_value": "\n* ERRO! Os valores devem ser estritamente -1, 0 ou 1.",
      
      # Estilo
      "style_title": "ESCOLHA O FORMATO DA SOLUÇÃO",
      "style_a": "[A] Formato Rápido (Ex: 3x -> Placa 2/A)",
      "style_b": "[B] Formato Detalhado (Ex: Movimento 1. Placa 4 -> Esquerda x3)",
      "style_c": "[C] Formato Teclas/Macro (Ex: W -> W -> D -> S -> A )",
      "style_prompt": "Digite a opção desejada (A, B ou C): ",
      "style_err": "\n* ERRO: Opção inválida! Por favor, digite apenas 'A', 'B' ou 'C'.\n",
      
      # Resumo e Configuração
      "summary_title": "RESUMO",
      "sum_size": "[0] Tamanho: ",
      "sum_init": "[1] Estado inicial: ",
      "sum_moves": "[2] Movimentos:",
      "sum_plate": "      Placa {placa} -> {mov}",
      "sum_style": "[3] Estilo: ",
      "change_prompt": "Deseja alterar algo [S/N]? ",
      "change_err_sn": "\n* ERRO! Digite apenas S ou N.",
      "change_opt_prompt": "Qual você deseja alterar [0-3]? ",
      "change_size_msg": "\nAlterar o tamanho vai reiniciar a configuração.",
      "change_init_msg": "\nRedefinindo o estado inicial...",
      "change_plate_prompt": "Qual placa deseja alterar o movimento [1-{tamanho}]? ",
      "change_plate_err_int": "\n* ERRO! Digite um número inteiro.",
      "change_plate_err_notfound": "\n* ERRO! Placa inexistente.",
      "change_style_msg": "\nRedefinindo o estilo de exibição...",
      "change_err_opt": "\n* ERRO! Opção inválida. Escolha entre 0 e 3.",
      
      # Execução
      "calc_msg": "\nCalculando a solução...",
      "no_solution": "\n Não foi possível encontrar uma solução para este estado!",
      "dir_b_right": "direita",
      "dir_b_left": "esquerda",
      "press_enter": "\nPressione ENTER para fechar..."
   },
   "en": {
    "lang_title": "GOTHIC LOCKPICK SOLVER",
    "lang_select": "Select your language / Selecione o idioma:",
    "opt_pt": "[1] Português (Brasil)",
    "opt_en": "[2] English",
    "err_lang": "* Invalid option! Type 1 or 2.",
    "banner_sub": "Dijkstra Search Algorithm",
    "banner_author": "Made By: FranciscoFernandesJr",
    
    # Tamanho
    "size_prompt": "Enter the number of plates [4-7]: ",
    "size_err_num": "* ERROR! Enter only valid integer numbers!\n",
    "size_err_range": "* ERROR! Size must be between 4 and 7!\n",
    
    # Estado Inicial
    "init_prompt": "Enter the initial state of the {tamanho} pins (e.g., 6 2 4 5): ",
    "init_err_len": "\n* ERROR! Expected amount of numbers: {tamanho}. Entered amount: {qtd}.",
    "init_err_char": "\n* ERROR! Invalid character detected. Enter only integers.",
    "init_err_range": "\n* ERROR! Pins must be between [1-7].",
    
    # Movimentos
    "move_prompt": "Enter the movement made by plate {placa} (e.g., 0 1 0 0 -1): ",
    "move_err_len": "\n* ERROR! Expected amount of numbers: {tamanho}. Entered amount: {qtd}.",
    "move_err_char": "\n* ERROR! Invalid character. Enter only -1, 0 or 1.",
    "move_err_current": "\n* ERROR! The current plate must strictly be 1",
    "move_err_value": "\n* ERROR! Values must be strictly -1, 0 or 1.",
    
    # Estilo
    "style_title": "CHOOSE SOLUTION FORMAT",
    "style_a": "[A] Fast Format (e.g., 3x -> Plate 2/A)",
    "style_b": "[B] Detailed Format (e.g., Move 1. Plate 4 -> Right x3)",
    "style_c": "[C] Keys/Macro Format (e.g., W -> W -> D -> S -> A )",
    "style_prompt": "Enter desired option (A, B or C): ",
    "style_err": "\n* ERROR: Invalid option! Please type 'A', 'B' or 'C'.\n",
    
    # Resumo e Configuração
    "summary_title": "SUMMARY",
    "sum_size": "[0] Size: ",
    "sum_init": "[1] Initial state: ",
    "sum_moves": "[2] Movements:",
    "sum_plate": "      Plate {placa} -> {mov}",
    "sum_style": "[3] Style: ",
    "change_prompt": "Do you wish to change anything [Y/N]? ",
    "change_err_sn": "\n* ERROR! Type only Y or N (or S/N).",
    "change_opt_prompt": "What do you want to change [0-3]? ",
    "change_size_msg": "\nChanging the size will reset the configuration.",
    "change_init_msg": "\nRedefining initial state...",
    "change_plate_prompt": "Which plate movement do you want to change [1-{tamanho}]? ",
    "change_plate_err_int": "\n* ERROR! Enter an integer.",
    "change_plate_err_notfound": "\n* ERROR! Plate does not exist.",
    "change_style_msg": "\nRedefining display style...",
    "change_err_opt": "\n* ERROR! Invalid option. Choose between 0 and 3.",
    
    # Execução
    "calc_msg": "\nCalculating solution...",
    "no_solution": "\n Could not find a solution for this state!",
    "dir_b_right": "right",
    "dir_b_left": "left",
    "press_enter": "\nPress ENTER to exit..."
   }
}

#Linguagem
def selecionar_linguagem():
   global lang
   while True:
      os.system('cls' if os.name == 'nt' else 'clear')
      print("=" * 55)
      print("         GOTHIC LOCKPIC SOLVER")
      print("=" * 55 + "\n")
      print("[1] Português (Brasil)")
      print("[2] English")
      escolha = input("\nSelect your language / Selecione o idioma [1/2]: ").strip()

      if escolha == "1":
         lang = "pt_br"
         break
      elif escolha == "2":
         lang = "en"
         break
      else:
         print("\n* Opção inválida! / Invalid option!")
         input("Pressione ENTER para tentar novamente...")


# --- Banner ---
def exibir_banner():   
   # Limpa a tela ao iniciar (compatível com Windows e Linux/macOS)
   os.system('cls' if os.name == 'nt' else 'clear')
    
   # Cores ANSI para o terminal
   CYAN = "\033[96m"
   AMARELO = "\033[93m"
   VERDE = "\033[92m"
   RESET = "\033[0m"

   t = textos[lang]

   print(CYAN + "=" * 115 + RESET)
   print(AMARELO + r"""
    _                _     ___  ___          _                 _                 _____       _                
   | |              | |    |  \/  |         | |               (_)               /  ___|     | |               
   | |     ___   ___| | __ | .  . | ___  ___| |__   __ _ _ __  _ ___ _ __ ___   \ `--.  ___ | |_   _____ _ __ 
   | |    / _ \ / __| |/ / | |\/| |/ _ \/ __| '_ \ / _` | '_ \| / __| '_ ` _ \   `--. \/ _ \| \ \ / / _ \ '__|
   | |___| (_) | (__|   <  | |  | |  __/ (__| | | | (_| | | | | \__ \ | | | | | /\__/ / (_) | |\ V /  __/ |   
   \_____/\___/ \___|_|\_\ \_|  |_/\___|\___|_| |_|\__,_|_| |_|_|___/_| |_| |_| \____/ \___/|_| \_/ \___|_|                                                                                                 
   """ + RESET)
   print(VERDE + f"     {t['banner_sub']} ".center(115) + RESET)
   print(CYAN + f"     {t['banner_author']}".center(115) + RESET)
   print(CYAN + "=" * 115 + RESET + "\n")

# --- Montar Puzzle ---
def pegar_tamanho():
   t = textos[lang]
   while True:
      entrada = input(t["size_prompt"])

      try:
         tamanho_novo = int(entrada)
      except ValueError:
         print(t["size_err_num"])
         continue
   
      if not 4 <= tamanho_novo <= 7:
         print(t["size_err_range"])
         continue
      
      print("-" * 55 + "\n")
      return tamanho_novo

def pegar_estado_inicial(tamanho):
   t = textos[lang]
   while True:
      novo_inicio = []
      erro = False
      entrada = input(t["init_prompt"].format(tamanho=tamanho)).replace(",", " ")
      entrada = entrada.split()
   
      if len(entrada) != tamanho:
         print(t["init_err_len"].format(tamanho=tamanho, qtd=len(entrada)))
         continue
   
      for e in entrada:
         try:
            pino = int(e)
         except ValueError:
            print(t["init_err_char"])
            erro = True
            break
   
         if not 1 <= pino <= 7:
            print(t["init_err_range"])
            erro = True
            break
   
         novo_inicio.append(pino)  
   
      if erro:
         continue
      
      print("-" * 55 + "\n")
      return tuple(novo_inicio)
      
def pegar_movimentos(tamanho, movimentos_originais=None, placa_alvo=None):
   t = textos[lang]
   if movimentos_originais is None:
      movimentos_originais = {}

   if placa_alvo is None:
      placas_para_configurar = range(1, tamanho + 1)
   else: 
      placas_para_configurar = [placa_alvo]

   for placa in placas_para_configurar:
      while True:
         entrada = input(t["move_prompt"].format(placa=placa)).replace(",", " ")
         placas = entrada.split()
         novo_movimento = []
   
         if len(placas) != tamanho:
            print(t["move_err_len"].format(tamanho=tamanho, qtd=len(placas)))
            continue
   
         for i, e in enumerate(placas):
            try:
               mov = int(e)
            except ValueError:
               print(t["move_err_char"])
               break

            if (i + 1) == placa and mov != 1:
               print(t["move_err_current"])
               break

            if mov not in (-1, 0, 1):
               print(t["move_err_value"])
               break
   
            novo_movimento.append(mov)
         else: 
            movimentos_originais[placa] = tuple(novo_movimento)
            break
   print("-" * 55 + "\n")
   return movimentos_originais

def pegar_estilo():
   t = textos[lang]
   print("\n" + "=" * 55)
   print(f"       {t['style_title']}")
   print("=" * 55)
   print(t["style_a"])
   print(t["style_b"])
   print(t["style_c"])
   print("-" * 55)
   
   while True:
      estilo = input(t["style_prompt"]).strip().upper()
      if estilo in ("A", "B", "C"):
            return estilo
      print(t["style_err"])

def exibir_resumo(tamanho, inicio, movimentos_originais, modelo):
   t = textos[lang]
   print("\n" + "=" * 55)
   print(f"       {t['summary_title']}")
   print(f"{t['sum_size']}{tamanho}")
   print(f"{t['sum_init']}{inicio}")
   print(f"{t['sum_moves']}")
   for placa, mov in movimentos_originais.items():
      print(t["sum_plate"].format(placa=placa, mov=list(mov)))
   print(f"{t['sum_style']}{modelo}")
   print("=" * 55)

def configurar_puzzle():
   t = textos[lang]
   tamanho = pegar_tamanho()
   objetivo = (4,) * tamanho
   inicio = pegar_estado_inicial(tamanho)
   movimentos_originais = pegar_movimentos(tamanho)
   modelo = pegar_estilo()
   
   movimentos_inversos = {-k: tuple(-x for x in v) for k, v in movimentos_originais.items()}
   movimentos = movimentos_originais | movimentos_inversos

   exibir_resumo(tamanho, inicio, movimentos_originais, modelo)
   
   while True:
      alterar = input(t["change_prompt"]).strip().upper()
   
      if lang == "en" and alterar == "Y":
         alterar = "S"
         
      if alterar not in ("S", "N"):
         print(t["change_err_sn"])
         continue
   
      if alterar == "N":
         break
      else: 
         opcao = input(t["change_opt_prompt"]).strip()
         
         if opcao == "0":
            print(t["change_size_msg"])
            tamanho = pegar_tamanho()
            objetivo = (4,) * tamanho
            inicio = pegar_estado_inicial(tamanho)
            movimentos_originais = pegar_movimentos(tamanho)
            
         elif opcao == "1":
            print(t["change_init_msg"])
            inicio = pegar_estado_inicial(tamanho)
               
         elif opcao == "2":
            try:
               placa_alvo = int(input(t["change_plate_prompt"].format(tamanho=tamanho)))
            except ValueError:
               print(t["change_plate_err_int"])
               continue
            if placa_alvo not in range(1, tamanho + 1):
               print(t["change_plate_err_notfound"])
               continue

            movimentos_originais = pegar_movimentos(tamanho, movimentos_originais, placa_alvo)
         
         elif opcao == "3":
            print(t["change_style_msg"])
            modelo = pegar_estilo()
         else:
            print(t["change_err_opt"])
         
         movimentos_inversos = {-k: tuple(-x for x in v) for k, v in movimentos_originais.items()}
         movimentos = movimentos_originais | movimentos_inversos

         exibir_resumo(tamanho, inicio, movimentos_originais, modelo)
   return inicio, objetivo, movimentos, modelo

# --- Gerar estados ---
def gerar_vizinhos(estado, movimentos):
   vizinhos = []

   for nome, movimento in movimentos.items():
    valido = True
    estado_multavel = list(estado)

    for i, e in enumerate(estado_multavel):
       novo_valor = e + movimento[i]
       if not 1 <= novo_valor <= 7:
         valido = False
         break
       estado_multavel[i] = novo_valor

    if valido == True:
       vizinhos.append((tuple(estado_multavel), nome))

   return vizinhos

# --- Encontrar caminho com Dijkstra ---
def resolver(inicio, objetivo, movimentos, heuristica):
   fila = []
   custos = {inicio: 0}
   pais = {inicio: None}

   heapq.heappush(fila, (heuristica, 0, inicio))

   while fila: 
     prioridade, custo_atual, estado_atual = heapq.heappop(fila)

     if custo_atual > custos.get(estado_atual, float('inf')):
        continue
     
     if estado_atual == objetivo:
      caminho = []
      atual = objetivo
      while pais[atual] is not None:
         nome, estado_pai = pais[atual]
         caminho.append(nome)
         atual = estado_pai
      caminho.reverse()
      return caminho
     
     for vizinho, nome in gerar_vizinhos(estado_atual, movimentos):
        novo_custo = custo_atual + 1

        if vizinho in custos and custos[vizinho] <= novo_custo: 
           continue
         
        custos[vizinho] = novo_custo
        pais[vizinho] = (nome, estado_atual)
        heapq.heappush(fila, (novo_custo + heuristica, novo_custo, vizinho))

   return None

# --- Inicializa o código ---
if __name__ == "__main__":
   selecionar_linguagem()
   exibir_banner()
   inicio, objetivo, movimentos, modelo = configurar_puzzle()
   
   t = textos[lang]

   print(t["calc_msg"])
   caminho = resolver(inicio, objetivo, movimentos, heuristica=0)

   if not caminho:
      print(t["no_solution"])
   else: 
      caminho_formatado = []
      # --- Formatação da saída ---
      if modelo == "A":
         for movimento, grupo in groupby(caminho):
            quantidade = len(list(grupo))
            direcao = "D" if movimento < 0 else "A"
            caminho_formatado.append(f"{quantidade}x {abs(movimento)}{direcao}")
         print(" -> ".join(caminho_formatado))
      
      elif modelo == "B":
         mov_contador = 0
         for movimento, grupo in groupby(caminho):
            quantidade = len(list(grupo))
            mov_contador += 1
            direcao = t["dir_b_right"] if movimento < 0 else t["dir_b_left"]
            num = abs(movimento) if movimento < 0 else movimento
            caminho_formatado.append(f"{mov_contador}. Plate {num} -> {direcao} x{quantidade}" if lang == "en" else f"{mov_contador}. Placa {num} -> {direcao} x{quantidade}")
         for passo in caminho_formatado:
            print(passo)
      
      elif modelo == "C":
         cursor = 1
         teclas = []
      
         for movimento in caminho:
            placa_alvo = abs(movimento)
      
            while cursor < placa_alvo:
               teclas.append("W")
               cursor += 1
            while cursor > placa_alvo:
               teclas.append("S")
               cursor -= 1
      
            direcao = "D" if movimento < 0 else "A"
            teclas.append(direcao)
         print(" -> ".join(teclas))

   input(t["press_enter"])


