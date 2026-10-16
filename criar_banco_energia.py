import pandas as pd
import sqlite3

print("A iniciar a transferência de telemetria para o SQLite...")

# 1. Ler o ficheiro CSV gerado pelo simulador
df = pd.read_csv('historico_grid.csv')

# 2. Criar a ligação à base de dados (o SQLite cria o ficheiro automaticamente)
conexao = sqlite3.connect('banco_energia.db')

# 3. Guardar os dados numa tabela chamada 'telemetria_horaria'
df.to_sql('telemetria_horaria', conexao, if_exists='replace', index=False)

# 4. Fechar a ligação por segurança
conexao.close()

print("Sucesso! A base de dados 'banco_energia.db' foi criada e populada.")