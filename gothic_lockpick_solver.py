import heapq
import os
from itertools import groupby

# --- Banner ---
def exibir_banner():
    # Limpa a tela ao iniciar (compatível com Windows e Linux/macOS)
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Cores ANSI para o terminal
    CYAN = "\033[96m"
    AMARELO = "\033[93m"
    VERDE = "\033[92m"
    RESET = "\033[0m"
    
    print(CYAN + "=" * 115 + RESET)
    print(AMARELO + r"""
     _                _     ___  ___          _                 _                 _____       _                
    | |              | |    |  \/  |         | |               (_)               /  ___|     | |               
    | |     ___   ___| | __ | .  . | ___  ___| |__   __ _ _ __  _ ___ _ __ ___   \ `--.  ___ | |_   _____ _ __ 
    | |    / _ \ / __| |/ / | |\/| |/ _ \/ __| '_ \ / _` | '_ \| / __| '_ ` _ \   `--. \/ _ \| \ \ / / _ \ '__|
    | |___| (_) | (__|   <  | |  | |  __/ (__| | | | (_| | | | | \__ \ | | | | | /\__/ / (_) | |\ V /  __/ |   
    \_____/\___/ \___|_|\_\ \_|  |_/\___|\___|_| |_|\__,_|_| |_|_|___/_| |_| |_| \____/ \___/|_| \_/ \___|_|                                                                                                 
    """ + RESET)
    print(VERDE + "     Dijkstra Search Algorithm ".center(115) + RESET)
    print(CYAN + "     Desenvolvido por: Francisco de Assis Junior".center(115) + RESET)
    print(CYAN + "=" * 115 + RESET + "\n")

#Variáveis 
heuristica = 0
modelo = "A"
objetivo = None
tamanho = 0
inicio = None
movimentos_originais = {}

# --- Montar Puzzle ---
#Tamanho
def pegar_tamanho():
   while True:
      entrada = input("Informe a quantidade de placas [4-7]: ")

      try:
         tamanho_novo = int(entrada)
      except ValueError:
         print("* ERRO! Digite apenas números inteiros válidos!\n")
         continue
   
      if not 4 <= tamanho_novo <= 7:
         print("* ERRO! Tamanho deve ser entre 4 e 7!\n")
         continue
      
      print("-" * 55 + "\n")
      return tamanho_novo

#Posição inicial
def pegar_estado_inicial(tamanho):
   while True:
      novo_inicio = []
      erro = False
      entrada = input(f"Informe o estado inicial dos {tamanho} pinos (ex: 6 2 4 5): ").replace(",", " ")
      entrada = entrada.split()
   
      if len(entrada) != tamanho:
         print(f"\n* ERRO! Quantidade esperada de números: {tamanho}. Quantidade digitada: {len(entrada)}.")
         continue
   
      for e in entrada:
         try:
            pino = int(e)
         except ValueError:
            print("\n* ERRO! Caractere inválido detectado. Digite apenas números inteiros.")
            erro = True
            break
   
         if not 1 <= pino <=7:
            print("\n* ERRO! O os pinos devem estar entre [1-7].")
            erro = True
            break
   
         novo_inicio.append(pino)  
   
      if erro:
         continue
      
      print("-" * 55 + "\n")
      return tuple(novo_inicio)
      
#Movimentos
def pegar_movimentos(tamanho, movimentos_originais=None, placa_alvo=None):
   if movimentos_originais is None:
      movimentos_originais = {}

   if placa_alvo is None:
      placas_para_configurar = range(1, tamanho + 1)
   else: 
      placas_para_configurar = [placa_alvo]

   for placa in placas_para_configurar:
      while True:
         entrada = input(f"Digite o movimento realizado pela {placa}ª placa (ex: 0 1 0 0 -1): ").replace(",", " ")
         placas = entrada.split()
         novo_movimento = []
   
         if len(placas) != tamanho:
            print(f"\n* ERRO! Quantidade esperada de números: {tamanho}. Quantidade digitada: {len(placas)}.")
            continue
   
         for i, e in enumerate(placas):
            try:
               mov = int(e)
            except ValueError:
               print("\n* ERRO! Caractere inválido. Digite apenas -1, 0 ou 1.")
               break

            if (i + 1) == placa and mov != 1:
               print("\n* ERRO! A placa atual deve ser obrigatóriamente 1")
               break

            if mov not in (-1, 0, 1):
               print("\n* ERRO! Os valores devem ser estritamente -1, 0 ou 1.")
               break
   
            novo_movimento.append(mov)
         else: 
            movimentos_originais[placa] = tuple(novo_movimento)
            break
   print("-" * 55 + "\n")
   return movimentos_originais

