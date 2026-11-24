#!/usr/bin/env python3
"""Medidor de consumo da Sociedade Artificial.

Lê os transcritos do Claude Code (não gasta tokens de modelo) e mede o consumo
real de cada chamada de especialista e de cada sessão do governador.

Unidade: TE (tokens equivalentes), que pesa cada tipo de token pelo que custa
em relação a um token de entrada:

    TE = entrada nova + 1,25 x escrita de cache (5 min) + 2 x escrita de cache (1 h)
         + 0,1 x leitura de cache + 5 x saída

O número antigo ("tokens" que o resultado do subagente informa) é só o tamanho
do contexto no fim da chamada. Ele não mede o consumo: cada ação relê o contexto
inteiro, então uma chamada longa consome dezenas de vezes mais do que esse número.

Uso (na raiz da sociedade):
    python sociedade/ferramentas/medidor.py lancar [--projeto NOME]
        Acrescenta em orcamento-lancamentos.md tudo o que ainda não foi lançado
        e mostra o total por projeto. Rode uma vez por etapa.
    python sociedade/ferramentas/medidor.py resumo [--sessao ID]
        Mostra o consumo por sessão e por chamada. Não grava nada.
    python sociedade/ferramentas/medidor.py retroativo
        Soma por projeto tudo o que há nos transcritos. Não grava nada.
    python sociedade/ferramentas/medidor.py marcar [--menos-sessao ID]
        Marca tudo como já lançado, sem lançar (uso único, na troca do medidor).

Os transcritos são apagados pelo Claude Code depois de `cleanupPeriodDays`
(30 dias por padrão): lance dentro desse prazo.
"""
import argparse
import collections
import datetime
import glob
import json
import os
import re
import sys

PESO_ENTRADA = 1.0
PESO_ESCRITA_5M = 1.25
PESO_ESCRITA_1H = 2.0
PESO_LEITURA = 0.1
PESO_SAIDA = 5.0

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
REGISTRO = os.path.join(RAIZ, "sociedade", "registro")
LANCAMENTOS = os.path.join(REGISTRO, "orcamento-lancamentos.md")
ESTADO = os.path.join(REGISTRO, "medidor-estado.json")
PROJETOS = os.path.join(RAIZ, "projetos")
VOTACOES = os.path.join(RAIZ, "sociedade", "votacoes")


def pastas_transcritos():
    """Pastas de transcritos da sociedade: a da raiz e as de sessões abertas em subpastas.

    Devolve pares (pasta, projeto): o projeto vem do nome da pasta quando a sessão
    foi aberta dentro de projetos/<projeto>/.
    """
    base = os.environ.get("CLAUDE_CONFIG_DIR") or os.path.join(os.path.expanduser("~"), ".claude")
    raiz = re.sub(r"[^A-Za-z0-9]", "-", RAIZ)
    pares = []
    for d in sorted(glob.glob(os.path.join(base, "projects", raiz + "*"))):
        resto = os.path.basename(d)[len(raiz):]
        if resto and not resto.startswith("-"):
            continue                      # outra pasta que só começa com o mesmo nome
        projeto = None
        if resto.startswith("-projetos-"):
            sub = resto[len("-projetos-"):]
            for p in projetos_conhecidos():
                if sub == p or sub.startswith(p + "-"):
                    projeto = p
                    break
        pares.append((d, projeto))
    return pares


def fmt(n):
    return f"{int(round(n)):,}".replace(",", ".")


def projetos_conhecidos():
    if not os.path.isdir(PROJETOS):
        return []
    return sorted((d for d in os.listdir(PROJETOS) if os.path.isdir(os.path.join(PROJETOS, d))),
                  key=len, reverse=True)


def ler_rodadas(caminho):
    """Uma rodada = uma resposta do modelo. Devolve (rodadas, primeiro_prompt)."""
    por_id = collections.OrderedDict()
    prompt = None
    with open(caminho, encoding="utf-8", errors="replace") as f:
        for linha in f:
            try:
                o = json.loads(linha)
            except Exception:
                continue
            m = o.get("message") or {}
            if prompt is None and o.get("type") == "user":
                c = m.get("content")
                if isinstance(c, str):
                    prompt = c
                elif isinstance(c, list):
                    prompt = " ".join(b.get("text", "") for b in c if isinstance(b, dict) and b.get("type") == "text")
            if o.get("type") != "assistant":
                continue
            u, mid = m.get("usage"), m.get("id")
            if not u or not mid:
                continue
            r = por_id.setdefault(mid, {"texto": ""})
            cw = u.get("cache_creation_input_tokens") or 0
            det = u.get("cache_creation") or {}
            cw1h = det.get("ephemeral_1h_input_tokens") or 0
            cw5m = det.get("ephemeral_5m_input_tokens")
            if cw5m is None:
                cw5m = max(cw - cw1h, 0)
            r.update({
                "in": u.get("input_tokens") or 0, "cw5m": cw5m, "cw1h": cw1h,
                "cr": u.get("cache_read_input_tokens") or 0, "out": u.get("output_tokens") or 0,
                "modelo": (m.get("model") or "?").replace("claude-", ""), "quando": o.get("timestamp"),
            })
            for b in m.get("content") or []:
                if isinstance(b, dict) and b.get("type") == "tool_use":
                    r["texto"] += json.dumps(b.get("input", {}), ensure_ascii=False)
    return list(por_id.values()), (prompt or "")


