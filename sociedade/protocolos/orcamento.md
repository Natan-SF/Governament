# Protocolo de orçamento

Cada projeto tem um orçamento de tokens aprovado pelo Revisor. O orçamento serve para ver para onde o gasto vai e decidir com o Revisor; a economia de verdade vem de como o trabalho é feito (`registro.md`, seção "Economia").

## Arquivos

- `sociedade/registro/orcamento.md`: **só o resumo** — uma linha por projeto (aprovado, gasto, saldo, %) e a divisão prevista por especialista. É o que se lê no dia a dia.
- `sociedade/registro/orcamento-lancamentos.md`: uma linha por chamada de especialista (tarefa ou voto) e uma estimativa do governador por etapa. **Só se acrescenta, pelo terminal** (`cat >> ... <<'EOF'`), sem abrir o arquivo.

## Medição

- Quando o resultado de um subagente informar o uso de tokens, lance o número exato. Quando não informar, estime e marque "estimado".
- O consumo do governador não é medido com precisão: lance uma estimativa por etapa.
- Some ao resumo uma vez por etapa, não a cada chamada.

## Regras

1. Nenhum projeto começa sem orçamento aprovado.
2. **O teto é do projeto.** A divisão por especialista é uma previsão para planejar; o governador pode remanejar entre especialistas dentro do total sem nova aprovação, e conta isso ao Revisor no resumo da etapa.
3. Dimensione pelo gasto real de tarefas parecidas em `orcamento-lancamentos.md`, não pela estimativa do especialista.
4. **Ao atingir 80%** do projeto: avise o Revisor com o saldo e a previsão do que falta.
5. **Ao atingir 100%:** pare e peça aumento ou corte de escopo.
6. Se um especialista parar sem terminar (limite de turnos ou travamento), retome o mesmo agente com SendMessage a partir do arquivo de andamento; não comece do zero.
7. O Revisor pode tirar o teto de um projeto; aí o gasto só é informado.
