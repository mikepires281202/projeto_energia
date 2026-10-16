import pandas as pd
import sqlite3
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
import numpy as np

print("A iniciar o treino da Inteligência Artificial (Séries Temporais)...")

# 1. Conectar ao banco de dados e ler o histórico
conexao = sqlite3.connect('banco_energia.db')
df = pd.read_sql('SELECT * FROM telemetria_horaria', conexao)

# Converter a coluna de texto para formato de data/hora oficial do Pandas
df['data_hora'] = pd.to_datetime(df['data_hora'])

# 2. Engenharia de Features (Extrair o "Tempo" para a IA entender os padrões)
df['hora'] = df['data_hora'].dt.hour
df['dia_semana'] = df['data_hora'].dt.dayofweek

# 3. Preparar as variáveis
# O que vamos usar para prever (Features)
X = df[['hora', 'dia_semana', 'radiacao_solar', 'velocidade_vento']]

# O que queremos prever (Targets)
y_demanda = df['demanda_mw']
y_geracao = df['geracao_renovavel_mw']

# Separar Treino (80%) e Teste (20%)
# Em Séries Temporais, NUNCA baralhamos os dados (shuffle=False), para a IA aprender a sequência do tempo
X_treino, X_teste, y_dem_treino, y_dem_teste = train_test_split(X, y_demanda, test_size=0.2, shuffle=False)
_, _, y_ger_treino, y_ger_teste = train_test_split(X, y_geracao, test_size=0.2, shuffle=False)

# 4. Treinar os Modelos (Usamos Regressor para prever valores numéricos contínuos)
print("A treinar a rede para prever a Demanda da cidade...")
modelo_demanda = RandomForestRegressor(n_estimators=100, random_state=42)
modelo_demanda.fit(X_treino, y_dem_treino)

print("A treinar a rede para prever a Geração Renovável...")
modelo_geracao = RandomForestRegressor(n_estimators=100, random_state=42)
modelo_geracao.fit(X_treino, y_ger_treino)

# 5. Avaliar o Modelo
prev_demanda = modelo_demanda.predict(X_teste)
erro_demanda = mean_absolute_error(y_dem_teste, prev_demanda)

prev_geracao = modelo_geracao.predict(X_teste)
erro_geracao = mean_absolute_error(y_ger_teste, prev_geracao)

print(f"\n--- Resultados da Precisão ---")
print(f"Erro Médio na previsão de Demanda: {erro_demanda:.2f} MW")
print(f"Erro Médio na previsão de Geração: {erro_geracao:.2f} MW")

# 6. Simular o futuro: Prever as próximas 48 horas da Smart Grid
print("\nA processar previsões para as próximas 48 horas...")
ultima_data = df['data_hora'].max()
futuro_datas = pd.date_range(start=ultima_data + pd.Timedelta(hours=1), periods=48, freq="h")
df_futuro = pd.DataFrame({'data_hora': futuro_datas})
df_futuro['hora'] = df_futuro['data_hora'].dt.hour
df_futuro['dia_semana'] = df_futuro['data_hora'].dt.dayofweek

# Simular a previsão meteorológica de amanhã e depois
df_futuro['radiacao_solar'] = np.where(
    (df_futuro['hora'] > 6) & (df_futuro['hora'] < 18),
    np.sin((df_futuro['hora'] - 6) * (np.pi / 12)) * 800,
    0
).clip(0)
df_futuro['velocidade_vento'] = 6.5 # Vento estável simulado

# Fazer as previsões reais usando a IA treinada
X_futuro = df_futuro[['hora', 'dia_semana', 'radiacao_solar', 'velocidade_vento']]
df_futuro['previsao_demanda_mw'] = modelo_demanda.predict(X_futuro).round(2)
df_futuro['previsao_geracao_mw'] = modelo_geracao.predict(X_futuro).round(2)

# Guardar as previsões no SQLite
df_futuro.to_sql('previsao_48h', conexao, if_exists='replace', index=False)
conexao.close()

print("Sucesso! Tabela 'previsao_48h' criada no banco de dados.")