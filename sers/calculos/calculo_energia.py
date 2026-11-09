"""
GS 2026.2 - SERS - Neighborhood Action Dashboard (CitizenTech)
Estudo energetico da iluminacao de uma praca comunitaria.

Le dados/premissas.json, calcula consumo, custos, emissoes e indicadores
das quatro situacoes (atual + 3 alternativas) e gera:
  - calculos/resultados.json          -> todos os numeros calculados
  - calculos/memoria_de_calculo.md    -> passo a passo das contas
  - dados/monitoramento_simulado.csv  -> 30 noites de monitoramento SIMULADO
  - dashboard/dados.js                -> dados consumidos pelo dashboard
e, em seguida, chama video/gerar_roteiro.py, que preenche as falas do video
com estes mesmos numeros (dashboard/roteiro.js e video/roteiro_video.md).

Uso:  python calculos/calculo_energia.py   (a partir da pasta sers/)
Sem dependencias externas (so biblioteca padrao do Python 3).
"""

import csv
import json
import random
from datetime import date, timedelta
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
P = json.loads((BASE / "dados" / "premissas.json").read_text(encoding="utf-8"))


def v(grupo, chave):
    """Valor numerico de uma premissa."""
    return P[grupo][chave]["valor"]


def energia_kwh(potencia_w, horas):
    """Formula do enunciado: E = (P x t) / 1000  ->  kWh."""
    return potencia_w * horas / 1000


# ---------------------------------------------------------------- premissas
N = v("praca", "pontos_de_luz")
T_NOITE = v("operacao", "horas_noite")
DIAS_MES = v("operacao", "dias_mes")
DIAS_ANO = v("operacao", "dias_ano")
ANOS = v("operacao", "horizonte_anos")
T_INTENSO = v("operacao", "horas_uso_intenso")
T_MADRUGADA = T_NOITE - T_INTENSO
DIM = v("operacao", "nivel_dimerizado")
PRES = v("operacao", "fracao_tempo_com_presenca_madrugada")

TARIFA = (v("tarifa", "tusd_b4a") + v("tarifa", "te_b4a")) / 1000          # R$/kWh
TARIFA_VERMELHA = TARIFA + v("tarifa", "adicional_bandeira_vermelha_1") / 1000
FE = v("emissoes", "fator_emissao_sin")                                     # tCO2/MWh = kgCO2/kWh
FE_2023 = v("emissoes", "fator_emissao_sin_2023")

memoria = []  # linhas da memoria de calculo


def m(texto=""):
    memoria.append(texto)


# ---------------------------------------------------------------- situacao atual (A0)
p_sodio = v("situacao_atual", "potencia_lampada_vapor_sodio") + v("situacao_atual", "perda_reator")
e_a0_ponto_dia = energia_kwh(p_sodio, T_NOITE)

# ---------------------------------------------------------------- carga comum das alternativas
# Mesma necessidade: 12 pontos LED 60 W com o mesmo perfil de uso (presenca + dimerizacao).
p_led = v("luminaria_led", "potencia")
fator_madrugada = PRES * 1.0 + (1 - PRES) * DIM
horas_equivalentes = T_INTENSO + T_MADRUGADA * fator_madrugada
e_led_ponto_dia = energia_kwh(p_led, horas_equivalentes)
e_iot_ponto_dia = energia_kwh(v("monitoramento", "consumo_modulo_iot"), 24)
e_alt_ponto_dia = e_led_ponto_dia + e_iot_ponto_dia
horas_dimerizado = T_MADRUGADA * (1 - PRES)

