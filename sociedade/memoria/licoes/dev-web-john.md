# Lições do cargo: dev-web-john

Falhas já apontadas em revisão. Não repita. Uma linha por lição; até 15.

- Texto que promete algo ao usuário (privacidade, prazos, direitos) só diz o que o código faz: confira cada frase contra o código, inclusive o prazo real de limpeza (prazo + intervalo da rotina).
- Estado de que o usuário precisa para continuar (código de reserva, confirmação) sobrevive a recarregar a página e a voltar de outro aplicativo: ponha na URL.
- Campo-armadilha contra robôs tem nome que o autocompletar não preenche, e a resposta falsa tem o mesmo formato da verdadeira.
- Telefone é normalizado no servidor (DDI, zero de operadora) e número inválido gera aviso no log; nunca falha calado.
- Ação que apaga dados de demonstração só funciona quando o sistema está marcado como exemplo.
- Cache de resposta que depende do relógio (horários livres, "hoje", antecedência) leva o momento na chave ou tem validade curta.
- Datas e horas saem pelo fuso do negócio, nunca pelo relógio do aparelho.
- Nome do negócio, faixa de demonstração e avisos vêm da configuração, não ficam fixos no código.
- A API recusa entrada repetida ou fora do passo com o erro certo, não com um erro genérico de outro caso.
- Passo que regrava arquivos gerados (testes, dev) roda antes do ajuste final de publicação; confira o arquivo gerado antes do deploy.
- README e comentários de cabeçalho são atualizados na mesma etapa em que o código muda.
- Diga na entrega o que não testou (ex.: aparelho real, navegador específico) em vez de deixar implícito.
