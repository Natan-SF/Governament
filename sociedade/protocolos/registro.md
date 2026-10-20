# Protocolo de registro, entrega e memória

## Quadro de tarefas (`sociedade/registro/quadro.md`)

- Cada tarefa recebe um ID `T-<NNN>` em sequência e não muda mais.
- Status possíveis: `a fazer`, `em andamento`, `aguardando aprovação`, `bloqueada`, `concluída`, `cancelada`.
- Cada tarefa tem um único responsável (um especialista ou o governador).
- Atualize o quadro ao delegar, ao receber cada entrega e quando algo travar.

## Log de decisões (`sociedade/registro/decisoes.md`)

- Cada decisão recebe um ID `D-<NNN>` em sequência.
- "Decidido por" diz **quem tomou a decisão**: `Revisor`, `Governador` ou `<nome do especialista>`. Se veio de uma votação, inclua o placar e o ID da votação.
- Decisões técnicas pequenas que um especialista tomou durante a tarefa também entram, a partir da seção "Decisões que tomei" da entrega dele.
- **Só acrescente linhas.** Para corrigir ou desfazer uma decisão, crie uma nova entrada que cite a anterior ("revoga D-012").

## Formato de entrega dos especialistas

Todo especialista termina a tarefa com:

```
## Entrega: <nome do especialista>, tarefa T-<NNN>
Status: CONCLUÍDA | PARCIAL | BLOQUEADA
Resultado: (o que foi feito, em poucas linhas)
Arquivos criados ou alterados: (lista de caminhos; "nenhum" se não houver)
Decisões que tomei: (cada uma com o motivo; "nenhuma" se não houver)
Riscos, dúvidas ou falhas que encontrei: (lista; "nenhum" se não houver)
Precisa de aprovação do Revisor?: SIM (o quê) | NÃO
```

O governador confere a entrega, atualiza o quadro, copia as decisões para o log e, se for o caso, leva os pontos ao Revisor.

## Memória

- `sociedade/memoria/sociedade.md`: lições que valem para qualquer projeto (o que funcionou, o que falhou, preferências do Revisor).
- `projetos/<projeto>/memoria.md`: contexto do projeto (objetivo, decisões-chave, estado atual, próximos passos). Crie ao abrir o projeto.
- O governador atualiza a memória do projeto no fim de cada fase e a da sociedade quando aprende algo que vale para outros projetos. Mantenha as duas curtas: elas são lidas sempre e custam tokens.
