# Roteiro do vídeo — falas prontas

**Duração estimada: 2:35** (limite do PDF: 3:00) · 9 cenas · fala calma, ~144 palavras por minuto.

Cada cena abaixo é uma tela do **modo apresentação** (`dashboard/index.html`, botão *Apresentar*). Os números das falas vêm do mesmo cálculo da tela; se alguém mudar uma premissa e rodar `python calculos/calculo_energia.py`, as falas e a apresentação mudam juntas.

Texto entre colchetes, como **[clique em A1]**, é o que você faz na tela. Não é para ler.

## Antes de gravar

1. Abra `sers/dashboard/index.html` no Google Chrome (dois cliques no arquivo).
2. Clique em **Apresentar para o vídeo** e aperte **F** para a tela cheia (ou F11).
3. Aperte **R** para abrir o roteiro numa janela separada. Ponha essa janela no segundo monitor, ou ao lado. Se preferir, leia as falas pelo celular (vista *Roteiro e falas* ou este arquivo).
4. Na janela do roteiro, aperte **Iniciar cronômetro** e faça um ensaio completo. Se passar de 2:50, fale um pouco mais rápido nas cenas 5 e 7.
5. Volte para a cena 1 com a tecla **Home**. As setas **→** e **←** funcionam nas duas janelas.

## Gravar

- **OBS Studio** (grátis): Fontes → **Captura de janela** → escolha a janela do Chrome com a apresentação. Assim só ela aparece no vídeo; a janela do roteiro fica de fora. Áudio: seu microfone.
- Sem OBS: grave a tela inteira e leia as falas pelo celular.
- Fale perto do microfone, num lugar silencioso. Mexa o mouse só na cena 7, para clicar em A1, A2 e A3; fora dela o cursor some sozinho.

## Publicar

1. YouTube → **Criar** → **Enviar vídeo**.
2. Título sugerido: *GS 2026.2 SERS — Praça Comunitária — Grupo 5*.
3. Em **Visibilidade**, escolha **Não listado** (não use *Privado*: o professor não conseguiria abrir).
4. Copie o link, teste numa aba anônima e cole no arquivo `.txt` de entrega.

## Falas

### Cena 1 — Abertura  ·  ≈ 7 s  ·  começa em 0:00

*Na tela:* Comece a gravação já nesta tela e fale assim que ela começar.

> Olá! Somos o Grupo 5. Esta é a nossa solução de energia para uma praça comunitária.

Aperte **→** para a próxima cena.

### Cena 2 — O espaço e o problema  ·  ≈ 20 s  ·  começa em 0:08

*Na tela:* Só fale. A tela mostra a praça de madrugada, vazia e com os postes no máximo.

> Escolhemos uma praça de bairro em São Paulo, com 12 postes de vapor de sódio. Eles ficam no máximo a noite toda, mesmo com a praça vazia, e ninguém sabe quando uma lâmpada queima. Quem ganha com a melhoria: os moradores e a prefeitura, que paga a conta.

Aperte **→** para a próxima cena.

### Cena 3 — Quanto a praça gasta hoje  ·  ≈ 18 s  ·  começa em 0:29

*Na tela:* Só fale. A conta aparece passo a passo, de cima para baixo.

> Para o consumo, usamos E igual a P vezes t, dividido por mil. Com 115 watts por quase 12 horas, os 12 postes gastam 491 quilowatts-hora por mês: 213 reais na conta.

Aperte **→** para a próxima cena.

### Cena 4 — LED com sensor de presença  ·  ≈ 18 s  ·  começa em 0:48

*Na tela:* Só fale. Uma pessoa atravessa a praça e os postes perto dela acendem.

> A solução começa com LED de 60 watts e sensor de presença. Até as 23 horas, luz total. Depois, cai para 30% e volta a 100% quando alguém passa. O consumo cai 64%.

Aperte **→** para a próxima cena.

### Cena 5 — Três alternativas  ·  ≈ 26 s  ·  começa em 1:07

*Na tela:* Só fale. Os três cartões e o custo em 10 anos já estão na tela.

> Comparamos três alternativas para a mesma iluminação. A1 é a mais barata, mas usa só a rede. A2 é 100% solar, com bateria em cada poste, mas leva 24 anos para se pagar. A3 soma painéis no quiosque: 99% renovável, com retorno em 7,6 anos. É a nossa escolha.

Aperte **→** para a próxima cena.

### Cena 6 — Diagrama da solução  ·  ≈ 15 s  ·  começa em 1:34

*Na tela:* Só fale. As camadas aparecem de cima para baixo.

> No diagrama, a energia da rede e dos painéis alimenta as luminárias. Sensores mandam dados para um ESP32 em cada poste, que controla a luz, e esses dados viram os indicadores do dashboard.

Aperte **→** para a próxima cena.

### Cena 7 — Indicadores no dashboard  ·  ≈ 21 s  ·  começa em 1:50

*Na tela:* Clique em A1, A2 e A3 nos momentos marcados (ou aperte 1, 2 e 3).

> No dashboard, **[clique em A1]** cada alternativa mostra seus indicadores: consumo, economia, custo, energia renovável, CO₂ evitado e horas em modo econômico. **[clique em A2]** Na A2, tudo vem do sol. **[clique em A3]** Na A3, 99% renovável e 214 reais a menos por mês. O monitoramento é simulado.

Aperte **→** para a próxima cena.

### Cena 8 — Benefícios e limitações  ·  ≈ 16 s  ·  começa em 2:12

*Na tela:* Só fale. Benefícios à esquerda, limitações à direita.

> Benefícios: menos gasto, luz branca quando tem gente, aviso de falha e fim do mercúrio. Limitações: a praça é um caso de referência, os preços são estimativas e, sem energia na rede, a A3 também apaga.

Aperte **→** para a próxima cena.

### Cena 9 — Encerramento  ·  ≈ 6 s  ·  começa em 2:29

*Na tela:* Depois de falar, espere 2 segundos em silêncio e pare a gravação.

> Esses números são projeções baseadas nas nossas premissas; os detalhes estão no GitHub. Obrigado!

Fim. Pare a gravação.

## Checklist final

- [ ] Vídeo com menos de 3:00
- [ ] Visibilidade **Não listado**
- [ ] Link testado numa aba anônima
- [ ] Links do vídeo e do GitHub colados no `.txt` de entrega

*Gerado em 09/11/2026 por `video/gerar_roteiro.py`.*