# ---------------------------------------------------------------- A2: dimensionamento solar off-grid
A2 = P["alt2_solar_offgrid"]
pr = A2["performance_ratio"]["valor"]
hsp_min = A2["hsp_pior_mes"]["valor"]
p_fv_necessaria_wp = e_alt_ponto_dia / (hsp_min * pr) * 1000
p_fv_escolhida = A2["painel_escolhido"]["valor"]
geracao_pior_dia_wh = p_fv_escolhida * hsp_min * pr
margem_fv = geracao_pior_dia_wh / (e_alt_ponto_dia * 1000) - 1
bat_necessaria_kwh = e_alt_ponto_dia * A2["dias_autonomia"]["valor"] / (
    A2["profundidade_descarga"]["valor"] * A2["eficiencia_bateria"]["valor"])
bat_escolhida = A2["bateria_escolhida_kwh"]["valor"]
autonomia_real = bat_escolhida * A2["profundidade_descarga"]["valor"] * A2["eficiencia_bateria"]["valor"] / e_alt_ponto_dia
descarga_diaria = e_alt_ponto_dia / A2["eficiencia_bateria"]["valor"] / bat_escolhida

# ---------------------------------------------------------------- A3: FV on-grid na praca
A3 = P["alt3_led_rede_fv_ongrid"]
kwp = A3["potencia_fv_kwp"]["valor"]
hsp_media = A3["hsp_media_anual"]["valor"]
geracao_ano_a3 = kwp * hsp_media * pr * DIAS_ANO
fio_b = v("tarifa", "tusd_b4a") / 1000 * A3["fracao_tusd_fio_b"]["valor"]
valor_credito = TARIFA - fio_b * A3["fio_b_nao_compensado_2026"]["valor"]   # R$/kWh compensado


# ---------------------------------------------------------------- consolidacao
def resumo(nome, codigo, consumo_rede_dia_ponto, renovavel_kwh_ano, capex, om_ano,
           reposicoes, custo_energia_ano, descricao, fonte_energia):
    consumo_mes = consumo_rede_dia_ponto * N * DIAS_MES
    consumo_ano = consumo_rede_dia_ponto * N * DIAS_ANO
    return {
        "codigo": codigo, "nome": nome, "descricao": descricao, "fonte_energia": fonte_energia,
        "consumo_rede_kwh_mes": consumo_mes, "consumo_rede_kwh_ano": consumo_ano,
        "renovavel_kwh_ano": renovavel_kwh_ano,
        "custo_energia_ano": custo_energia_ano, "custo_energia_mes": custo_energia_ano * DIAS_MES / DIAS_ANO,
        "capex": capex, "om_ano": om_ano, "reposicoes_horizonte": reposicoes,
    }


a0_om = N * v("situacao_atual", "custo_troca_lampada") / v("situacao_atual", "troca_lampada_a_cada_anos")
a0 = resumo("Situação atual", "A0", e_a0_ponto_dia, 0, 0, a0_om, 0,
            e_a0_ponto_dia * N * DIAS_ANO * TARIFA,
            "12 lâmpadas de vapor de sódio 100 W com reator, acesas a 100% a noite toda",
            "Rede elétrica (SIN)")

capex_a1_ponto = (v("luminaria_led", "preco") + v("monitoramento", "preco_sensor_iot")
                  + v("alt1_led_rede", "instalacao"))
capex_a1 = capex_a1_ponto * N + v("alt1_led_rede", "custo_medicao")
a1 = resumo("LED + sensores na rede", "A1", e_alt_ponto_dia, 0, capex_a1,
            N * v("alt1_led_rede", "om_anual"), 0, e_alt_ponto_dia * N * DIAS_ANO * TARIFA,
            "Troca por LED 60 W com sensor de presença, dimerização e monitoramento IoT",
            "Rede elétrica (SIN)")

capex_a2_ponto = (v("luminaria_led", "preco") + v("monitoramento", "preco_sensor_iot")
                  + A2["preco_painel_por_wp"]["valor"] * p_fv_escolhida + A2["preco_bateria"]["valor"]
                  + A2["preco_controlador_mppt"]["valor"] + A2["preco_estrutura_cabos"]["valor"]
                  + A2["instalacao"]["valor"])
