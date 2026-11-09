# Memória de cálculo (gerada por `calculo_energia.py`)

Todos os valores são **projeções condicionadas às premissas** de `dados/premissas.json`, não resultados garantidos.
Período de referência: **mês de 30 dias** e **ano de 365 dias**; horizonte de **10 anos**; **12 pontos de luz**.

## 1. Situação atual (A0)
- Potência por ponto = lâmpada 100 W + reator 15 W = **115 W**
- Tempo de funcionamento = 11 h 52 min = **11,8667 h/dia**
- E = (P × t) / 1000 = (115 × 11,8667) / 1000 = **1,3647 kWh/dia por ponto**
- 12 pontos × 30 dias = **491,3 kWh/mês** · **5.977 kWh/ano**
- Tarifa B4a Enel SP = TUSD 259,83 + TE 174,33 = 434,16 R$/MWh = **R$ 0,43416/kWh** (sem tributos, bandeira verde)
- Custo de energia = 5.977 × 0,43416 = **R$ 2.595,09/ano** (R$ 213,29/mês)
- Manutenção: troca de lâmpada a cada 4 anos × R$ 150 × 12 pontos = **R$ 450,00/ano**
- Emissões = 5.977 kWh × 0,0545 kgCO₂/kWh = **325,8 kgCO₂/ano**

## 2. Carga comum das alternativas (mesma necessidade)
- LED 60 W (9.000 lm) substitui a lâmpada de 10.600 lm: o LED é direcional e a luminária de sódio perde parte do fluxo no refletor, então o fluxo útil no chão é equivalente.
- Das 18h às 23h (5 h): 100%. Madrugada (6,87 h): 30% sem movimento, 100% com presença em 20% do tempo.
- Fator médio de madrugada = 0,20 × 1 + 0,80 × 0,30 = **0,44**
- Horas equivalentes a plena potência = 5 + 6,8667 × 0,44 = **8,0213 h**
- E_LED = (60 × 8,0213) / 1000 = **0,4813 kWh/dia**
- E_IoT = (0,5 W × 24 h) / 1000 = **0,0120 kWh/dia**
- **Total por ponto = 0,4933 kWh/dia** → 12 pontos: **177,6 kWh/mês**
- Tempo em modo eficiente (dimerizado) = 6,87 × 0,80 = **5,49 h/dia**

## 3. Alternativa 1 — LED + sensores na rede
- Consumo: **177,6 kWh/mês** (economia de **63,9%**)
- Investimento = 12 × (LED R$ 450 + sensores/IoT R$ 200 + instalação R$ 150) + medição R$ 1.500,00 = **R$ 11.100,00**
- A medição é necessária porque, sem medidor, a iluminação pública é faturada por estimativa (potência cadastrada × 11 h 52 min) e a economia da dimerização não chegaria à conta.
- Economia anual (energia + manutenção) = **R$ 1.987,05** → payback simples **5,6 anos**

## 4. Alternativa 2 — Luminárias solares autônomas (off-grid)
- Painel necessário = E / (HSP_pior_mês × PR) = 0,4933 / (3,8 × 0,75) = **173 Wp** → escolhido **200 Wp** (folga de 16% no pior mês)
- Bateria necessária = E × 2 noites / (DoD 0,90 × η 0,95) = **1,154 kWh** → escolhida **12,8 V × 100 Ah = 1,28 kWh** (autonomia real 2,2 noites; descarga diária ≈ 41%)
- Consumo da rede: **0 kWh/mês**; participação renovável **100%**
- Investimento por ponto = R$ 4.600,00 → **R$ 55.200,00** (+ reposição de baterias no ano 10: R$ 24.000,00)
- Economia anual = **R$ 2.325,09** → payback simples **23,7 anos** (maior que a vida da bateria)
- Alerta técnico: luminárias solares baratas anunciadas como "100 W" ou "150 W" costumam ter painel de ~35 W e bateria de ~125 Wh — não sustentam 60 W reais a noite toda. O dimensionamento acima é o que garante o serviço.

## 5. Alternativa 3 — LED + sensores + solar conectada à rede (on-grid)
- Geração = 1,6 kWp × HSP 4,9 × PR 0,75 × 365 = **2.146 kWh/ano** (consumo anual da A1 = 2.161 kWh)
- Como a luz é usada à noite, quase toda a geração é injetada e compensada depois (Lei 14.300).
- Valor do crédito = tarifa − 60% × Fio B = 0,43416 − 0,60 × 0,12992 = **R$ 0,35621/kWh**
- Custo de energia = 2.161 × 0,43416 − 2.146 × 0,35621 = **R$ 173,53/ano**
- Investimento = A1 R$ 11.100,00 + FV R$ 8.800,00 = **R$ 19.900,00** (o medidor da A1 passa a ser bidirecional)
- Economia anual = **R$ 2.601,55** → payback simples **7,6 anos**; participação renovável **99,3%** (balanço anual)

## 6. Emissões
- Fator médio do SIN 2024 = 0,0545 tCO₂/MWh (= kgCO₂/kWh). Sensibilidade com o fator de 2023 (0,0385): A0 emitiria 230,1 kgCO₂/ano.
- A matriz elétrica brasileira já é muito renovável; por isso as emissões evitadas são pequenas em valor absoluto. O ganho ambiental maior está no fim do mercúrio das lâmpadas de sódio e na energia que deixa de ser demandada.

## 7. Sensibilidade — bandeira vermelha patamar 1 (+R$ 0,04463/kWh)
- A0: custo de energia R$ 2.595,09/ano → R$ 2.861,85/ano
- A1: custo de energia R$ 938,03/ano → R$ 1.034,46/ano
- A2: custo de energia R$ 0,00/ano → R$ 0,00/ano
- A3: custo de energia R$ 173,53/ano → R$ 174,17/ano
