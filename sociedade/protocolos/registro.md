# Protocolo de registro, delegação, entrega, memória e economia

## Delegação: o briefing

Todo prompt de tarefa para um especialista segue este formato. Um bom briefing poupa o especialista de explorar o projeto, que é onde mais se gasta.

```
Tarefa T-<NNN> (<projeto>): <objetivo em uma frase>
Ler: <arquivos exatos, com trechos ou funções quando souber>
Mexer em: <arquivos ou pastas que pode alterar>
Regras do projeto: seção "Regras para especialistas" de projetos/<projeto>/memoria.md
Pronto quando: <critério verificável>
Andamento: projetos/<projeto>/andamento/T-<NNN>.md
Não releia o projeto inteiro; use Grep e leia por trechos.
```

Se a tarefa repete algo já feito em outro projeto, aponte o arquivo de origem para copiar e adaptar. As lições do cargo (`sociedade/memoria/licoes/<nome>.md`) o especialista lê sozinho: está no contrato.

## Etapas por contexto, não por turnos

O que encarece uma chamada é o **contexto**: cada ação do especialista relê tudo o que já passou por ele. O custo cresce com o quadrado do tamanho da chamada. Medido em 2026-10: uma chamada de 127 rodadas terminou com 476 mil tokens de contexto e consumiu 34 milhões; uma de 38 rodadas terminou com 136 mil e consumiu 3,3 milhões.

Por isso o corte de uma etapa é pelo tamanho do contexto, e quem avisa é o sistema:

- **Aos 100 mil tokens** de contexto o especialista recebe o aviso "CONTEXTO": termina o passo em que está, grava o andamento e entrega.
- **Aos 150 mil** recebe a ordem de parar e entregar como PARCIAL.
- Os limites ficam no início de `sociedade/ferramentas/aviso_contexto.py`. O `maxTurns` do contrato é só rede de segurança e fica folgado: o aviso chega antes, então o especialista sempre grava o andamento e entrega, em vez de ser cortado sem relatório.

Como o governador conduz:

- Planeje etapas com **um resultado testável** cada (ex.: "API e testes", depois "telas", depois "painel").
- **Entrega PARCIAL é normal.** Continue numa **chamada nova**, com briefing próprio, apontando o arquivo de andamento (o que foi feito, o que falta, arquivos tocados, comandos de teste). A chamada nova começa com ~12 mil tokens de contexto; retomar o mesmo agente com SendMessage carrega o contexto antigo inteiro.
- Use SendMessage só quando o agente travou no meio de um passo sem gravar o andamento, ou para uma pergunta curta a um agente de contexto pequeno.

O que enche o contexto de um especialista (medido): arquivos lidos inteiros 27%, arquivos gravados 21%, scripts colados no terminal 20%, saída de comandos 18%. As regras 3 e 6 do contrato atacam isso; reforce no briefing quando a tarefa tiver muito teste ou muita captura de tela (capturas só das telas que mudaram, e medir por script o que der para medir sem olhar a imagem).

## Formato de entrega dos especialistas

A resposta ao governador é curta: **no máximo ~200 palavras**. Relatórios, listas de falhas, medições e capturas vão para um arquivo em `projetos/<projeto>/` (ex.: `revisoes/T-049.md`), e a entrega aponta o caminho.

```
## Entrega: <nome do especialista>, tarefa T-<NNN>
Status: CONCLUÍDA | PARCIAL | BLOQUEADA
Resultado: (o que foi feito, em poucas linhas)
Detalhes em: (caminho do relatório; "—" se não houver)
Arquivos alterados: (lista de caminhos; "nenhum" se não houver)
Decisões que tomei: (só as que mudam o projeto, uma linha cada; "nenhuma")
Suposições que fiz: (o que adotei sem confirmação do Revisor, uma linha cada; "nenhuma")
Não testei ou não verifiquei: (uma linha cada; "nada")
Riscos ou falhas: (uma linha cada; "nenhum")
Precisa de aprovação do Revisor?: SIM (o quê) | NÃO
```

O governador confere a entrega lendo o relatório só quando precisar. As suposições e o que não foi verificado alimentam a entrega final ao Revisor (`pontos-cegos.md`).

## Revisão por diff (git local do projeto)

Cada projeto tem um repositório git só dele, dentro de `projetos/<projeto>/`, que nunca sai do computador. Ele existe para o critico revisar **o que mudou**, e não o projeto inteiro (uma revisão que explora o projeto consome 5 milhões de tokens ou mais).

```bash
python sociedade/ferramentas/projeto_git.py marco <projeto> "fase 2 aprovada"      # ao fechar cada etapa aprovada
python sociedade/ferramentas/projeto_git.py diff  <projeto> revisoes/T-NNN.diff    # antes de pedir a revisão
python sociedade/ferramentas/projeto_git.py marcos <projeto>                        # lista os marcos
```

