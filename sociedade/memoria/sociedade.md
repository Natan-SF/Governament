# Memória da sociedade

Lições que valem para todos os projetos, sem nome de cliente. Uma linha por lição. É lida sempre: mantenha curta.

## Preferências do Revisor
- Fala português; quer respostas curtas e diretas.
- Aprova pessoalmente contratações, planos, ações irreversíveis, orçamento e entregas.
- Quer ver quem concorda ou discorda do rumo (votações) para evitar falhas, com qualidade alta e sem desperdício de tokens.
- Quer ser avisado quando um especialista parar no limite de turnos ou o projeto passar do orçamento (D-072). Um projeto pode ficar sem teto se ele decidir; aí o gasto só é informado.
- Sites: sem "cubo azul" ao tocar ou selecionar, caixa de opção escolhida recuada, barra "Continuar" só depois da primeira escolha. CSS no contrato do designer-visual, "Toque no celular" (D-144).
- No git vai só a estrutura da sociedade; projetos, registros e votações ficam só no computador (D-148).

## Núcleo permanente
- `critico` (revisão crítica) e `pesquisador` (pesquisa com fontes) atendem todos os projetos (D-013). O critico vota em toda votação; o pesquisador, quando a área for afetada.
- Em projeto novo, reaproveite especialistas ativos e proponha só os que faltam.

## Economia (medido em 2026-10)
- Estimativas saem 2 a 3 vezes abaixo do real. Dimensione pelo gasto real de tarefas parecidas em `orcamento-lancamentos.md`.
- Chamadas de 110 a 190 ações custaram 320 a 480 mil tokens cada; o custo por ação cresce com o contexto. Etapas de até ~40 ações com arquivo de andamento.
- Revisão que relê o projeto custa 140 a 150 mil; por diff custa bem menos. Votação com 5 votantes ~136 mil; com briefing e só áreas afetadas, bem menos.
- Correções pequenas e localizadas o governador faz direto (D-136).
- Copiar e adaptar um projeto parecido sai muito mais barato que escrever do zero.
- Contrato e memória do projeto são lidos a cada ação: mantenha os dois curtos.

## Lições técnicas
- Downloads e processamentos longos: o governador roda em segundo plano; o especialista só escreve e testa o script.
- Verificações automáticas podem passar com resultado errado. Sempre uma conferência independente e uma amostra contra fonte externa.
- Especialista recém-contratado ou contrato alterado costuma só valer depois de reabrir o Claude Code (às vezes aparece após a próxima notificação). Mudança de `maxTurns` só vale depois de reabrir.
- Especialista pode travar no meio. Exija andamento em arquivo e retome o mesmo agente com SendMessage; antes, encerre os processos que ele deixou abertos (servidor, navegador headless).
- Encerrar processos SÓ filtrando pelo nome do executável (node, workerd, msedge) E pelo caminho do projeto na linha de comando. Filtro por número solto já derrubou o navegador do Revisor (D-133). Repita isso no briefing de toda tarefa que abre servidor ou navegador.
- Duas sessões podem escrever nos registros ao mesmo tempo: pegue o próximo número de T e D logo antes de gravar.
- WebFetch não lê alguns servidores de dados abertos (WebDAV); o governador confere com curl. Dê ao pesquisador tarefas com poucos pontos.
- Dados abertos de CNPJ da Receita: o caminho antigo dá 404; use o WebDAV público `https://arquivos.receitafederal.gov.br/public.php/dav/files/YggdBLfdninEJX9/AAAA-MM/` (aceita Range).
- Acervo de leis local (`C:/Users/natan/leis`): parte dos arquivos só está no git; leia com `git -C C:/Users/natan/leis show HEAD:<caminho>`. O advogado-artificial é agente pessoal do Revisor (fora da sociedade) e não grava arquivos: o governador salva o parecer.
- Textos legais (privacidade, prazos, direitos) só prometem o que o código faz: confira cada frase contra o código.
- Demonstração com dados reais de terceiro: faixa "Demonstração" visível mesmo sem JS; use só noindex (sem `Disallow` no robots.txt, que impede o robô de ler o noindex).
- Deploy no Windows: variáveis com sintaxe do PowerShell (`$env:VAR="x"; npm run ...`); passos que regravam arquivos (testes, dev) antes do ajuste final; `wrangler secret`/`deploy` sempre na pasta do projeto certo (ou `--name`), conferindo com `--dry-run`, para não sobrescrever outro site.
