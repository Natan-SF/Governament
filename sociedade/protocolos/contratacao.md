# Protocolo de contratação

Especialistas são contratados por projeto, para tarefas definidas. O governador recomenda e o Revisor aprova.

## 1. Recomendar

Ao receber uma ordem, o governador apresenta ao Revisor uma **proposta de contratação** com uma linha por especialista:

| Nome | Função | Por que é necessário | Ferramentas | Modelo | maxTurns | Orçamento (tokens) |
|---|---|---|---|---|---|---|

Regras para a proposta:
- **Contrate o mínimo.** Não crie um especialista para uma tarefa que o governador resolve sozinho com facilidade.
- **Escolha o modelo pelo trabalho:** `haiku` para tarefas simples e repetitivas, `sonnet` para a maior parte do trabalho, `opus` só para raciocínio difícil. Modelo mais forte custa mais.
- **Ferramentas mínimas.** Só o que a função precisa (ver abaixo).
- Se já existe um especialista ativo que serve, proponha reaproveitá-lo em vez de contratar outro.

## 2. Ferramentas

- O campo `tools:` é **obrigatório** e nunca pode ficar em branco: um agente sem essa linha herda todas as ferramentas, inclusive as de enviar e-mail, compartilhar arquivos e pagamentos.
- Ferramentas só de leitura: `Read, Grep, Glob`.
- Para escrever arquivos: acrescente `Write, Edit`.
- Para rodar comandos: `Bash` ou `PowerShell`. Justifique na proposta.
- Web: `WebSearch, WebFetch`.
- Ferramentas MCP (Gmail, Drive, Notion, navegador etc.) só pelo nome exato e com justificativa. Ações que saem do computador (enviar, compartilhar, publicar, pagar) continuam exigindo aprovação, mesmo que o agente tenha a ferramenta. Ver `aprovacao.md`.

## 3. Formalizar (só depois do "aprovado")

1. Copie `sociedade/modelos/contrato-especialista.md` para `.claude/agents/<nome>.md` e preencha todos os campos. Nome em kebab-case, sem acento (ex.: `pesquisador-mercado`).
2. Adicione uma linha em `sociedade/registro/contratacoes.md`.
3. Registre a decisão em `sociedade/registro/decisoes.md` (decidido por: Revisor, a partir da recomendação do governador).
4. Adicione o orçamento do especialista em `sociedade/registro/orcamento.md`.

**Depois de contratar, peça ao Revisor para reabrir o Claude Code** antes da primeira chamada ao especialista. Um agente criado no meio da sessão pode só aparecer depois disso, e é assim que a restrição de ferramentas do contrato passa a valer.

Plano B, **só com "aprovado" explícito do Revisor**: chamar com `subagent_type: general-purpose`, colando o contrato inteiro no início do prompt. Explique ao Revisor o risco: nesse modo o agente tem acesso a todas as ferramentas, e a lista do contrato vira só uma instrução, não um limite.

## 4. Encerrar contrato

Quando o projeto ou a função acabar, ou por decisão do Revisor:
1. Mova `.claude/agents/<nome>.md` para `sociedade/arquivo/agentes/<nome>.md`.
2. Atualize a linha em `contratacoes.md` (status: encerrado, data, motivo).
3. Registre em `decisoes.md`.
4. Se o especialista aprendeu algo útil para o futuro, anote na memória do projeto ou da sociedade.
