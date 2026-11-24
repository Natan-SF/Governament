#!/usr/bin/env python3
"""Git local por projeto, para o critico revisar um diff de verdade.

Cada projeto ganha um repositório git só dele, dentro de projetos/<projeto>/.
Ele nunca é enviado a lugar nenhum (não tem remoto) e a pasta projetos/ já é
ignorada pelo git da sociedade.

Uso (na raiz da sociedade):
    python sociedade/ferramentas/projeto_git.py marco <projeto> "<mensagem>"
        Fotografa o estado atual (cria o repositório na primeira vez).
        Faça um marco ao fechar cada etapa aprovada.
    python sociedade/ferramentas/projeto_git.py diff <projeto> <saida> [--desde REF] [--so CAMINHO ...]
        Grava em <saida> (ex.: revisoes/T-070.diff, relativo ao projeto) tudo o
        que mudou desde o último marco e mostra o tamanho. O critico lê só esse arquivo.
    python sociedade/ferramentas/projeto_git.py marcos <projeto>
        Lista os marcos.

Ficam fora do repositório: dependências, saídas de build, segredos (.env),
os próprios arquivos .diff e qualquer arquivo com mais de 1 MB.
"""
import argparse
import os
import subprocess
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LIMITE_ARQUIVO = 1_000_000
ARVORE_VAZIA = "4b825dc642cb6eb9a060e54bf8d69288fbee4904"
PASTAS_FORA = {"node_modules", ".wrangler", "dist", "build", ".venv", "venv", "__pycache__",
               ".cache", ".next", ".git"}
PADROES_FORA = ["node_modules/", ".wrangler/", "dist/", "build/", ".venv/", "venv/", "__pycache__/",
                ".cache/", ".next/", "*.pyc", ".env", ".env.*", ".dev.vars", "*.diff", "*.log"]
AVISO_DIFF = 60_000   # bytes; acima disso vale dividir a revisão


def pasta(projeto):
    p = os.path.join(RAIZ, "projetos", projeto)
    if not os.path.isdir(p):
        sys.exit(f"Projeto não encontrado: projetos/{projeto}")
    return p


def git(dirp, *args, texto=True, checar=True):
    base = ["git", "-C", dirp, "-c", "core.autocrlf=false", "-c", "core.safecrlf=false",
            "-c", "core.quotepath=false", "-c", "user.name=Sociedade Artificial",
            "-c", "user.email=sociedade@localhost"]
    r = subprocess.run(base + list(args), capture_output=True)
    if checar and r.returncode != 0:
        sys.exit(f"git {' '.join(args)} falhou: {r.stderr.decode('utf-8', 'replace').strip()}")
    return r.stdout.decode("utf-8", "replace") if texto else r.stdout


def preparar(dirp):
    """Cria o repositório se faltar e atualiza a lista do que fica de fora."""
    if not os.path.isdir(os.path.join(dirp, ".git")):
        git(dirp, "init", "-q")
    grandes = []
    for atual, pastas, arquivos in os.walk(dirp):
        pastas[:] = [d for d in pastas if d not in PASTAS_FORA]
        for a in arquivos:
            c = os.path.join(atual, a)
            try:
                if os.path.getsize(c) > LIMITE_ARQUIVO:
                    grandes.append("/" + os.path.relpath(c, dirp).replace(os.sep, "/"))
            except OSError:
                pass
    exclude = os.path.join(dirp, ".git", "info", "exclude")
    os.makedirs(os.path.dirname(exclude), exist_ok=True)
    with open(exclude, "w", encoding="utf-8", newline="\n") as f:
        f.write("# Gerado por sociedade/ferramentas/projeto_git.py\n")
        f.write("\n".join(PADROES_FORA) + "\n")
        f.write("# arquivos com mais de 1 MB\n")
        f.write("\n".join(sorted(grandes)) + ("\n" if grandes else ""))
    git(dirp, "add", "-A")
    return len(grandes)


def tem_marco(dirp):
    return subprocess.run(["git", "-C", dirp, "rev-parse", "--verify", "-q", "HEAD"],
                          capture_output=True).returncode == 0


def cmd_marco(args):
    dirp = pasta(args.projeto)
    fora = preparar(dirp)
    if tem_marco(dirp) and not git(dirp, "status", "--porcelain").strip():
        print("Nada mudou desde o último marco:", git(dirp, "log", "-1", "--format=%h %s").strip())
        return
    git(dirp, "commit", "-q", "-m", args.mensagem)
    print("Marco criado:", git(dirp, "log", "-1", "--format=%h %s").strip(),
          f"({fora} arquivos grandes fora do repositório)" if fora else "")


def cmd_diff(args):
    dirp = pasta(args.projeto)
    preparar(dirp)
    ref = args.desde or ("HEAD" if tem_marco(dirp) else ARVORE_VAZIA)
    so = (["--"] + args.so) if args.so else []
    resumo = git(dirp, "diff", "--cached", "--stat", ref, *so)
    corpo = git(dirp, "diff", "--cached", ref, *so, texto=False)
    if not corpo.strip():
        print("Sem mudanças desde", ref)
        return
    saida = os.path.join(dirp, args.saida)
    os.makedirs(os.path.dirname(saida) or dirp, exist_ok=True)
    marco = git(dirp, "log", "-1", "--format=%h %s", checar=False).strip() or "(nenhum marco: projeto inteiro)"
    with open(saida, "wb") as f:
        f.write(f"# Diff de projetos/{args.projeto} desde o marco: {marco}\n".encode("utf-8"))
        f.write(resumo.encode("utf-8"))
        f.write(b"\n")
        f.write(corpo)
    tam = os.path.getsize(saida)
    print(resumo.strip().splitlines()[-1].strip())
    print(f"Gravado em projetos/{args.projeto}/{args.saida} ({tam // 1000} KB, ~{tam // 4000} mil tokens)")
    if tam > AVISO_DIFF:
        print("Diff grande: divida a revisão por pasta com --so <caminho>, um arquivo de diff por parte.")


def cmd_marcos(args):
    dirp = pasta(args.projeto)
    if not os.path.isdir(os.path.join(dirp, ".git")) or not tem_marco(dirp):
        print("Nenhum marco ainda.")
        return
    print(git(dirp, "log", "--format=%h %ad %s", "--date=short").strip())


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser(description="Git local por projeto (marcos e diffs para revisão).")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("marco")
    p.add_argument("projeto")
    p.add_argument("mensagem")
    p.set_defaults(f=cmd_marco)
    p = sub.add_parser("diff")
    p.add_argument("projeto")
    p.add_argument("saida", help="arquivo de saída, relativo à pasta do projeto")
    p.add_argument("--desde", help="marco de referência (padrão: o último)")
    p.add_argument("--so", nargs="+", help="limitar a estes caminhos")
    p.set_defaults(f=cmd_diff)
    p = sub.add_parser("marcos")
    p.add_argument("projeto")
    p.set_defaults(f=cmd_marcos)
    args = ap.parse_args()
    args.f(args)


if __name__ == "__main__":
    main()
