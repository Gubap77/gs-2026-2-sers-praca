# Global Solution 2026.2 · SERS · Praça Comunitária

Contribuição de **Soluções em Energias Renováveis e Sustentáveis (SERS)** ao desafio *Neighborhood Action Dashboard — CitizenTech*, FIAP, Ciência da Computação (1CC). Grupo 5.

## Ver funcionando

| O quê | Como |
|---|---|
| **Dashboard no navegador** | [gubap77.github.io/gs-2026-2-sers-praca](https://gubap77.github.io/gs-2026-2-sers-praca/) (abre direto, sem instalar nada) |
| **Cálculo rodando no GitHub** | aba [**Actions**](https://github.com/Gubap77/gs-2026-2-sers-praca/actions/workflows/calculos.yml) → última execução de *Cálculos de SERS* → a tabela de resultados aparece no resumo. Para rodar de novo: **Run workflow** |
| **Rodar o código no navegador** | [![Abrir no GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/Gubap77/gs-2026-2-sers-praca) e, no terminal: `cd sers && python calculos/calculo_energia.py` |
| **Rodar no computador** | **Code → Download ZIP**, abrir `sers/dashboard/index.html` (dashboard) e, com Python 3, rodar `python calculos/calculo_energia.py` dentro de `sers/` |

O cálculo usa só a biblioteca padrão do Python: não há nada para instalar.

## Onde está cada parte

Todo o trabalho de SERS está na pasta [`sers/`](sers/). Comece pelo [README da pasta](sers/README.md).

- Diagnóstico, análise, comparação, indicadores, limitações e referências: [`sers/README.md`](sers/README.md)
- Premissas e fontes dos dados: [`sers/dados/`](sers/dados/)
- Cálculos e memória de cálculo: [`sers/calculos/`](sers/calculos/)
- Diagrama de blocos: [`sers/diagrama/`](sers/diagrama/)
- Dashboard (código da integração): [`sers/dashboard/index.html`](sers/dashboard/index.html)