reposicao_a2 = N * A2["preco_bateria"]["valor"] if A2["reposicao_bateria_ano"]["valor"] <= ANOS else 0
a2 = resumo("Luminárias solares autônomas", "A2", 0, e_alt_ponto_dia * N * DIAS_ANO,
            capex_a2_ponto * N, N * A2["om_anual"]["valor"], reposicao_a2, 0,
            "Mesma luminária LED + sensores, alimentada por painel de 200 Wp e bateria LiFePO4 em cada poste",
            "Solar fotovoltaica (off-grid)")

consumo_a3_ano = e_alt_ponto_dia * N * DIAS_ANO
custo_a3_ano = consumo_a3_ano * TARIFA - min(geracao_ano_a3, consumo_a3_ano) * valor_credito
capex_a3 = capex_a1 + kwp * 1000 * A3["custo_fv_por_wp_instalado"]["valor"]
a3 = resumo("LED + sensores + solar na rede", "A3", e_alt_ponto_dia, min(geracao_ano_a3, consumo_a3_ano),
            capex_a3, N * v("alt1_led_rede", "om_anual") + A3["om_anual_fv"]["valor"], 0, custo_a3_ano,
            "Alternativa 1 + 1,6 kWp de painéis no quiosque da praça, compensando o consumo pela rede (Lei 14.300)",
            "Rede + solar fotovoltaica (on-grid)")
a3["geracao_fv_kwh_ano"] = geracao_ano_a3

cenarios = [a0, a1, a2, a3]
for c in cenarios:
    consumo_total_ano = c["consumo_rede_kwh_ano"] if c["codigo"] != "A2" else e_alt_ponto_dia * N * DIAS_ANO
    c["energia_demandada_kwh_ano"] = consumo_total_ano
    c["energia_demandada_kwh_mes"] = consumo_total_ano * DIAS_MES / DIAS_ANO
    c["renovavel_kwh_mes"] = c["renovavel_kwh_ano"] * DIAS_MES / DIAS_ANO
    c["participacao_renovavel_pct"] = 100 * c["renovavel_kwh_ano"] / consumo_total_ano if consumo_total_ano else 0
    # energia que ainda vem do SIN em balanco anual (para emissoes)
    rede_liquida = max(c["energia_demandada_kwh_ano"] - c["renovavel_kwh_ano"], 0)
    c["emissoes_kgco2_ano"] = rede_liquida * FE
    c["economia_kwh_mes"] = a0["consumo_rede_kwh_mes"] - c["consumo_rede_kwh_mes"]
    c["economia_rede_pct"] = 100 * c["economia_kwh_mes"] / a0["consumo_rede_kwh_mes"]
    c["reducao_demanda_pct"] = 100 * (1 - c["energia_demandada_kwh_ano"] / a0["energia_demandada_kwh_ano"])
    c["emissoes_evitadas_kgco2_ano"] = a0["emissoes_kgco2_ano"] - c["emissoes_kgco2_ano"]
    c["economia_rs_ano"] = (a0["custo_energia_ano"] + a0["om_ano"]) - (c["custo_energia_ano"] + c["om_ano"])
    c["economia_rs_mes"] = c["economia_rs_ano"] * DIAS_MES / DIAS_ANO
    c["payback_anos"] = c["capex"] / c["economia_rs_ano"] if c["economia_rs_ano"] > 0 and c["capex"] else None
    c["custo_total_10_anos"] = c["capex"] + ANOS * (c["custo_energia_ano"] + c["om_ano"]) + c["reposicoes_horizonte"]
    c["horas_dimerizado_dia"] = 0 if c["codigo"] == "A0" else horas_dimerizado
    c["custo_energia_ano_bandeira_vermelha"] = (
        c["custo_energia_ano"] * TARIFA_VERMELHA / TARIFA if c["codigo"] != "A3"
        else consumo_a3_ano * TARIFA_VERMELHA - min(geracao_ano_a3, consumo_a3_ano) * (valor_credito + TARIFA_VERMELHA - TARIFA))

