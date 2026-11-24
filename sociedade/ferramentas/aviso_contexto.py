#!/usr/bin/env python3
"""Aviso de contexto da Sociedade Artificial (hook do Claude Code).

Roda depois de cada ferramenta e a cada mensagem do Revisor. Lê o fim do
transcrito, vê o tamanho atual do contexto e avisa quando passa dos limites:

- Governador: avisa o Revisor e o próprio governador em LIMITE_GOVERNADOR.
- Especialista: em AVISO_ESPECIALISTA manda fechar o passo e entregar; em
  PARADA_ESPECIALISTA manda parar e entregar como PARCIAL.

É a "etapa por contexto": o que encarece uma chamada é o contexto relido a cada
ação, não o número de turnos. O aviso chega antes do corte por maxTurns, então o
especialista sempre grava o andamento e entrega.

Nunca falha nem bloqueia: qualquer erro sai em silêncio com código 0.
Limites em tokens; mude aqui.
"""
import json
import os
import re
import sys
import tempfile

LIMITE_GOVERNADOR = 500_000
REPETIR_GOVERNADOR = 50_000      # avisa de novo a cada tanto acima do limite
AVISO_ESPECIALISTA = 100_000
PARADA_ESPECIALISTA = 150_000
REPETIR_ESPECIALISTA = 25_000    # insiste a cada tanto acima da parada
CAUDA = 2_000_000                # bytes lidos do fim do transcrito


def contexto_atual(caminho):
    """Tamanho do contexto na última resposta do modelo (0 se não achar)."""
    tam = os.path.getsize(caminho)
    with open(caminho, "rb") as f:
        if tam > CAUDA:
            f.seek(tam - CAUDA)
            f.readline()
        linhas = f.read().decode("utf-8", errors="replace").splitlines()
    for linha in reversed(linhas):
        if '"usage"' not in linha:
            continue
        try:
            o = json.loads(linha)
        except Exception:
            continue
        u = (o.get("message") or {}).get("usage")
        if o.get("type") == "assistant" and u:
            return ((u.get("input_tokens") or 0) + (u.get("cache_creation_input_tokens") or 0)
                    + (u.get("cache_read_input_tokens") or 0) + (u.get("output_tokens") or 0))
    return 0


def nivel(ctx, especialista):
    if especialista:
        if ctx >= PARADA_ESPECIALISTA:
            return 2 + (ctx - PARADA_ESPECIALISTA) // REPETIR_ESPECIALISTA
        return 1 if ctx >= AVISO_ESPECIALISTA else 0
    if ctx >= LIMITE_GOVERNADOR:
        return 1 + (ctx - LIMITE_GOVERNADOR) // REPETIR_GOVERNADOR
    return 0


def main():
    dados = json.load(sys.stdin)
    evento = dados.get("hook_event_name") or "PostToolUse"
    sessao = dados.get("session_id") or ""
    agente = dados.get("agent_id")
    principal = dados.get("transcript_path") or ""
    if not principal or not sessao:
        return
    if agente:
        nome = f"agent-{agente}.jsonl"
        caminho = os.path.join(os.path.dirname(principal), sessao, "subagents", nome)
        if not os.path.isfile(caminho):
            # o hook pode receber o transcrito do próprio especialista
            caminho = principal if os.path.basename(principal) == nome else ""
    else:
        caminho = principal
    if not caminho or not os.path.isfile(caminho):
        return
    ctx = contexto_atual(caminho)
    n = nivel(ctx, bool(agente))

    # só fala quando sobe de nível, para não repetir a cada ação
    pasta = os.path.join(tempfile.gettempdir(), "sociedade-aviso-contexto")
    os.makedirs(pasta, exist_ok=True)
    marca = os.path.join(pasta, re.sub(r"[^A-Za-z0-9_-]", "", f"{sessao}-{agente or 'governador'}") + ".txt")
    anterior = 0
    try:
        with open(marca, encoding="utf-8") as f:
            anterior = int(f.read().strip() or 0)
    except Exception:
        pass
    if n < anterior:                 # contexto diminuiu (compactação ou /clear): rearma
        with open(marca, "w", encoding="utf-8") as f:
            f.write(str(n))
        return
    if n == 0 or n == anterior:
        return
    with open(marca, "w", encoding="utf-8") as f:
        f.write(str(n))

    mil = f"{ctx // 1000} mil"
    saida = {}
    if agente:
        if n == 1:
            texto = (f"CONTEXTO: seu contexto chegou a {mil} tokens e cada ação agora relê tudo isso. "
                     "Termine o passo em que está, grave o andamento no arquivo do briefing e entregue: "
                     "CONCLUÍDA se acabou a tarefa, PARCIAL se não (diga o que falta). Não comece passo novo.")
        else:
            texto = (f"CONTEXTO: {mil} tokens, acima do limite da etapa. Pare agora: grave o andamento "
                     "(feito, falta, arquivos tocados, comandos de teste) e entregue como PARCIAL. "
                     "O governador continua numa chamada nova a partir do arquivo de andamento.")
    else:
        texto = (f"CONTEXTO DO GOVERNADOR: {mil} tokens (aviso em {LIMITE_GOVERNADOR // 1000} mil). "
                 "Diga isso ao Revisor em uma frase na próxima resposta e proponha fechar a etapa: "
                 "atualizar a memória do projeto e os registros e continuar em sessão nova (/clear).")
        saida["systemMessage"] = (f"Sociedade: o contexto do governador está em {mil} tokens "
                                  f"(aviso em {LIMITE_GOVERNADOR // 1000} mil). Vale fechar a etapa e abrir sessão nova.")
    saida["hookSpecificOutput"] = {"hookEventName": evento, "additionalContext": texto}
    sys.stdout.write(json.dumps(saida, ensure_ascii=True))


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
    sys.exit(0)
