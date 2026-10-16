⚡ Smart Grid: Precificação Dinâmica de Energia Renovável com Machine Learning

Este projeto simula o núcleo analítico de uma rede elétrica inteligente (Smart Grid). O objetivo é prever a geração de energia renovável (solar/eólica) e a procura da cidade nas próximas 48 horas, aplicando um algoritmo financeiro de precificação dinâmica: tarifas mais baratas quando há excesso de energia verde, e tarifas mais caras nos picos noturnos de consumo, incentivando a sustentabilidade e poupança de energia.

🚀 O Problema de Negócio
As redes elétricas tradicionais cobram um preço fixo pela energia, independentemente de ela estar a ser gerada por painéis solares sustentáveis ou por termoelétricas a carvão poluentes no horário de ponta. A precificação dinâmica resolve isso repassando a poupança da energia renovável para o cliente.

⚙️ A Solução (Arquitetura)
*   **Engenharia de Dados (Sprint 1):** Python (Pandas/Numpy) e SQLite. Geração de um dataset estocástico de 90 dias simulando radiação solar de dia, vento e consumo da cidade (picos matinais e noturnos).
*   **Machine Learning (Sprint 2):** Scikit-Learn (`RandomForestRegressor`). Em vez de classificação, usámos Séries Temporais (Regressão) para prever as próximas 48 horas de consumo e geração de forma independente. O modelo atingiu um erro médio de previsão inferior a 10 MW.
*   **Algoritmo Financeiro (Sprint 3):** Python. Lógica de cálculo do Déficit (Demanda - Geração) que decide a alteração da tarifa base (desconto de 40% para excedente verde, ou penalização de 50% para risco noturno).
*   **Business Intelligence (Sprint 4):** Power BI. Dashboard executivo que não resume os dados, exibindo o comportamento horário e as bandeiras tarifárias (Verde, Amarela, Vermelha) num layout de alto impacto visual.

🛠️ Como Executar
1. Instale os requisitos: `pip install pandas numpy scikit-learn sqlite3`
2. Execute `simulador_clima.py` e `criar_banco_energia.py` para construir o banco de dados base.
3. Execute `treinar_modelo_energia.py` para treinar a Inteligência Artificial e gerar a previsão de 48h.
4. Execute `motor_precos.py` para calcular o preço da energia com base no Déficit e exportar o CSV que alimenta o Power BI.