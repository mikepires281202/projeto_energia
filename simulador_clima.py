import pandas as pd
import numpy as np

print("A iniciar os sensores da Smart Grid (simulação de 90 dias)...")

# 1. Gerar 2160 horas (90 dias) de dados sequenciais
datas = pd.date_range(start="2026-01-01", periods=2160, freq="h")
df = pd.DataFrame({"data_hora": datas})

# Extrair a hora do dia para criar os padrões naturais
df['hora_do_dia'] = df['data_hora'].dt.hour

# 2. Simular a Natureza
# Radiação Solar: Forte entre as 7h e 18h, zero à noite
df['radiacao_solar'] = np.where(
    (df['hora_do_dia'] > 6) & (df['hora_do_dia'] < 18),
    np.sin((df['hora_do_dia'] - 6) * (np.pi / 12)) * 800 + np.random.normal(0, 30, len(df)),
    0
).clip(0) # <-- SOLUÇÃO: Apenas o número 0, sem palavras.

# Vento: Constante com rajadas aleatórias
df['velocidade_vento'] = np.random.normal(6, 2, len(df)).clip(0) # <-- AQUI TAMBÉM

# 3. Simular a Cidade (Consumo vs Geração)
# Consumo dispara de manhã (preparar para o trabalho) e à noite (chuveiros/luzes)
df['demanda_mw'] = 100 + np.where(
    ((df['hora_do_dia'] >= 18) & (df['hora_do_dia'] <= 22)) | ((df['hora_do_dia'] >= 7) & (df['hora_do_dia'] <= 9)),
    80, # Pico de consumo
    20  # Consumo normal
) + np.random.normal(0, 10, len(df))

# Geração de Energia: Painéis solares + Turbinas eólicas
df['geracao_renovavel_mw'] = (df['radiacao_solar'] * 0.15) + (df['velocidade_vento'] * 8) + np.random.normal(0, 5, len(df))
df['geracao_renovavel_mw'] = df['geracao_renovavel_mw'].clip(0) # <-- E AQUI TAMBÉM

# Limpar coluna auxiliar e guardar
df.drop(columns=['hora_do_dia'], inplace=True)
df.to_csv('historico_grid.csv', index=False)

print(f"Sucesso! Gerados {len(df)} registos de telemetria no ficheiro 'historico_grid.csv'.")