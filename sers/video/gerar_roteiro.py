"""
Gera o roteiro do video a partir de video/falas.json e calculos/resultados.json.

Os trechos {{GRUPO.campo|casas}} das falas sao trocados pelos numeros calculados
(A0..A3 = cenarios, p = parametros). Assim a fala, a apresentacao e o dashboard
usam exatamente os mesmos valores.

Saidas:
  - dashboard/roteiro.js       -> lido pelo modo apresentacao (teleprompter)
  - video/roteiro_video.md     -> roteiro para ler/imprimir

E chamado no final de calculos/calculo_energia.py, mas tambem roda sozinho:
  python video/gerar_roteiro.py      (a partir da pasta sers/)
"""

import json
import math
import re
from datetime import date
from pathlib import Path

UNID = ["zero", "um", "dois", "três", "quatro", "cinco", "seis", "sete", "oito", "nove", "dez",
        "onze", "doze", "treze", "catorze", "quinze", "dezesseis", "dezessete", "dezoito", "dezenove"]
DEZ = ["", "", "vinte", "trinta", "quarenta", "cinquenta", "sessenta", "setenta", "oitenta", "noventa"]
CEN = ["", "cento", "duzentos", "trezentos", "quatrocentos", "quinhentos", "seiscentos",
       "setecentos", "oitocentos", "novecentos"]


def ate999(n):
    if n == 100:
        return "cem"
    c, r = divmod(n, 100)
    partes = [CEN[c]] if c else []
    if r:
        if r < 20:
            partes.append(UNID[r])
        else:
            d, u = divmod(r, 10)
            partes.append(DEZ[d] + (" e " + UNID[u] if u else ""))
    return " e ".join(partes) if partes else "zero"


def inteiro(n):
    if n < 1000:
        return ate999(n)
    mil, r = divmod(n, 1000)
    s = "mil" if mil == 1 else ate999(mil) + " mil"
    if r:
        s += (" e " if r < 100 or r % 100 == 0 else " ") + ate999(r)
    return s


def extenso(numero):
    """'1.234,5' -> por extenso (so para estimar o tempo de fala)."""
    numero = numero.replace(".", "")
    if "," in numero:
        a, b = numero.split(",", 1)
        return inteiro(int(a)) + " vírgula " + inteiro(int(b))
    return inteiro(int(numero))


def br(x, casas=0):
    return f"{x:,.{casas}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def resolver(texto, ctx):
    def troca(m):
        grupo, campo, casas = m.group(1), m.group(2), int(m.group(3) or 0)
        return br(ctx[grupo][campo], casas)
    return re.sub(r"\{\{\s*(\w+)\.(\w+)\s*(?:\|(\d))?\s*\}\}", troca, texto)


def palavras_faladas(fala):
    t = re.sub(r"\[[^\]]*\]", " ", fala)                          # acoes na tela nao sao lidas
    t = t.replace("CO₂", "cê ó dois").replace("ESP32", "ESP trinta e dois")
    t = re.sub(r"\bA([123])\b", lambda m: "A " + UNID[int(m.group(1))], t)
    t = re.sub(r"(\d[\d.]*(?:,\d+)?)\s*%", lambda m: extenso(m.group(1)) + " por cento", t)
    t = re.sub(r"\d[\d.]*(?:,\d+)?", lambda m: extenso(m.group(0)), t)
    return len(re.findall(r"[A-Za-zÀ-ÿ]+", t))


def mmss(s):
    return f"{int(s) // 60}:{int(s) % 60:02d}"