def te(r):
    return (PESO_ENTRADA * r["in"] + PESO_ESCRITA_5M * r["cw5m"] + PESO_ESCRITA_1H * r["cw1h"]
            + PESO_LEITURA * r["cr"] + PESO_SAIDA * r["out"])


def somar(rodadas):
    s = {"rodadas": len(rodadas), "te": 0.0, "bruto": 0, "ctx_fim": 0, "modelo": "?", "data": "?"}
    for r in rodadas:
        s["te"] += te(r)
        s["bruto"] += r["in"] + r["cw5m"] + r["cw1h"] + r["cr"] + r["out"]
    if rodadas:
        u = rodadas[-1]
        s["ctx_fim"] = u["in"] + u["cw5m"] + u["cw1h"] + u["cr"] + u["out"]
        s["modelo"] = u["modelo"]
        s["data"] = data_local(u.get("quando"))
    return s


def data_local(iso):
    try:
        d = datetime.datetime.fromisoformat(iso.replace("Z", "+00:00"))
        return d.astimezone().strftime("%Y-%m-%d")
    except Exception:
        return datetime.date.today().isoformat()


def projeto_do_texto(texto, conhecidos):
    """Projeto mais citado no texto; None se nenhum."""
    cont = collections.Counter()
    for p in conhecidos:
        n = len(re.findall(r"(?<![a-z0-9-])" + re.escape(p) + r"(?![a-z0-9-])", texto))
        if n:
            cont[p] = n
    if cont:
        return cont.most_common(1)[0][0]
    m = re.search(r"(V-\d{3})[^\s\"'`]*\.md", texto)
    if m:
        for arq in glob.glob(os.path.join(VOTACOES, m.group(1) + "*.md")):
            try:
                with open(arq, encoding="utf-8") as f:
                    pm = re.search(r"^- Projeto:\s*(\S+)", f.read(), re.M)
                if pm:
                    return pm.group(1)
            except Exception:
                pass
    return None


def coletar(so_sessao=None):
    """Lista de itens medidos: sessões do governador e chamadas de especialista."""
    conhecidos = projetos_conhecidos()
    itens = []
    arquivos = [(p, base, proj) for base, proj in pastas_transcritos()
                for p in sorted(glob.glob(os.path.join(base, "*.jsonl")))]
    for p, base, da_pasta in arquivos:
        sid = os.path.basename(p)[:-6]
        if so_sessao and not sid.startswith(so_sessao):
            continue
        rodadas, _ = ler_rodadas(p)
        if rodadas:
            itens.append({"tipo": "sessao", "id": sid, "sessao": sid, "quem": "Governador",
                          "tarefa": "sessão " + sid[:8], "rodadas": rodadas, "conhecidos": conhecidos,
                          "da_pasta": da_pasta})
        for a in sorted(glob.glob(os.path.join(base, sid, "subagents", "agent-*.jsonl"))):
            aid = os.path.basename(a)[6:-6]
            rodadas, prompt = ler_rodadas(a)
            if not rodadas:
                continue
            meta = {}
            try:
                with open(a[:-6] + ".meta.json", encoding="utf-8") as f:
                    meta = json.load(f)
            except Exception:
                pass
            itens.append({"tipo": "agente", "id": aid, "sessao": sid,
                          "quem": meta.get("agentType") or "especialista?",
                          "tarefa": (meta.get("description") or prompt[:60]).replace("|", "/").strip(),
                          "rodadas": rodadas, "projeto": projeto_do_texto(prompt, conhecidos) or da_pasta})
    return itens


def carregar_estado():
    try:
        with open(ESTADO, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"agente": {}, "sessao": {}}


def gravar_estado(est):
    os.makedirs(REGISTRO, exist_ok=True)
    with open(ESTADO, "w", encoding="utf-8") as f:
        json.dump(est, f, ensure_ascii=False, indent=1)


