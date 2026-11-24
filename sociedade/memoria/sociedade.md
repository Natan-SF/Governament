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

## Economia (medido nos transcritos, 2026-11)
- O "total de tokens" que um subagente informa é o tamanho do contexto no fim, não o consumo. Meça com `sociedade/ferramentas/medidor.py` (TE). O real foi dezenas de vezes maior que o lançado até 2026-11-13.
- O governador é ~40% do consumo: 78 mil tokens fixos por rodada, média de 168 mil. Sessão nova a cada fase; registros num só comando; trabalho direto só até ~5 ações.
- Voto e ponto cego custam 30 a 50 mil TE: é o item mais barato e o que pega cedo o erro caro. Não economize aí.
- Revisão se faz sobre o diff do git local do projeto (`projeto_git.py`), a cada fase.
- Estimativas saem 2 a 3 vezes abaixo do real. Dimensione pelo gasto real de tarefas parecidas em `orcamento-lancamentos.md`.
- Quatro chamadas de 96 a 175 rodadas foram 62% do consumo dos especialistas: o custo cresce com o quadrado do tamanho. A etapa se corta pelo contexto (aviso aos 100 mil, parada aos 150 mil), não por turnos; PARCIAL com andamento continua em chamada nova.
- Correções pequenas e localizadas o governador faz direto (D-136).
- Copiar e adaptar um projeto parecido sai muito mais barato que escrever do zero.
- Contrato e memória do projeto são lidos a cada ação: mantenha os dois curtos.

## Lições técnicas
- Downloads e processamentos longos: o governador roda em segundo plano; o especialista só escreve e testa o script.
- Verificações automáticas podem passar com resultado errado. Sempre uma conferência independente e uma amostra contra fonte externa.
- Especialista recém-contratado ou contrato alterado costuma só valer depois de reabrir o Claude Code (às vezes aparece após a próxima notificação). Mudança de `maxTurns` só vale depois de reabrir.
- Especialista pode travar ou entregar PARCIAL no meio. Exija andamento em arquivo e continue numa chamada nova a partir dele (SendMessage só se travou sem gravar o andamento; `registro.md`, "Etapas por contexto"); antes, encerre os processos que ele deixou abertos (servidor, navegador headless).
- Encerrar processos SÓ filtrando pelo nome do executável (node, workerd, msedge) E pelo caminho do projeto na linha de comando. Filtro por número solto já derrubou o navegador do Revisor (D-133). Repita isso no briefing de toda tarefa que abre servidor ou navegador.
- Duas sessões podem escrever nos registros ao mesmo tempo: pegue o próximo número de T e D logo antes de gravar.
- WebFetch não lê alguns servidores de dados abertos (WebDAV); o governador confere com curl. Dê ao pesquisador tarefas com poucos pontos.
- Dados abertos de CNPJ da Receita: o caminho antigo dá 404; use o WebDAV público `https://arquivos.receitafederal.gov.br/public.php/dav/files/YggdBLfdninEJX9/AAAA-MM/` (aceita Range).
- Acervo de leis local (`C:/Users/natan/leis`): parte dos arquivos só está no git; leia com `git -C C:/Users/natan/leis show HEAD:<caminho>`. O advogado-artificial é agente pessoal do Revisor (fora da sociedade) e não grava arquivos: o governador salva o parecer.
- Textos legais (privacidade, prazos, direitos) só prometem o que o código faz: confira cada frase contra o código.
- Demonstração com dados reais de terceiro: faixa "Demonstração" visível mesmo sem JS; use só noindex (sem `Disallow` no robots.txt, que impede o robô de ler o noindex).
- Deploy no Windows: variáveis com sintaxe do PowerShell (`$env:VAR="x"; npm run ...`); passos que regravam arquivos (testes, dev) antes do ajuste final; `wrangler secret`/`deploy` sempre na pasta do projeto certo (ou `--name`), conferindo com `--dry-run`, para não sobrescrever outro site.
- O Revisor usa o GridCraft (open source), não o Excel. Planilhas: testar e salvar com `C:/Program Files/GridCraft/gridcraft-cli.exe` (`check` confere fórmulas e round trip; `run --out` grava os valores; `cat`, `eval`). Imagens em PNG (EMF não aparece). No `data.validate`, selecione a célula antes com `edit.goTo` (D-165).
- DWG: `C:/Program Files/CADCraft/cadcraft-cli.exe convert arquivo.dwg saida.dxf` converte sem abrir a janela (não rode `cadcraft.exe --help`: abre o programa). Planta de parcelamento pode não ter o polígono dos lotes: o quadro de áreas costuma estar numa planilha Excel embutida na folha (OLE2FRAME no DXF, grupo 310; o .xlsx está dentro, a partir de `PK`).
