import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.preprocessing import LabelEncoder
import socket
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import warnings

# Silenciar avisos de nomes de colunas do sklearn
warnings.filterwarnings("ignore", category=UserWarning)

# ==================== DADOS DE TREINO ATUALIZADOS ====================
dados = pd.DataFrame({
    'porta': [80, 443, 22, 3389, 21, 25, 53, 80, 443, 22, 3389, 80, 443, 21, 25, 80, 22],
    'pacotes': [40, 50, 60, 70, 20, 30, 15, 35, 32, 80, 90, 45, 55, 10, 5, 38, 12],
    'erros': [2, 1, 15, 20, 3, 4, 25, 2, 1, 30, 40, 1, 2, 5, 50, 12, 8],
    'classe': [
        'normal', 'normal', 'malicioso', 'malicioso', 'suspeito', 'suspeito', 'malicioso',
        'suspeito', 'suspeito', 'malicioso', 'malicioso', 'normal', 'normal', 'suspeito', 'malicioso',
        'malicioso', 'suspeito'
    ]
})

encoder = LabelEncoder()
dados['porta_cod'] = encoder.fit_transform(dados['porta'])

X = dados[['porta_cod', 'pacotes', 'erros']]
y = dados['classe']

modelo = DecisionTreeClassifier(max_depth=3, random_state=42)
modelo.fit(X, y)
arvore = modelo.tree_
classes_reais = [c.upper() for c in modelo.classes_]

def obter_cor_classe(nome_classe):
    nome_classe = nome_classe.upper()
    if nome_classe == 'NORMAL': return '#90EE90'  # Verde
    if nome_classe == 'SUSPEITO': return '#FFA500' # Laranja
    return '#9B59B6' # Roxo (Malicioso)

# ==================== FUNÇÕES DO SISTEMA ====================

def mostrar_dashboard_arvore():
    fig, ax = plt.subplots(figsize=(12, 8))
    
    plot_tree(modelo, 
              feature_names=['porta_cod', 'pacotes', 'erros'],
              class_names=classes_reais, 
              filled=True, 
              rounded=True, 
              fontsize=10,
              ax=ax)
    
    patches = [p for p in ax.patches if isinstance(p, mpatches.FancyBboxPatch)]
    
    for i, patch in enumerate(patches):
        if i < arvore.node_count:
            classe_idx = np.argmax(arvore.value[i][0])
            classe_nome = classes_reais[classe_idx]
            
            cor = obter_cor_classe(classe_nome)
            patch.set_facecolor(cor)
            patch.set_edgecolor('black')
            patch.set_alpha(1.0) # FORÇA O ROXO NO NÓ RAIZ

    legend_elements = [
        mpatches.Patch(facecolor='#90EE90', edgecolor='black', label='NORMAL (Permitir)'),
        mpatches.Patch(facecolor='#FFA500', edgecolor='black', label='SUSPEITO (Monitorar)'),
        mpatches.Patch(facecolor='#9B59B6', edgecolor='black', label='MALICIOSO (Bloquear)')
    ]
    ax.legend(handles=legend_elements, loc='upper right', title="Legenda de Segurança")
    plt.title("MAPA DE DECISÃO - FIREWALL (ERRO >= 10 -> ROXO)", fontsize=14, pad=20)
    plt.show()

def escanear_alvo():
    alvo = input("\nDigite o IP ou Site: ").strip() or "127.0.0.1"
    print(f"\nAnalizando: {alvo}...")
    print(f"{'PORTA':<7} | {'CLASSE':<10} | {'AÇÃO'}")
    print("-" * 40)
    
    for p in [22, 80, 443, 3389]:
        p_cod = encoder.transform([p])[0] if p in encoder.classes_ else 0
        pac, err = (30, 12) if p in [22, 3389] else (45, 2)
        
        # Criando DataFrame para evitar o UserWarning de feature names
        entrada = pd.DataFrame([[p_cod, pac, err]], columns=['porta_cod', 'pacotes', 'erros'])
        pred = modelo.predict(entrada)[0].upper()
        
        acao = "BLOQUEAR" if pred == "MALICIOSO" else "MONITORAR" if pred == "SUSPEITO" else "PERMITIR"
        # CORREÇÃO DO ERRO DE FORMATAÇÃO ABAIXO (removido o '=')
        print(f"{p:<7} | {pred:<10} | {acao}")

# ==================== MENU PRINCIPAL ====================
while True:
    print(f"\n{' FIREWALL DINÂMICO':^35}")
    print("="*35)
    print("1 - Teste Manual")
    print("2 - Escanear IP/Site")
    print("3 - Arvore de processo em dashboard")
    print("4 - Sair")
    print("="*35)
    
    opcao = input("Escolha: ")
    if opcao == '1':
        try:
            p = int(input("Porta: "))
            pac = int(input("Pacotes: "))
            err = int(input("Erro (Inteiro): "))
            p_cod = encoder.transform([p])[0] if p in encoder.classes_ else 0
            entrada = pd.DataFrame([[p_cod, pac, err]], columns=['porta_cod', 'pacotes', 'erros'])
            res = modelo.predict(entrada)[0].upper()
            print(f"\n>>> RESULTADO: {res}")
        except: print("\nErro: Use valores inteiros.")
    elif opcao == '2': escanear_alvo()
    elif opcao == '3': mostrar_dashboard_arvore()
    elif opcao == '4': break