def cmd_resumo(args):
    itens = coletar(args.sessao)
    if not itens:
        print("Nenhum transcrito em", [d for d, _ in pastas_transcritos()])
        return
    print("quem | tarefa | modelo | rodadas | contexto final | TE | bruto")
    tot = collections.Counter()
    for it in itens:
        s = somar(it["rodadas"])
        tot[it["quem"] if it["tipo"] == "sessao" else "Especialistas"] += s["te"]
        print(f"{it['quem']} | {it['tarefa'][:50]} | {s['modelo']} | {s['rodadas']} | "
              f"{fmt(s['ctx_fim'])} | {fmt(s['te'])} | {fmt(s['bruto'])}")
    print("--- totais em TE:", " · ".join(f"{k} {fmt(v)}" for k, v in tot.items()))


def cmd_retroativo(args):
    conhecidos = projetos_conhecidos()
    tot = collections.defaultdict(lambda: collections.Counter())
    for it in coletar():
        s = somar(it["rodadas"])
        if it["tipo"] == "agente":
            proj = it.get("projeto") or "(sem projeto)"
            tot[proj]["Especialistas"] += s["te"]
        else:
            proj = (it["da_pasta"] or projeto_do_texto(" ".join(r["texto"] for r in it["rodadas"]), conhecidos)
                    or "(sem projeto)")
            tot[proj]["Governador"] += s["te"]
    print("projeto | especialistas (TE) | governador (TE) | total (TE)")
    for proj in sorted(tot):
        e, g = tot[proj]["Especialistas"], tot[proj]["Governador"]
        print(f"{proj} | {fmt(e)} | {fmt(g)} | {fmt(e + g)}")
    print("Sessão do governador vai inteira para o projeto mais citado nela; é aproximação.")


def cmd_marcar(args):
    est = carregar_estado()
    n = 0
    for it in coletar():
        if args.menos_sessao and it["sessao"].startswith(args.menos_sessao):
            continue
        est[it["tipo"]][it["id"]] = len(it["rodadas"])
        n += 1
    gravar_estado(est)
    print(f"{n} itens marcados como já lançados em {os.path.relpath(ESTADO, RAIZ)}")


def cmd_lancar(args):
    est = carregar_estado()
    linhas, por_projeto = [], collections.Counter()
    for it in coletar():
        feitas = est[it["tipo"]].get(it["id"], 0)
        novas = it["rodadas"][feitas:]
        if not novas:
            continue
        s = somar(novas)
        if it["tipo"] == "agente":
            proj = it.get("projeto") or args.projeto or "Sociedade"
            rotulo = it["tarefa"] + (" (retomada)" if feitas else "")
        else:
            proj = (it["da_pasta"] or args.projeto
                    or projeto_do_texto(" ".join(r["texto"] for r in novas), it["conhecidos"]) or "Sociedade")
            rotulo = f"coordenação e trabalho direto, sessão {it['id'][:8]}"
        detalhe = f"{rotulo} ({s['rodadas']} rodadas, contexto final {fmt(s['ctx_fim'] / 1000)} mil, {s['modelo']})"
        linhas.append(f"| {s['data']} | {proj} | {it['quem']} | {detalhe} | {fmt(s['te'])} | medido (TE) |")
        por_projeto[proj] += s["te"]
        est[it["tipo"]][it["id"]] = len(it["rodadas"])
    if not linhas:
        print("Nada novo para lançar.")
        return
    if args.simular:
        print("\n".join(linhas))
        print("(simulação: nada foi gravado)")
        return
    with open(LANCAMENTOS, "a", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(linhas) + "\n")
    gravar_estado(est)
    print(f"{len(linhas)} lançamentos acrescentados (unidade: TE).")
    for proj, v in por_projeto.most_common():
        print(f"  {proj}: +{fmt(v)} TE")
    print("Some esses valores ao resumo em sociedade/registro/orcamento.md.")


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser(description="Medidor de consumo da Sociedade Artificial (unidade: TE).")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("lancar")
    p.add_argument("--projeto", help="projeto do governador e das chamadas sem projeto identificável")
    p.add_argument("--simular", action="store_true", help="mostra as linhas sem gravar")
    p.set_defaults(f=cmd_lancar)
    p = sub.add_parser("resumo")
    p.add_argument("--sessao", help="início do ID da sessão")
    p.set_defaults(f=cmd_resumo)
    p = sub.add_parser("retroativo")
    p.set_defaults(f=cmd_retroativo)
    p = sub.add_parser("marcar")
    p.add_argument("--menos-sessao", help="início do ID de uma sessão a deixar de fora")
    p.set_defaults(f=cmd_marcar)
    args = ap.parse_args()
    args.f(args)


if __name__ == "__main__":
    main()
