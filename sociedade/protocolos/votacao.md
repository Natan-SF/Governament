# Protocolo de votação

A votação mostra ao Revisor quem concorda ou discorda do rumo do projeto e quais falhas cada um enxerga. **O voto é consultivo: quem decide é o Revisor.**

## Quando votar

- Antes de aprovar o plano de um projeto.
- Antes de cada fase de execução e antes da entrega final.
- Sempre que surgir uma mudança de rumo importante.
- Quando o Revisor pedir (`/votacao <tema>`).

Só votam os especialistas **ativos no projeto**. Sem especialistas contratados não há votação; o governador avisa o Revisor.

## Como conduzir

1. Crie `sociedade/votacoes/V-<NNN>-<tema-curto>.md` a partir de `sociedade/modelos/votacao.md`. Descreva a proposta e liste os arquivos que os votantes devem ler.
2. Chame cada especialista **separadamente**, sem mostrar o voto dos outros, para evitar efeito manada. O prompt deve dizer:
   - que é uma votação **somente leitura**: o especialista lê e avalia, mas não altera nenhum arquivo;
   - qual é a proposta e quais arquivos ler;
   - que a resposta deve vir no formato abaixo.
3. Se os especialistas forem independentes, chame-os em paralelo.
4. Anote cada voto no arquivo da votação e faça a contagem.
5. Apresente o resultado ao Revisor: placar, os votos contrários com seus motivos e as falhas apontadas. Pergunte a decisão.
6. Registre a decisão do Revisor no arquivo da votação e em `sociedade/registro/decisoes.md`, com o placar.
7. Some os tokens das chamadas de voto ao orçamento do projeto: votar também custa.

## Formato do voto

```
Voto: A FAVOR | CONTRA | ABSTENÇÃO
Justificativa: (2 a 4 frases)
Falhas ou riscos que vejo: (lista; "nenhum" se não houver)
O que mudaria meu voto: (condição concreta)
```

Todo voto conta no placar como foi dado. Um voto CONTRA sem falha concreta continua sendo CONTRA, mas o governador o marca como "sem falha concreta" para o Revisor pesar. O governador não vota: ele faz a proposta.
