# Pontos de aprovação e permissões

O Revisor (Natan) é quem aprova. Nestes pontos o governador **para, explica e espera um "aprovado" explícito**:

1. **Contratar ou encerrar especialistas.**
2. **Plano do projeto** e cada mudança importante de rumo.
3. **Ações irreversíveis ou que saem do computador:**
   - apagar ou sobrescrever arquivos fora de `projetos/` e `sociedade/registro/`;
   - `git push`, publicar pacotes ou sites, fazer deploy;
   - enviar e-mails ou mensagens, criar rascunhos em nome do Revisor, responder eventos;
   - compartilhar arquivos (Drive, Notion, artifacts) ou mudar permissões;
   - qualquer coisa que envolva pagamento ou dinheiro;
   - instalar programas ou pacotes globais.
4. **Orçamento:** ao chegar a 80% do orçamento do projeto, e para qualquer aumento.
5. **Entrega final** de cada projeto.
6. **Chamar um especialista pelo plano B** (`general-purpose` com o contrato colado), porque nesse modo a restrição de ferramentas não vale. Ver `contratacao.md`.

O governador pode, sem pedir: ler arquivos, planejar, chamar especialistas já contratados para tarefas do plano aprovado, criar e editar arquivos dentro de `projetos/<projeto>/` e atualizar os registros em `sociedade/`. O log de decisões é exceção: nele só se acrescentam linhas.

## Permissões técnicas

`.claude/settings.json` reforça só uma parte disso:
- pede confirmação para `git push` **quando rodado pela ferramenta Bash**. Pelo PowerShell não há bloqueio automático; vale a regra acima;
- bloqueia a leitura de `.env` **pela ferramenta Read**. Um comando de terminal ainda conseguiria ler; por isso especialistas só ganham terminal com justificativa.

Fora isso, a proteção vem destas regras e da lista de ferramentas de cada contrato.

## Como registrar uma aprovação

Toda aprovação ou recusa do Revisor vira uma linha em `sociedade/registro/decisoes.md` com "decidido por: Revisor".
