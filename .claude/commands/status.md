---
description: Mostrar o estado da Sociedade Artificial (tarefas, especialistas, orçamento, pendências)
---

Você é o governador. Sem alterar nenhum arquivo, leia só o necessário:
- tarefas vivas: `grep -v "concluída\|cancelada" sociedade/registro/quadro.md`
- `sociedade/registro/contratacoes.md` (só as linhas com status ativo)
- `sociedade/registro/orcamento.md` (resumo; não abra os lançamentos)
- `tail -n 3 sociedade/registro/decisoes.md`
- votações sem decisão: `grep -l "Decisão: PENDENTE" sociedade/votacoes/V-*.md`

Responda ao Revisor em português, curto, nesta ordem:
1. **Aguardando sua aprovação:** o que está parado esperando o Revisor (ou "nada").
2. **Em andamento:** tarefas, com o responsável de cada uma.
3. **Especialistas ativos:** nome, função e projetos.
4. **Orçamento:** gasto e saldo por projeto, com alerta se algum passou de 80%.
5. **Últimas decisões:** as 3 mais recentes, com quem decidiu.
