# Protocolo de registro, delegação, entrega, memória e economia

## Delegação: o briefing

Todo prompt de tarefa para um especialista segue este formato. Um bom briefing poupa o especialista de explorar o projeto, que é onde mais se gasta.

```
Tarefa T-<NNN> (<projeto>): <objetivo em uma frase>
Ler: <arquivos exatos, com trechos ou funções quando souber>
Mexer em: <arquivos ou pastas que pode alterar>
Regras do projeto: seção "Regras para especialistas" de projetos/<projeto>/memoria.md
Pronto quando: <critério verificável>
Andamento: projetos/<projeto>/andamento/T-<NNN>.md  (só para tarefa em etapas)
Não releia o projeto inteiro; use Grep e leia por trechos.
```

Se a tarefa repete algo já feito em outro projeto, aponte o arquivo de origem para copiar e adaptar.

## Tarefas grandes: etapas, não maratonas

O contexto inteiro do especialista é reenviado a cada ação, então uma chamada longa custa cada vez mais por ação. Por isso:

- Divida o trabalho em etapas de **até ~40 ações** cada, com um resultado testável no fim de cada uma (ex.: "API e testes", depois "telas", depois "painel").
- Cada etapa é uma chamada nova, com briefing próprio. O especialista grava o andamento em `projetos/<projeto>/andamento/T-<NNN>.md` (o que fez, o que falta, arquivos tocados, comandos de teste). A etapa seguinte lê esse arquivo em vez de redescobrir o código.
- Se uma etapa travar ou acabar no meio, retome o **mesmo** agente com SendMessage, que mantém o contexto. Não comece outra chamada do zero.
- Isso não é limite de gasto: é decomposição. O trabalho total é o mesmo, com contexto menor em cada passo.

## Formato de entrega dos especialistas

A resposta ao governador é curta: **no máximo ~200 palavras**. Relatórios, listas de falhas, medições e capturas vão para um arquivo em `projetos/<projeto>/` (ex.: `revisoes/T-049.md`), e a entrega aponta o caminho.

```
## Entrega: <nome do especialista>, tarefa T-<NNN>
Status: CONCLUÍDA | PARCIAL | BLOQUEADA
Resultado: (o que foi feito, em poucas linhas)
Detalhes em: (caminho do relatório; "—" se não houver)
Arquivos alterados: (lista de caminhos; "nenhum" se não houver)
Decisões que tomei: (só as que mudam o projeto, uma linha cada; "nenhuma")
Riscos ou falhas: (uma linha cada; "nenhum")
Precisa de aprovação do Revisor?: SIM (o quê) | NÃO
```

O governador confere a entrega lendo o relatório só quando precisar.

## Quadro de tarefas (`sociedade/registro/quadro.md`)

- Cada tarefa recebe um ID `T-<NNN>` em sequência e não muda mais. Pegue o próximo número logo antes de gravar (`grep -o 'T-[0-9]*' ... | sort | tail -1`, olhando também `quadro-arquivo.md`).
- Status: `a fazer`, `em andamento`, `aguardando aprovação`, `bloqueada`, `concluída`, `cancelada`.
- Um responsável por tarefa. Descrição em uma linha curta; o detalhe fica na memória do projeto.
- Atualize ao delegar, ao receber a entrega e quando algo travar.
- Ao fechar uma etapa, mova as tarefas concluídas e canceladas para `quadro-arquivo.md`. O quadro só mostra o que está vivo.

## Log de decisões (`sociedade/registro/decisoes.md`)

- Cada decisão recebe um ID `D-<NNN>` em sequência. Pegue o próximo com `tail -n 1`.
- "Decidido por" diz quem decidiu: `Revisor`, `Governador` ou `<especialista>`. Se veio de votação, o ID e o placar.
- **Linha curta (até ~30 palavras).** O detalhe fica na memória do projeto ou no relatório; a linha aponta para ele.
- Entram as decisões do Revisor, as do governador que mudam o rumo e as decisões de especialista que mudam o projeto. Decisões técnicas miúdas ficam só no relatório da entrega.
- **Só acrescente linhas, pelo terminal**, sem abrir o arquivo:
  ```bash
  tail -n 1 sociedade/registro/decisoes.md   # último ID
  cat >> sociedade/registro/decisoes.md <<'EOF'
  | D-NNN | AAAA-MM-DD | decisão | quem | votação | motivo |
  EOF
  ```
- Para corrigir, crie uma nova entrada que cite a anterior ("revoga D-012").

## Quando atualizar os registros

Uma vez por etapa (ao delegar e ao fechar), juntando quadro, log e lançamentos de orçamento num só passo. Não atualize a cada mensagem.

## Memória

- `sociedade/memoria/sociedade.md`: lições que valem para qualquer projeto, sem nome de cliente. Uma linha por lição.
- `projetos/<projeto>/memoria.md`: criada a partir de `sociedade/modelos/memoria-projeto.md`. **Até ~5 KB**, porque todo especialista lê esse arquivo a cada chamada. Guarde o estado atual, as regras e os próximos passos; o histórico já está no log de decisões. Quando passar do tamanho, mova o que é histórico para `projetos/<projeto>/historico.md`.
- O governador atualiza a memória do projeto no fim de cada fase e a da sociedade quando aprende algo que vale para outros projetos.

## Economia de tokens

Onde o gasto aparece, em ordem de peso (medido nos projetos de 2026-10):

1. **Chamadas longas de especialista** (300 a 480 mil tokens em 110 a 190 ações). Remédio: briefing com arquivos exatos e etapas de até ~40 ações (acima).
2. **Revisões que releem tudo** (critico gastou 137 a 152 mil). Remédio: revisar só o diff ou a lista de arquivos; quando critico e seguranca-web olhariam o mesmo código, chame um só com os dois focos ou dê a cada um só a sua parte.
3. **Votações com todos** (~136 mil com 5 votantes). Remédio: `votacao.md`.
4. **Contexto do governador:** cada entrega longa e cada arquivo lido ficam na conversa para sempre. Remédio: entregas curtas com relatório em arquivo, registros pelo terminal, e uma sessão nova (`/clear`) ao trocar de projeto; a memória do projeto é a passagem de bastão.
5. **Leitura fixa por chamada** (contrato + memória do projeto + memória da sociedade). Remédio: contratos genéricos e memórias curtas.

Hábitos que mantêm a qualidade e custam pouco:
- Correção pequena e bem localizada (poucas linhas, arquivo conhecido): o governador faz direto com Grep + edição.
- Copiar e adaptar o que já existe em outro projeto antes de pedir para escrever do zero.
- Capturas de tela só nas telas que mudaram, no tamanho necessário.
- Especialista não lê arquivos grandes inteiros: Grep e leitura por trechos.
- Processo que demora (download, servidor, carga) roda em segundo plano, iniciado pelo governador; o especialista escreve e testa o script.
- Modelo: use o do contrato. Para tarefa leve de um especialista caro (conferência curta, pergunta pontual), o governador pode chamar com `model: sonnet`. Plano e revisão final ficam no modelo do contrato.
