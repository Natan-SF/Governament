# Protocolo de orçamento

Cada projeto tem um orçamento aprovado pelo Revisor. O orçamento serve para ver para onde o consumo vai e decidir com o Revisor; a economia de verdade vem de como o trabalho é feito (`registro.md`, seção "Economia").

## Unidade: TE (tokens equivalentes)

Desde 2026-11-13 o orçamento é em **TE**, medido pelo `medidor.py` direto nos transcritos do Claude Code:

```
TE = entrada nova + 1,25 × escrita de cache (5 min) + 2 × escrita de cache (1 h)
     + 0,1 × leitura de cache + 5 × saída
```

Cada tipo de token pesa pelo que custa em relação a um token de entrada. O TE não distingue o modelo: o medidor mostra o modelo de cada chamada, e opus custa mais que sonnet pelo mesmo TE.

**O número antigo não media consumo.** O "total de tokens" que o resultado de um subagente informa é o tamanho do contexto no fim da chamada. Como cada ação relê o contexto inteiro, o consumo real é muito maior: uma chamada lançada como 476 mil consumiu 34 milhões de tokens (2,6 milhões de TE). As linhas antigas de `orcamento-lancamentos.md` ficam como estão, mas **não são comparáveis** com as novas; tetos aprovados na unidade antiga precisam ser refeitos em TE pelo Revisor.

## Arquivos

- `sociedade/registro/orcamento.md`: **só o resumo** — uma linha por projeto (aprovado, gasto, saldo, %) e a divisão prevista por especialista. É o que se lê no dia a dia.
- `sociedade/registro/orcamento-lancamentos.md`: uma linha por chamada de especialista (tarefa ou voto) e uma por sessão do governador. **Só o medidor acrescenta linhas.**
- `sociedade/registro/medidor-estado.json`: o que já foi lançado. Não edite.

## Medição

```bash
python sociedade/ferramentas/medidor.py lancar [--projeto NOME]   # uma vez por etapa
python sociedade/ferramentas/medidor.py resumo [--sessao ID]       # consulta, não grava
python sociedade/ferramentas/medidor.py retroativo                 # soma por projeto, não grava
```

- `lancar` acrescenta o que ainda não foi lançado: cada chamada de especialista e o trecho novo de cada sessão do governador. O consumo do governador é **medido**, não estimado.
- O projeto de cada chamada vem do briefing (nome do projeto ou arquivo da votação). `--projeto` vale para o governador e para chamadas sem projeto identificável; sem ele, vai para "Sociedade".
- Some ao resumo uma vez por etapa, com os totais que o `lancar` mostra.
- Os transcritos são apagados pelo Claude Code depois de 30 dias (`cleanupPeriodDays`): quem não lança por etapa perde a medição.

## Regras

1. Nenhum projeto começa sem orçamento aprovado (a chamada de pontos cegos da Fase A é a exceção, e é lançada).
2. **O teto é do projeto.** A divisão por especialista é uma previsão para planejar; o governador pode remanejar entre especialistas dentro do total sem nova aprovação, e conta isso ao Revisor no resumo da etapa.
3. Dimensione pelo consumo medido de tarefas parecidas (`medidor.py retroativo` e as linhas "medido (TE)" dos lançamentos), não pela estimativa do especialista.
4. **Ao atingir 80%** do projeto: avise o Revisor com o saldo e a previsão do que falta.
5. **Ao atingir 100%:** pare e peça aumento ou corte de escopo.
6. Se um especialista entregar PARCIAL ou parar sem terminar, continue numa chamada nova a partir do arquivo de andamento (`registro.md`, "Etapas por contexto").
7. O Revisor pode tirar o teto de um projeto; aí o consumo só é informado.
