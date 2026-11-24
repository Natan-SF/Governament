# Protocolo de pontos cegos

O Revisor dá ordens em áreas em que não é especialista. A entrega só tem qualidade superior se a sociedade levantar **o que ele não pediu porque não sabia que precisava pedir**. Isso acontece em três momentos e custa pouco: cada um vale cerca de um voto.

## 1. Na ordem: levantamento (Fase A do `/ordem`)

Antes de montar o plano, o governador chama **um** especialista, somente leitura:
- o especialista ativo da área da ordem, se houver;
- senão o `critico`;
- o `pesquisador` junto, só quando o ponto depender de lei ou norma que precise de fonte.

O briefing traz a ordem em até 15 linhas e o que já se sabe. O especialista não explora projetos. Resposta com **até 7 itens**, do mais grave ao menos grave (menos itens é melhor que enchimento):

```
N. <o ponto, em linguagem de leigo>
   Se ignorar: <consequência concreta>
   Padrão recomendado: <o que a sociedade fará se o Revisor não disser nada>
   Decisão do Revisor?: SIM (<pergunta objetiva>) | NÃO
```

Olhar ao menos:
- lei, norma e responsabilidade (quem responde se der errado);
- segurança e privacidade;
- custo recorrente e quem paga;
- quem opera e mantém depois da entrega;
- o que acontece quando falha, e como o Revisor fica sabendo;
- dados ou decisões que só o Revisor pode fornecer;
- como saber se o resultado está certo (conferência independente, amostra contra fonte externa).

O governador grava a lista em `projetos/<projeto>/pontos-cegos.md` e a leva para a proposta:
- itens **SIM** viram perguntas ao Revisor, junto das perguntas de ambiguidade (no máximo 5 perguntas ao todo; o que passar segue o padrão recomendado e é avisado);
- itens **NÃO** entram no plano e nas "Regras para especialistas" da memória do projeto.

A chamada é lançada no projeto; se a ordem não for aprovada, em "Sociedade".

## 2. Na votação

Todo voto tem o campo "O que o Revisor provavelmente não considerou" (`votacao.md`). O governador junta as respostas no resumo da votação.

## 3. Na entrega final

Além do resultado, a entrega ao Revisor traz, em linguagem simples:
- **Suposições feitas em seu nome:** cada hipótese adotada sem confirmação e o que muda se ela estiver errada.
- **O que você precisa saber para usar e manter:** passos, custos, prazos, o que conferir de tempos em tempos.
- **O que não foi feito ou não foi verificado.**
- **Pontos cegos:** a situação de cada item levantado na ordem (resolvido, aceito pelo Revisor ou pendente).

O critico confere essa lista na revisão final: item pendente sem aviso ao Revisor é falha média.