- O briefing da revisão manda ler **só** `revisoes/T-NNN.diff`, a memória do projeto e as lições do cargo revisado. O critico abre outro arquivo apenas para confirmar uma suspeita concreta, por trecho.
- **Revise a cada fase**, enquanto o diff é pequeno, em vez de uma revisão grande no fim. Se o diff passar de ~60 KB, divida por pasta com `--so <caminho>` (um arquivo de diff e uma chamada por parte).
- Quando critico e seguranca-web olhariam o mesmo diff, chame um só com os dois focos ou dê a cada um só a sua parte.
- Depois das correções, gere o diff das correções (mesmo comando, o marco não mudou) para a conferência; aprovado, faça o marco.
- Ficam fora do repositório: dependências, saídas de build, `.env`, os próprios `.diff` e arquivos com mais de 1 MB.

## Lições das revisões

As falhas que o critico aponta servem para que os especialistas não as repitam.

1. O relatório do critico termina com **"Lições para não repetir"**: uma linha genérica (sem nome de cliente) por falha grave ou média que pode aparecer em outro projeto, com o cargo a que serve. A seguranca-web faz o mesmo quando revisa.
2. O governador acrescenta cada linha a `sociedade/memoria/licoes/<especialista>.md`, sem duplicar. **Até 15 linhas por arquivo**: ao passar disso, junte as parecidas e tire as que viraram regra do contrato.
3. Todo especialista lê o arquivo do seu cargo antes de começar (regra 2 do contrato).
4. O briefing de revisão aponta o arquivo de lições do cargo revisado. Falha que repete uma lição é **reincidência**: o governador avisa o Revisor e propõe transformar a lição em regra do contrato.

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

Uma vez por etapa (ao delegar e ao fechar), **num único comando de terminal** que junta marco do projeto, quadro, log e `medidor.py lancar`. Cada rodada do governador relê o contexto inteiro: em 2026-10, uma em cada cinco rodadas dele foi só para gravar registro ou atualizar a barra de progresso. Não atualize a cada mensagem, e mande a barra de progresso na mesma rodada de outra ferramenta.

## Memória

- `sociedade/memoria/sociedade.md`: lições que valem para qualquer projeto, sem nome de cliente. Uma linha por lição.
- `sociedade/memoria/licoes/<especialista>.md`: lições das revisões, por cargo (acima).
- `projetos/<projeto>/memoria.md`: criada a partir de `sociedade/modelos/memoria-projeto.md`. **Até ~5 KB**, porque todo especialista lê esse arquivo a cada chamada. Guarde o estado atual, as regras e os próximos passos; o histórico já está no log de decisões. Quando passar do tamanho, mova o que é histórico para `projetos/<projeto>/historico.md`.
- O governador atualiza a memória do projeto no fim de cada fase e a da sociedade quando aprende algo que vale para outros projetos.

## Economia de tokens

O consumo se mede com `sociedade/ferramentas/medidor.py`, em TE (`orcamento.md`). Onde ele aparece, em ordem de peso (medido nos transcritos de 2026-10 e 2026-11):

1. **Chamadas longas de especialista:** quatro chamadas de 96 a 175 rodadas foram 62% de todo o consumo dos especialistas. Remédio: etapas por contexto (acima) e contexto enxuto.
2. **Contexto do governador:** cerca de 40% do consumo total. Cada rodada dele começa com ~78 mil tokens fixos (ferramentas, plugins e listas carregados na sessão; `/context` mostra a divisão) e a média foi de 168 mil. Remédio: sessão nova (`/clear`) **a cada fase**, não só a cada projeto, com a memória do projeto como passagem de bastão; registros num só comando; chamadas independentes na mesma rodada; trabalho direto só quando é pequeno. O sistema avisa o Revisor quando o contexto do governador passa de 500 mil.
3. **Revisões que exploram o projeto** (5 milhões ou mais). Remédio: revisão por diff, a cada fase.
4. **Leitura fixa por chamada** (contrato + memória do projeto + lições). Remédio: contratos genéricos, memórias e lições curtas.

**Onde não economizar:** votos e pontos cegos custam 30 a 50 mil TE por chamada, menos de 1% de uma etapa, e são o que pega cedo o erro caro. Chame todos os votantes da área afetada.

Hábitos que mantêm a qualidade e custam pouco:
- Correção pequena e bem localizada (poucas linhas, arquivo conhecido, até ~5 ações): o governador faz direto. Acima disso vai para um especialista, que começa com contexto seis vezes menor que o do governador.
- Copiar e adaptar o que já existe em outro projeto antes de pedir para escrever do zero.
- Capturas de tela só nas telas que mudaram, no tamanho necessário.
- Processo que demora (download, servidor, carga) roda em segundo plano, iniciado pelo governador; o especialista escreve e testa o script.
- Modelo: use o do contrato. Para tarefa leve de um especialista caro (conferência curta, pergunta pontual), o governador pode chamar com `model: sonnet`. Plano e revisão final ficam no modelo do contrato.
