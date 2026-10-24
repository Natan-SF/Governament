# Protocolo de contratação

O governador recomenda e o Revisor aprova. Um especialista é contratado para um **cargo** (dev web, design, dados...) e pode servir a vários projetos.

## 1. Recomendar

Ao receber uma ordem, o governador apresenta ao Revisor uma **proposta de contratação** com uma linha por especialista:

| Nome | Função | Por que é necessário | Ferramentas | Modelo | Orçamento previsto (tokens) |
|---|---|---|---|---|---|

Regras para a proposta:
- **Reaproveite primeiro.** Se um especialista ativo já cobre o cargo, use-o no projeto novo: basta escrever as regras do projeto na memória do projeto. Não precisa mexer no contrato.
- **Contrate o mínimo.** Não crie um especialista para o que o governador resolve sozinho.
- **Modelo pelo trabalho:** `haiku` para tarefas simples e repetitivas, `sonnet` para a maior parte, `opus` só para raciocínio difícil (crítica, segurança, direção de arte).
- **Ferramentas mínimas** (ver abaixo).

## 2. Ferramentas

- O campo `tools:` é **obrigatório** e nunca pode ficar em branco: um agente sem essa linha herda todas as ferramentas, inclusive as de enviar e-mail, compartilhar arquivos e pagamentos.
- Só leitura: `Read, Grep, Glob`. Escrever: `+ Write, Edit`. Terminal: `Bash` ou `PowerShell`, com justificativa. Web: `WebSearch, WebFetch`.
- Ferramentas MCP (Gmail, Drive, Notion, navegador etc.) só pelo nome exato e com justificativa. Ações que saem do computador continuam exigindo aprovação (`aprovacao.md`).

## 3. Contrato: genérico por cargo

O contrato é o prompt de sistema do especialista e é reenviado a cada ação dele, então fica **curto e sem nada de projeto**:
- Contém: função, regras do cargo, critério de pronto.
- **Não contém:** regras, caminhos, cliente, identidade visual ou orçamento de um projeto. Isso vai na seção "Regras para especialistas" de `projetos/<projeto>/memoria.md`, que o briefing manda ler.
- `description` em uma frase sobre o cargo (ela aparece no contexto do governador em toda sessão).

## 4. Formalizar (só depois do "aprovado")

1. Copie `sociedade/modelos/contrato-especialista.md` para `.claude/agents/<nome>.md` e preencha. Nome em kebab-case, sem acento.
2. Acrescente uma linha em `sociedade/registro/contratacoes.md` e a decisão em `decisoes.md` (decidido por: Revisor).
3. Lance o orçamento previsto em `sociedade/registro/orcamento.md`.

Um contrato criado ou alterado no meio da sessão pode só valer depois de reabrir o Claude Code. Se o agente não aparecer, tente de novo depois da próxima notificação; se ainda falhar, peça ao Revisor para reabrir.

Plano B, **só com "aprovado" explícito do Revisor**: chamar com `subagent_type: general-purpose`, colando o contrato inteiro no início do prompt. Nesse modo o agente tem acesso a todas as ferramentas, e a lista do contrato vira só uma instrução.

## 5. Encerrar contrato

Quando o cargo não for mais necessário, ou por decisão do Revisor:
1. Mova `.claude/agents/<nome>.md` para `sociedade/arquivo/agentes/<nome>.md`.
2. Atualize a linha em `contratacoes.md` (status, data, motivo) e registre em `decisoes.md`.
3. Se o especialista aprendeu algo útil, anote na memória do projeto ou da sociedade.

Sair de um projeto não encerra o contrato: basta atualizar a linha em `contratacoes.md`.