def gerar(base=None):
    base = Path(base) if base else Path(__file__).resolve().parent.parent
    falas = json.loads((base / "video" / "falas.json").read_text(encoding="utf-8"))
    res = json.loads((base / "calculos" / "resultados.json").read_text(encoding="utf-8"))
    ctx = {c["codigo"]: c for c in res["cenarios"]}
    ctx["p"] = res["parametros"]

    taxa = falas["palavras_por_segundo"]
    pausa = falas["pausa_entre_cenas_s"]
    cenas, inicio = [], 0
    for i, c in enumerate(falas["cenas"], start=1):
        fala = resolver(c["fala"], ctx)
        n = palavras_faladas(fala)
        seg = math.ceil(n / taxa)
        cenas.append({"n": i, "id": c["id"], "titulo": c["titulo"], "acao": c["acao"], "fala": fala,
                      "palavras": n, "segundos": seg, "inicio_s": inicio})
        inicio += seg + pausa
    total = inicio - pausa
    roteiro = {"gerado_em": date.today().isoformat(), "palavras_por_segundo": taxa,
               "limite_s": falas["limite_video_s"], "total_s": total, "cenas": cenas}

    (base / "dashboard" / "roteiro.js").write_text(
        "// Gerado por video/gerar_roteiro.py a partir de video/falas.json - nao editar a mao\n"
        "window.SERS_ROTEIRO = " + json.dumps(roteiro, ensure_ascii=False) + ";\n", encoding="utf-8")

    md = []
    w = md.append
    w("# Roteiro do vídeo — falas prontas")
    w("")
    w(f"**Duração estimada: {mmss(total)}** (limite do PDF: 3:00) · {len(cenas)} cenas · fala calma, ~{round(taxa * 60)} palavras por minuto.")
    w("")
    w("Cada cena abaixo é uma tela do **modo apresentação** (`dashboard/index.html`, botão *Apresentar*). "
      "Os números das falas vêm do mesmo cálculo da tela; se alguém mudar uma premissa e rodar "
      "`python calculos/calculo_energia.py`, as falas e a apresentação mudam juntas.")
    w("")
    w("Texto entre colchetes, como **[clique em A1]**, é o que você faz na tela. Não é para ler.")
    w("")
    w("## Antes de gravar")
    w("")
    w("1. Abra `sers/dashboard/index.html` no Google Chrome (dois cliques no arquivo).")
    w("2. Clique em **Apresentar para o vídeo** e aperte **F** para a tela cheia (ou F11).")
    w("3. Aperte **R** para abrir o roteiro numa janela separada. Ponha essa janela no segundo monitor, "
      "ou ao lado. Se preferir, leia as falas pelo celular (vista *Roteiro e falas* ou este arquivo).")
    w("4. Na janela do roteiro, aperte **Iniciar cronômetro** e faça um ensaio completo. "
      "Se passar de 2:50, fale um pouco mais rápido nas cenas 5 e 7.")
    w("5. Volte para a cena 1 com a tecla **Home**. As setas **→** e **←** funcionam nas duas janelas.")
    w("")
    w("## Gravar")
    w("")
    w("- **OBS Studio** (grátis): Fontes → **Captura de janela** → escolha a janela do Chrome com a apresentação. "
      "Assim só ela aparece no vídeo; a janela do roteiro fica de fora. Áudio: seu microfone.")
    w("- Sem OBS: grave a tela inteira e leia as falas pelo celular.")
    w("- Fale perto do microfone, num lugar silencioso. Mexa o mouse só na cena 7, para clicar em A1, A2 e A3; "
      "fora dela o cursor some sozinho.")
    w("")
    w("## Publicar")
    w("")
    w("1. YouTube → **Criar** → **Enviar vídeo**.")
    w("2. Título sugerido: *GS 2026.2 SERS — Praça Comunitária — Grupo 5*.")
    w("3. Em **Visibilidade**, escolha **Não listado** (não use *Privado*: o professor não conseguiria abrir).")
    w("4. Copie o link, teste numa aba anônima e cole no arquivo `.txt` de entrega.")
    w("")
    w("## Falas")
    w("")
    for c in cenas:
        w(f"### Cena {c['n']} — {c['titulo']}  ·  ≈ {c['segundos']} s  ·  começa em {mmss(c['inicio_s'])}")
        w("")
        w(f"*Na tela:* {c['acao']}")
        w("")
        fala_md = re.sub(r"\[([^\]]+)\]", r"**[\1]**", c["fala"])
        w(f"> {fala_md}")
        w("")
        w("Aperte **→** para a próxima cena." if c["n"] < len(cenas) else "Fim. Pare a gravação.")
        w("")
    w("## Checklist final")
    w("")
    w("- [ ] Vídeo com menos de 3:00")
    w("- [ ] Visibilidade **Não listado**")
    w("- [ ] Link testado numa aba anônima")
    w("- [ ] Links do vídeo e do GitHub colados no `.txt` de entrega")
    w("")
    w(f"*Gerado em {date.today().strftime('%d/%m/%Y')} por `video/gerar_roteiro.py`.*")
    (base / "video" / "roteiro_video.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    print(f"Roteiro: {len(cenas)} cenas, {sum(c['palavras'] for c in cenas)} palavras faladas, "
          f"duracao estimada {mmss(total)}")
    for c in cenas:
        print(f"  {c['n']}. {c['titulo']:<28} {c['palavras']:3d} palavras  ~{c['segundos']:2d} s")
    return roteiro


if __name__ == "__main__":
    gerar()
