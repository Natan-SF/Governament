# Protocolo de votação

A votação mostra ao Revisor quem concorda ou discorda do rumo do projeto e quais falhas cada um enxerga. **O voto é consultivo: quem decide é o Revisor.**

## Quando votar

- **Plano do projeto**, antes da aprovação.
- **Mudança de rumo importante** (troca de tecnologia, de escopo ou de prazo).
- Quando o Revisor pedir (`/votacao <tema>`).

Não há votação no início de cada fase (o plano já foi votado) nem na entrega final: na entrega, a **revisão do critico** cumpre esse papel e o Revisor decide em cima dela.

## Quem vota

- O `critico`, sempre.
- Os especialistas **cuja área a proposta toca** (ex.: plano de site novo: dev e design; mudança só de texto jurídico: pesquisador). Quem não tem nada da sua área em jogo não vota.
- Sem nenhum especialista ativo não há votação; o governador avisa o Revisor.

## Como conduzir

1. Crie `sociedade/votacoes/V-<NNN>-<tema-curto>.md` a partir de `sociedade/modelos/votacao.md`.
2. Escreva no arquivo um **briefing autossuficiente de até ~40 linhas**: objetivo, proposta, alternativas descartadas, riscos já conhecidos e números que importam. O votante lê **só esse arquivo**; não lê memória do projeto nem código. Se um votante precisar conferir algo, cite o arquivo e o trecho exato no briefing.
3. Chame cada votante **separadamente**, sem mostrar o voto dos outros. Em paralelo, se forem independentes. O prompt diz: votação somente leitura, leia só `<arquivo da votação>`, responda no formato abaixo, sem relatório.
4. Anote os votos no arquivo, faça o placar e resuma as falhas.
5. Apresente ao Revisor: placar, votos contrários com motivos e falhas apontadas. Pergunte a decisão.
6. Registre a decisão no arquivo da votação e em `decisoes.md`, com o placar. Lance os tokens das chamadas de voto no orçamento.

## Formato do voto (até ~120 palavras)

```
Voto: A FAVOR | CONTRA | ABSTENÇÃO
Justificativa: (2 a 3 frases)
Falhas ou riscos que vejo: (uma linha cada; "nenhum")
O que mudaria meu voto: (condição concreta)
```

Todo voto conta no placar como foi dado. Um voto CONTRA sem falha concreta continua sendo CONTRA, mas o governador o marca como "sem falha concreta" para o Revisor pesar. O governador não vota: ele faz a proposta.