# ---------------------------------------------------------------- perfil horario de uma noite (por ponto, W)
perfil = []
for i in range(int(round(T_NOITE * 4))):          # passos de 15 min a partir das 18h
    hora = 18 + i / 4
    rotulo = f"{int(hora) % 24:02d}:{int((hora % 1) * 60):02d}"
    if hora < 18 + T_INTENSO:
        led = p_led
    else:
        led = p_led * fator_madrugada               # media esperada com presenca/dimerizacao
    perfil.append({"hora": rotulo, "atual_w": p_sodio * N, "led_w": round(led * N, 1)})

# ---------------------------------------------------------------- monitoramento SIMULADO (30 noites)
random.seed(2026)
inicio = date(2026, 11, 1)
linhas = []
soc = 1.0                                           # estado de carga da bateria do A2 (fracao)
for d in range(30):
    dia = inicio + timedelta(days=d)
    fim_de_semana = dia.weekday() >= 5
    presenca = min(max(random.gauss(0.28 if fim_de_semana else 0.18, 0.05), 0.05), 0.6)
    fator = presenca + (1 - presenca) * DIM
    e_led = N * (energia_kwh(p_led, T_INTENSO + T_MADRUGADA * fator) + e_iot_ponto_dia)
    hsp_dia = max(random.gauss(hsp_media, 1.3), 1.0)           # dia de sol variavel (nov/dez)
    gerado = p_fv_escolhida * hsp_dia * pr / 1000                 # kWh/dia por poste
    consumo_poste = e_led / N
    soc = min(soc + (gerado * A2["eficiencia_bateria"]["valor"] - consumo_poste / A2["eficiencia_bateria"]["valor"]) / bat_escolhida, 1.0)
    soc = max(soc, 1 - A2["profundidade_descarga"]["valor"])
    linhas.append({
        "data": dia.isoformat(),
        "fracao_presenca_madrugada": round(presenca, 3),
        "consumo_atual_kwh": round(N * e_a0_ponto_dia, 2),
        "consumo_led_sensor_kwh": round(e_led, 2),
        "hsp_simulada": round(hsp_dia, 2),
        "geracao_poste_solar_kwh": round(gerado, 3),
        "soc_bateria_poste_pct": round(soc * 100, 1),
        "geracao_fv_quiosque_kwh": round(kwp * hsp_dia * pr, 2),
    })