#Estilo
def pegar_estilo():
   print("\n" + "=" * 55)
   print("       ESCOLHA O FORMATO DA SOLUÇÃO")
   print("=" * 55)
   print("[A] Formato Rápido (Ex: 3x -> Placa 2/A)")
   print("[B] Formato Detalhado (Ex: Movimento 1. Placa 4 -> Esquerda x3)")
   print("[C] Formato Teclas/Macro (Ex: W -> W -> D -> S -> A )")
   print("-" * 55)
   
   while True:
      estilo = input("Digite a opção desejada (A, B ou C): ").strip().upper()
      if estilo in ("A", "B", "C"):
            return estilo
      print("\n* ERRO: Opção inválida! Por favor, digite apenas 'A', 'B' ou 'C'.\n")

#Resumo
def exibir_resumo(tamanho, inicio, movimentos_originais, modelo):
   print("\n" + "=" * 55)
   print("       RESUMO")
   print(f"[0]Tamanho: {tamanho}")
   print(f"[1]Estado inicial: {inicio}")
   print(f"[2]Movimentos:")
   for placa, mov in movimentos_originais.items():
      print(f"      Placa {placa} -> {list(mov)}")
   print(f"[3]Estilo: {modelo}")
   print("=" * 55)


#Configuração inicial
def configurar_puzzle():
   tamanho = pegar_tamanho()
   objetivo = (4,) * tamanho
   inicio = pegar_estado_inicial(tamanho)
   movimentos_originais = pegar_movimentos(tamanho)
   modelo = pegar_estilo()
   
   #Gerar movimentos inversos
   movimentos_inversos = {-k: tuple(-x for x in v) for k, v in movimentos_originais.items()}
   movimentos = movimentos_originais| movimentos_inversos

   #Resumo geral
   exibir_resumo(tamanho, inicio, movimentos_originais, modelo)
   
   #Modificar algo
   while True:
      alterar = input("Deseja alterar algo [S/N]? ").strip().upper()
   
      if alterar not in ("S", "N"):
         print("\n* ERRO! Digite apenas S ou N.")
         continue
   
      if alterar == "N":
         break
      else: 
         opcao = input("Qual você deseja alterar [0-3]? ").strip()
         
         if opcao == "0":
            print("\nAlterar o tamanho vai reiniciar a configuração.")
            tamanho = pegar_tamanho()
            objetivo = (4,) * tamanho
            inicio = pegar_estado_inicial(tamanho)
            movimentos_originais = pegar_movimentos(tamanho)
            
         elif opcao == "1":
            print("\nRedefinindo o estado inicial...")
            inicio = pegar_estado_inicial(tamanho)
               
         elif opcao == "2":
            try:
               placa_alvo = int(input(f"Qual placa deseja alterar o movimento [1-{tamanho}]? "))
            except ValueError:
               print("\n* ERRO! Digite um número inteiro.")
               continue
            if placa_alvo not in range(1, tamanho + 1):
               print("\n* ERRO! Placa inexistente.")
               continue

            movimentos_originais = pegar_movimentos(tamanho, movimentos_originais, placa_alvo)
         
         elif opcao == "3":
            print("\nRedefinindo o estilo de exibição...")
            modelo = pegar_estilo()
         else:
            print("\n* ERRO! Opção inválida. Escolha entre 0 e 3.")
         
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
   exibir_banner()
   inicio, objetivo, movimentos, modelo = configurar_puzzle()

   print("\nCalculando a solução...")
   caminho = resolver(inicio, objetivo, movimentos, heuristica=0)

   if not caminho:
      print("\n Não foi possível encontrar uma solução para este estado!")
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
         direcao = "direita" if movimento < 0 else "esquerda"
         num = abs(movimento) if movimento < 0 else movimento
         caminho_formatado.append(f"{mov_contador}. Placa {num} -> {direcao} x{quantidade}")
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

input("\nPressione ENTER para fechar...")


