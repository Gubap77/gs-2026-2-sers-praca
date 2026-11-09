# Fontes dos dados

Cada linha diz **o que foi usado** e **onde está**. Consulta feita em 09/11/2026. Os valores usados nos cálculos estão em `premissas.json`.

## Operação e tarifa

| Dado usado | Valor | Fonte |
|---|---|---|
| Tempo diário de iluminação pública para faturamento | 11 h 52 min | ANEEL, apresentação na Câmara dos Deputados — https://www2.camara.leg.br/atividade-legislativa/comissoes/comissoes-permanentes/cdu/apresentacoes-em-eventos/audiencias-publicas-2012-1/situacao-dos-municipios-em-relacao-a-responsabilidade-pelas-redes-de-iluminacao-publica/apresentacao-aneel/view |
| Tarifa B4a Enel SP (TUSD + TE, bandeira verde, sem tributos) | 259,83 + 174,33 R$/MWh | Enel SP, REH ANEEL nº 3.596/2026, válida a partir de 04/07/2026 — https://www.enel.com.br/pt-saopaulo/Para_Voce/tarifa-energia-eletrica.html e https://www.enel.com.br/content/dam/enel-br/megamenu/para-voc%C3%AA/REH%203596.2026%20Enel%20SP.pdf |
| Adicional da bandeira vermelha patamar 1 | R$ 4,463 / 100 kWh | O Setor Elétrico — https://www.osetoreletrico.com.br/?p=164719 |
| Faturamento por estimativa sem medição; dimerização e telegestão | — | O Setor Elétrico — https://www.osetoreletrico.com.br/dimerizacao-na-iluminacao-publica-desafios-e-alternativas/ ; ConJur — https://www.conjur.com.br/?p=471888 |

## Equipamentos

| Dado usado | Valor | Fonte |
|---|---|---|
| Lâmpada de vapor de sódio 100 W: fluxo, vida, mercúrio | 10.600 lm · 29.000 h · 16,3 mg Hg | Philips/Signify MASTER SON-T PIA Plus 100W — https://www.assets.signify.com/is/content/PhilipsLighting/fp928151709230-pss-pt_pt |
| Vida útil prática da lâmpada de sódio | 4 anos com ~11 h/dia | LEDVANCE NAV-T 100 W SUPER 4Y — https://www.ledvance.com/pt/product-datasheet/7315/88921 |
| Luminária LED pública 60 W: fluxo | 9.000 lm | ORSE 13065 — https://orcamentor.com/orse/materiais/ORSE-6827/ |
| Luminária LED pública 60 W: vida útil | 70.000 h | ORSE 13201 — https://orcamentor.com/orse/composicoes/ORSE-13201/ |
| Preço de luminária pública LED com Inmetro/Procel | R$ 415,01 (Ourolux 100 W) a R$ 525,40 (Demape 100 W) | https://www.lojaeletrica.com.br/iluminacao/iluminacao-publica/luminarias-publicas.html ; https://demape.com.br/categoria-produto/produtos/luminaria-publica-led/ |
| Parque de iluminação pública no Brasil (LED × HID) | até 19,6% LED e 59% HID | Inmetro, AIR de luminárias para iluminação pública viária — https://www.gov.br/inmetro/pt-br/assuntos/regulamentacao/analise-de-impacto-regulatorio/realizadas/2025/luminarias-para-iluminacao-publica-viaria/sei_inmetro-2304864-relatorio-final.pdf |
| Luminária solar "150 W" de varejo: painel e bateria reais | painel 35 W · LiFePO4 3,2 V 39 Ah | Arco Íris LED — https://www.arcoirisled.com.br/luminaria-publica-150w-solar-c-controle-80338 |

## Solar

| Dado usado | Valor | Fonte |
|---|---|---|
| HSP de São Paulo no pior mês (junho) | 3,8 kWh/m²·dia | Energia Solar Explicada (dados CRESESB/INPE SunData) — https://energiasolarexplicada.com.br/blog/quanto-gera-uma-placa-solar-por-dia/ |
| HSP média anual em São Paulo, plano inclinado ~23° | 4,9 kWh/m²·dia | Solar de Casa (dados CRESESB/SunData) — https://www.solardecasa.com.br/blog/residencial/orientacao-inclinacao-telhado-solar-quanto-gera-mais-2026 |
| Ferramenta oficial para confirmar a irradiação | — | CRESESB SunData — https://cresesb.cepel.br/index.php?section=sundata |
| Taxa de desempenho (performance ratio) | 0,75 | Zilles, R., IEE/USP, IEE0004 Aula 11 — https://edisciplinas.usp.br/pluginfile.php/6848059/mod_resource/content/5/undefined/Curso_IEE0004_Aula_11_2022_1.pdf |
| Preço de bateria LiFePO4 12,8 V 100 Ah | R$ 1.063,45 a R$ 2.883,44 | Magazine Luiza — https://m.magazineluiza.com.br/busca/bateria+100ah |
| Preço de módulo fotovoltaico | R$ 389,62 (155 Wp); R$ 3.815 (4 × 450 W) | Magazine Luiza — https://m.magazineluiza.com.br/busca/kit+solar+microinversor ; Mercado Livre — https://lista.mercadolivre.com.br/placas-para-energia-solar-avulsa |
| Preço de controlador MPPT 20 A | US$ 39 a US$ 88 | PowMr — https://powmr.com/es/products/mppt-solar-charge-controller-20amp-12v-24v ; Renogy — https://www.renogy.com/es/rover-li-20-amp-mppt-solar-charge-controller/ |
| Custo de sistema fotovoltaico instalado em SP | R$ 14.000–17.000 para 3,5 kW | SurgePV — https://www.surgepv.com/pt/solar-compliance/brazil/estado/sao-paulo |
| Fio B não compensado em 2026 (e cronograma) | 60% (75% em 2027, 90% em 2028) | Canal Solar, Lei 14.300/2022 art. 27 — https://canalsolar.com.br/consumidores-60-do-fio-b-2026/ |

## Emissões

| Dado usado | Valor | Fonte |
|---|---|---|
| Fator médio de emissão do SIN 2024 | 0,0545 tCO₂/MWh | Bradesco, Inventário de GEE 2024 (cita o fator do SIN) — https://assets.bradesco/content/dam/portal-bradesco/assets/classic/pdf/sustentabilidade/bradesco-inventario-de-emissoes-GEE-2024.pdf ; planilhas oficiais no MCTI/SIRENE — https://www.gov.br/mcti/pt-br/acompanhe-o-mcti/sirene/dados-e-ferramentas/fatores-de-emissao |
| Fator médio de emissão do SIN 2023 (sensibilidade) | 0,0385 tCO₂/MWh | MCTI — https://www.gov.br/mcti/pt-br/acompanhe-o-mcti/noticias/2024/02/fator-de-emissao-de-co2-na-geracao-de-energia-eletrica-no-brasil-em-2023-e-o-menor-em-12-anos |

## Estimativas da equipe (sem fonte direta)

Perda do reator (15 W), custo de troca de lâmpada (R$ 150), módulo IoT (0,5 W; R$ 200), instalação (R$ 150 a R$ 600 por ponto), estrutura e cabos (R$ 400), manutenção anual, medidor (R$ 1.500), Fio B = 50% da TUSD e perfil de presença. Cada uma tem a justificativa ao lado do valor em `premissas.json`.
