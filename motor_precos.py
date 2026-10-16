import pandas as pd
import sqlite3

print("A acionar o Motor Financeiro: Calculando Preço Dinâmico (Tarifas)...")

# 1. Ligar ao banco e puxar as previsões feitas pela IA
conexao = sqlite3.connect('banco_energia.db')
df_previsao = pd.read_sql('SELECT * FROM previsao_48h', conexao)

# 2. Calcular o Déficit de Energia
# Positivo = Falta energia verde (mau, preços sobem). Negativo = Sobra energia verde (bom, preços descem)
df_previsao['deficit_mw'] = (df_previsao['previsao_demanda_mw'] - df_previsao['previsao_geracao_mw']).round(2)

# 3. O Algoritmo Financeiro de Precificação
# Tarifa Base da cidade: 0.50$ por kWh. O preço sobe ou desce dependendo da sobra ou falta de energia renovável
def calcular_tarifa(deficit):
    preco_base = 0.50 
    
    if deficit < 0:
        # Excedente de energia renovável (Vento/Sol fortíssimos) -> Baratear muito a energia
        fator = 0.60  # Desconto de 40% (Tarifa Verde)
        bandeira = 'Verde (Barato - Sobra)'
    elif deficit < 50:
        # Faltou um pouco, mas a rede aguenta
        fator = 1.0   # Preço normal (Tarifa Amarela)
        bandeira = 'Amarela (Normal)'
    else:
        # Crise de geração (Noite, sem vento, todos a consumir) -> Encarecer a energia para evitar apagão
        fator = 1.5   # Aumento de 50% (Tarifa Vermelha)
        bandeira = 'Vermelha (Caro - Risco)'
        
    preco_final = preco_base * fator
    return pd.Series([round(preco_final, 2), bandeira])

# Aplicar o algoritmo a todas as 48 horas futuras
df_previsao[['preco_kwh_$', 'bandeira_tarifaria']] = df_previsao['deficit_mw'].apply(calcular_tarifa)

# 4. Exportar a tabela final para o Dashboard do Power BI
df_previsao.to_csv('tabela_tarifas_bi.csv', index=False)
conexao.close()

print(f"Sucesso! Gerada a tabela 'tabela_tarifas_bi.csv' com o preço da energia hora a hora.")