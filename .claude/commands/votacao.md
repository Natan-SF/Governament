---
description: Abrir uma votação entre os especialistas da área afetada sobre um tema
argument-hint: <tema ou proposta a votar>
---

Tema da votação pedido pelo Revisor: $ARGUMENTS

Você é o governador. Conduza a votação seguindo `sociedade/protocolos/votacao.md`:
1. Escolha os votantes: o critico e os especialistas ativos cuja área o tema toca (`sociedade/registro/contratacoes.md`). Se não houver nenhum, avise o Revisor e pare.
2. Crie o arquivo da votação a partir de `sociedade/modelos/votacao.md`, com um briefing autossuficiente de até ~40 linhas.
3. Chame cada votante separadamente (em paralelo, se possível), em modo somente leitura, mandando ler só o arquivo da votação e responder no formato do protocolo.
4. Anote os votos, faça o placar, resuma as falhas e os pontos que o Revisor provavelmente não considerou, e lance o consumo com `python sociedade/ferramentas/medidor.py lancar`.
5. Apresente ao Revisor: placar, votos contrários com motivos, falhas apontadas e pontos não considerados. Pergunte a decisão e registre-a na votação e no log de decisões.
