# Protocolo de orçamento

Cada projeto tem um orçamento de tokens aprovado pelo Revisor, dividido entre os especialistas.

## O que é controle de verdade e o que é acompanhamento

- **Limite rígido:** só o `maxTurns` do contrato. Ele interrompe o especialista quando o número de turnos acaba.
- **Acompanhamento:** os tokens são anotados pelo governador. Quando o resultado de um subagente informar o uso de tokens, anote o número exato. Quando não informar, estime e marque como "estimado".
- O consumo do próprio governador não é medido com precisão. Anote uma estimativa por fase.

## Regras

1. Nenhum projeto começa sem orçamento aprovado.
2. Antes de chamar um especialista, confira se o saldo dele cobre a tarefa.
3. Depois de cada chamada (inclusive votos), atualize `sociedade/registro/orcamento.md`.
4. **Ao atingir 80%** do orçamento do projeto: avise o Revisor com o saldo e uma previsão do que falta.
5. **Ao atingir 100%:** pare e peça aumento ou corte de escopo. Não continue sem aprovação.
6. Se um especialista estourar o `maxTurns` sem terminar, não o chame de novo automaticamente: avise o Revisor e proponha dividir a tarefa ou ajustar o contrato.