with open(BASE / "dados" / "monitoramento_simulado.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(linhas[0].keys()))
    w.writeheader()
    w.writerows(linhas)

# ---------------------------------------------------------------- memoria de calculo
def br(x, casas=2):
    return f"{x:,.{casas}f}".replace(",", "X").replace(".", ",").replace("X", ".")

m("# Memória de cálculo (gerada por `calculo_energia.py`)")
m()
m("Todos os valores são **projeções condicionadas às premissas** de `dados/premissas.json`, não resultados garantidos.")
m(f"Período de referência: **mês de {DIAS_MES} dias** e **ano de {DIAS_ANO} dias**; horizonte de **{ANOS} anos**; **{N} pontos de luz**.")
m()
m("## 1. Situação atual (A0)")
m(f"- Potência por ponto = lâmpada 100 W + reator 15 W = **{br(p_sodio,0)} W**")
m(f"- Tempo de funcionamento = 11 h 52 min = **{br(T_NOITE,4)} h/dia**")
m(f"- E = (P × t) / 1000 = ({br(p_sodio,0)} × {br(T_NOITE,4)}) / 1000 = **{br(e_a0_ponto_dia,4)} kWh/dia por ponto**")
m(f"- 12 pontos × 30 dias = **{br(a0['consumo_rede_kwh_mes'],1)} kWh/mês** · **{br(a0['consumo_rede_kwh_ano'],0)} kWh/ano**")
m(f"- Tarifa B4a Enel SP = TUSD 259,83 + TE 174,33 = 434,16 R$/MWh = **R$ {br(TARIFA,5)}/kWh** (sem tributos, bandeira verde)")
m(f"- Custo de energia = {br(a0['consumo_rede_kwh_ano'],0)} × {br(TARIFA,5)} = **R$ {br(a0['custo_energia_ano'])}/ano** (R$ {br(a0['custo_energia_mes'])}/mês)")
m(f"- Manutenção: troca de lâmpada a cada 4 anos × R$ 150 × 12 pontos = **R$ {br(a0_om)}/ano**")
m(f"- Emissões = {br(a0['consumo_rede_kwh_ano'],0)} kWh × {br(FE,4)} kgCO₂/kWh = **{br(a0['emissoes_kgco2_ano'],1)} kgCO₂/ano**")
m()
m("## 2. Carga comum das alternativas (mesma necessidade)")
m(f"- LED 60 W (9.000 lm) substitui a lâmpada de 10.600 lm: o LED é direcional e a luminária de sódio perde parte do fluxo no refletor, então o fluxo útil no chão é equivalente.")
m(f"- Das 18h às 23h ({br(T_INTENSO,0)} h): 100%. Madrugada ({br(T_MADRUGADA,2)} h): 30% sem movimento, 100% com presença em 20% do tempo.")
m(f"- Fator médio de madrugada = 0,20 × 1 + 0,80 × 0,30 = **{br(fator_madrugada,2)}**")
m(f"- Horas equivalentes a plena potência = {br(T_INTENSO,0)} + {br(T_MADRUGADA,4)} × {br(fator_madrugada,2)} = **{br(horas_equivalentes,4)} h**")
m(f"- E_LED = (60 × {br(horas_equivalentes,4)}) / 1000 = **{br(e_led_ponto_dia,4)} kWh/dia**")
m(f"- E_IoT = (0,5 W × 24 h) / 1000 = **{br(e_iot_ponto_dia,4)} kWh/dia**")
m(f"- **Total por ponto = {br(e_alt_ponto_dia,4)} kWh/dia** → 12 pontos: **{br(a1['consumo_rede_kwh_mes'],1)} kWh/mês**")
m(f"- Tempo em modo eficiente (dimerizado) = {br(T_MADRUGADA,2)} × 0,80 = **{br(horas_dimerizado,2)} h/dia**")
m()
m("## 3. Alternativa 1 — LED + sensores na rede")
m(f"- Consumo: **{br(a1['consumo_rede_kwh_mes'],1)} kWh/mês** (economia de **{br(a1['economia_rede_pct'],1)}%**)")
m(f"- Investimento = 12 × (LED R$ 450 + sensores/IoT R$ 200 + instalação R$ 150) + medição R$ {br(v('alt1_led_rede','custo_medicao'))} = **R$ {br(a1['capex'])}**")
m("- A medição é necessária porque, sem medidor, a iluminação pública é faturada por estimativa (potência cadastrada × 11 h 52 min) e a economia da dimerização não chegaria à conta.")
m(f"- Economia anual (energia + manutenção) = **R$ {br(a1['economia_rs_ano'])}** → payback simples **{br(a1['payback_anos'],1)} anos**")
m()
m("## 4. Alternativa 2 — Luminárias solares autônomas (off-grid)")
m(f"- Painel necessário = E / (HSP_pior_mês × PR) = {br(e_alt_ponto_dia,4)} / ({br(hsp_min,1)} × {br(pr,2)}) = **{br(p_fv_necessaria_wp,0)} Wp** → escolhido **{p_fv_escolhida} Wp** (folga de {br(margem_fv*100,0)}% no pior mês)")
m(f"- Bateria necessária = E × 2 noites / (DoD 0,90 × η 0,95) = **{br(bat_necessaria_kwh,3)} kWh** → escolhida **12,8 V × 100 Ah = {br(bat_escolhida,2)} kWh** (autonomia real {br(autonomia_real,1)} noites; descarga diária ≈ {br(descarga_diaria*100,0)}%)")
m(f"- Consumo da rede: **0 kWh/mês**; participação renovável **100%**")
m(f"- Investimento por ponto = R$ {br(capex_a2_ponto)} → **R$ {br(a2['capex'])}** (+ reposição de baterias no ano 10: R$ {br(reposicao_a2)})")
m(f"- Economia anual = **R$ {br(a2['economia_rs_ano'])}** → payback simples **{br(a2['payback_anos'],1)} anos** (maior que a vida da bateria)")
m("- Alerta técnico: luminárias solares baratas anunciadas como \"100 W\" ou \"150 W\" costumam ter painel de ~35 W e bateria de ~125 Wh — não sustentam 60 W reais a noite toda. O dimensionamento acima é o que garante o serviço.")
m()
m("## 5. Alternativa 3 — LED + sensores + solar conectada à rede (on-grid)")
m(f"- Geração = {br(kwp,1)} kWp × HSP {br(hsp_media,1)} × PR {br(pr,2)} × 365 = **{br(geracao_ano_a3,0)} kWh/ano** (consumo anual da A1 = {br(consumo_a3_ano,0)} kWh)")
m(f"- Como a luz é usada à noite, quase toda a geração é injetada e compensada depois (Lei 14.300).")
m(f"- Valor do crédito = tarifa − 60% × Fio B = {br(TARIFA,5)} − 0,60 × {br(fio_b,5)} = **R$ {br(valor_credito,5)}/kWh**")
m(f"- Custo de energia = {br(consumo_a3_ano,0)} × {br(TARIFA,5)} − {br(min(geracao_ano_a3, consumo_a3_ano),0)} × {br(valor_credito,5)} = **R$ {br(custo_a3_ano)}/ano**")
m(f"- Investimento = A1 R$ {br(a1['capex'])} + FV R$ {br(kwp*1000*A3['custo_fv_por_wp_instalado']['valor'])} = **R$ {br(a3['capex'])}** (o medidor da A1 passa a ser bidirecional)")
m(f"- Economia anual = **R$ {br(a3['economia_rs_ano'])}** → payback simples **{br(a3['payback_anos'],1)} anos**; participação renovável **{br(a3['participacao_renovavel_pct'],1)}%** (balanço anual)")
m()
m("## 6. Emissões")
m(f"- Fator médio do SIN 2024 = {br(FE,4)} tCO₂/MWh (= kgCO₂/kWh). Sensibilidade com o fator de 2023 ({br(FE_2023,4)}): A0 emitiria {br(a0['consumo_rede_kwh_ano']*FE_2023,1)} kgCO₂/ano.")
m("- A matriz elétrica brasileira já é muito renovável; por isso as emissões evitadas são pequenas em valor absoluto. O ganho ambiental maior está no fim do mercúrio das lâmpadas de sódio e na energia que deixa de ser demandada.")
m()
m("## 7. Sensibilidade — bandeira vermelha patamar 1 (+R$ 0,04463/kWh)")
for c in cenarios:
    m(f"- {c['codigo']}: custo de energia R$ {br(c['custo_energia_ano'])}/ano → R$ {br(c['custo_energia_ano_bandeira_vermelha'])}/ano")

(BASE / "calculos" / "memoria_de_calculo.md").write_text("\n".join(memoria) + "\n", encoding="utf-8")

# ---------------------------------------------------------------- saidas JSON / JS
resultado = {
    "gerado_em": date.today().isoformat(),
    "premissas_principais": {
        "pontos": N, "horas_noite": T_NOITE, "tarifa_rs_kwh": TARIFA, "fator_emissao": FE,
        "dias_mes": DIAS_MES, "horizonte_anos": ANOS,
    },
    "dimensionamento_solar": {
        "painel_necessario_wp": p_fv_necessaria_wp, "painel_escolhido_wp": p_fv_escolhida,
        "margem_pior_mes_pct": margem_fv * 100, "bateria_necessaria_kwh": bat_necessaria_kwh,
        "bateria_escolhida_kwh": bat_escolhida, "autonomia_noites": autonomia_real,
        "geracao_fv_quiosque_kwh_ano": geracao_ano_a3, "valor_credito_rs_kwh": valor_credito,
    },
    "parametros": {
        "pontos": N, "p_lampada_w": v("situacao_atual", "potencia_lampada_vapor_sodio"),
        "p_reator_w": v("situacao_atual", "perda_reator"), "p_atual_w": p_sodio,
        "fluxo_sodio_lm": v("situacao_atual", "fluxo_luminoso_lampada"),
        "mercurio_mg": v("situacao_atual", "mercurio_por_lampada"),
        "p_led_w": p_led, "fluxo_led_lm": v("luminaria_led", "fluxo_luminoso"),
        "horas_noite": T_NOITE, "horas_uso_intenso": T_INTENSO, "hora_fim_intenso": 18 + T_INTENSO,
        "dim_pct": DIM * 100, "presenca_pct": PRES * 100, "horas_dimerizado": horas_dimerizado,
        "e_a0_ponto_dia": e_a0_ponto_dia, "e_led_ponto_dia": e_led_ponto_dia,
        "e_iot_ponto_dia": e_iot_ponto_dia, "e_alt_ponto_dia": e_alt_ponto_dia,
        "tarifa_rs_kwh": TARIFA, "fator_emissao": FE, "dias_mes": DIAS_MES, "horizonte_anos": ANOS,
        "painel_wp": p_fv_escolhida, "bateria_kwh": bat_escolhida, "kwp_quiosque": kwp,
        "hsp_pior_mes": hsp_min, "hsp_media": hsp_media,
    },
    "cenarios": cenarios,
    "perfil_noite": perfil,
    "monitoramento_simulado": linhas,
}
(BASE / "calculos" / "resultados.json").write_text(json.dumps(resultado, ensure_ascii=False, indent=2), encoding="utf-8")
(BASE / "dashboard" / "dados.js").write_text(
    "// Gerado por calculos/calculo_energia.py - nao editar a mao\nwindow.SERS_DADOS = "
    + json.dumps(resultado, ensure_ascii=False) + ";\n", encoding="utf-8")

# ---------------------------------------------------------------- resumo no terminal
print(f"{'':4}{'kWh/mes rede':>14}{'econ %':>8}{'R$/mes':>10}{'renov %':>9}{'kgCO2 evit':>11}{'CAPEX':>11}{'payback':>9}{'10 anos':>11}")
for c in cenarios:
    pb = f"{c['payback_anos']:.1f}" if c["payback_anos"] else "-"
    print(f"{c['codigo']:4}{c['consumo_rede_kwh_mes']:14.1f}{c['economia_rede_pct']:8.1f}{c['custo_energia_mes']:10.2f}"
          f"{c['participacao_renovavel_pct']:9.1f}{c['emissoes_evitadas_kgco2_ano']:11.1f}{c['capex']:11.0f}{pb:>9}{c['custo_total_10_anos']:11.0f}")
print(f"Solar: painel {p_fv_necessaria_wp:.0f} Wp necessario, bateria {bat_necessaria_kwh:.2f} kWh, autonomia {autonomia_real:.2f} noites; FV quiosque {geracao_ano_a3:.0f} kWh/ano")

# ---------------------------------------------------------------- roteiro do video (mesmos numeros)
import sys
sys.path.insert(0, str(BASE / "video"))
import gerar_roteiro  # noqa: E402
gerar_roteiro.gerar(BASE)
