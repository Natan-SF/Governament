# Governament

**A society of AI agents that plans, votes on and delivers complex projects, with a human reviewer in charge of every key decision.**

Governament runs on [Claude Code](https://docs.claude.com/en/docs/claude-code). The main Claude Code session acts as the **Governor**. It hires specialist subagents, splits work into phases, holds votes between specialists, tracks a token budget and keeps an append-only decision log. You are the **Reviewer**: nothing important happens without your approval.

> The society's rules, records and agent prompts are written in **Portuguese (pt-BR)**. This README is in English.

---

## Table of contents

- [How it works](#how-it-works)
- [Features](#features)
- [Repository structure](#repository-structure)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Token economy](#token-economy)
- [What goes into git](#what-goes-into-git)
- [Safety and approvals](#safety-and-approvals)
- [Contributing](#contributing)

---

## How it works

```
            Reviewer (you)
     approves hires, plans, budget,
     irreversible actions, deliveries
                  │
                  ▼
     ┌───────────────────────────┐
     │  Governor (Claude Code)   │  plans · delegates · runs votes
     │                           │  keeps the board, log, budget
     └─────────────┬─────────────┘
                   │  calls one specialist at a time
      ┌────────────┼──────────────┐
      ▼            ▼              ▼
   critic      researcher    data analyst ...
 (read-only)  (web search)   (scripts, files)
```

1. **You give an order** with `/ordem <what you want>`.
2. **The Governor proposes** a project name, a phased plan with a "done when" for each phase, the specialists to hire and a token budget. Then it **stops and waits** for your approval.
3. **Specialists are hired or reused** as Claude Code subagents. Each one has a contract in `.claude/agents/<name>.md` that sets its role, rules, tools and model.
4. **The plan goes to a vote.** The critic and the specialists whose area is affected vote. You make the final call.
5. **The work runs in short stages.** Specialists never talk to each other. Everything goes through the Governor and is written to the records.
6. **The delivery comes back to you** for approval.

## Features

- **Human in the loop.** Hiring, plans, budget increases, `git push`, installs, sending messages and final deliveries all need your explicit "approved".
- **Contracts per role.** Each specialist has its own model and tool allow-list, and is reused across projects.
- **Voting.** The critic and the affected specialists vote on the plan and on changes of course.
- **Append-only decision log.** Every decision is saved with who made it and why. Old lines are never rewritten.
- **Task board and token budget.** These are kept up to date on every step, with an alert at 80% of a project's budget.
- **Memory.** Lessons learned are shared by all projects (`sociedade/memoria/`), and each project has its own memory file (`projetos/<project>/memoria.md`).
- **Permanent core team.** A `critico` (critic) and a `pesquisador` (researcher) serve every project. Other specialists are hired per project.

## Repository structure

| Path | Contents |
|---|---|
| `CLAUDE.md` | The constitution: roles and Governor rules (loaded by Claude Code automatically) |
| `.claude/agents/` | Active specialists (subagent contracts) |
| `.claude/commands/` | Slash commands: `/ordem`, `/status`, `/votacao` |
| `.claude/settings.json` | Project permissions (asks before `git push`, blocks reading `.env`) |
| `sociedade/protocolos/` | How to hire, vote, approve, budget, report and save tokens |
| `sociedade/modelos/` | Templates for agent contracts, votes, project memory and empty records |
| `sociedade/registro/` | Task board, decision log, hiring log, budget (local only) |
| `sociedade/votacoes/` | One file per vote (local only) |
| `sociedade/memoria/` | Lessons that apply to all projects |
| `sociedade/arquivo/agentes/` | Contracts of dismissed specialists (local only) |
| `projetos/<project>/` | Each project's memory, code and deliveries (local only) |

## Requirements

- [Claude Code](https://docs.claude.com/en/docs/claude-code) (CLI, desktop app or IDE extension) with an Anthropic account or API key.
- [Git](https://git-scm.com/).

## Installation

### 1. Install Claude Code

macOS, Linux or WSL:

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

Windows (PowerShell):

```powershell
irm https://claude.ai/install.ps1 | iex
```

Or with npm (Node.js 18+):

```bash
npm install -g @anthropic-ai/claude-code
```

See the [official setup guide](https://docs.claude.com/en/docs/claude-code/setup) for other options.

### 2. Clone the repository

```bash
git clone https://github.com/Natan-SF/Governament.git
cd Governament
```

### 3. Start the Governor

Open Claude Code in the repository folder:

```bash
claude
```

Claude Code reads `CLAUDE.md`, the agents in `.claude/agents/` and the commands in `.claude/commands/` automatically, so no extra setup is needed. On first run, log in when asked.

### 4. Check that it works

Inside Claude Code, run:

```
/status
```

The Governor should answer in Portuguese with what is waiting for your approval, the tasks in progress, the active specialists and the budget.

## Usage

| Command | What it does |
|---|---|
| `/ordem <text>` | Give a new order. The Governor proposes a plan, hires and a budget, then waits for your approval. |
| `/status` | Show pending approvals, tasks in progress, active specialists, budget and the latest decisions. |
| `/votacao <topic>` | Open a vote among the active specialists on a topic. |

Example:

```
/ordem Research the 10 largest logistics companies in Brazil and give me a comparison spreadsheet
```

Reply `aprovado` (approved) when you agree with the proposal, or ask for changes. You can also talk to the Governor in plain language at any time.

> Tip: the Governor speaks Portuguese, as the constitution requires. To run the society in another language, edit rule 8 in `CLAUDE.md` and the protocols in `sociedade/protocolos/`.

## Token economy

The society keeps output quality high and spends tokens only where quality is gained. This comes from **how the work is organised**, not from hard caps:

- **Briefings, not exploration.** Every task sent to a specialist names the exact files to read and touch and a verifiable "done when". Specialists use search and partial reads instead of rereading the whole project.
- **Stages, not marathons.** A specialist's whole context is resent on every action, so long calls get more expensive per step. Big tasks are split into stages of up to ~40 actions, each with a progress file the next stage reads.
- **Reviews on the diff.** The critic and the security reviewer look at what changed, not at the whole codebase.
- **Lean votes.** Votes happen on the plan and on real changes of course. Only the critic and the specialists whose area is affected vote, and they read a self-contained briefing of about 40 lines. At final delivery the critic's review replaces a vote.
- **Short deliveries.** Specialists answer in about 200 words and put long reports in files, so the Governor's context stays small.
- **Cheap bookkeeping.** Records are appended from the shell and read with `tail`/`grep`. The budget is split into a short summary and an append-only ledger. The task board only shows live tasks.
- **Generic contracts.** Contracts describe a role and are reused across projects. Project rules live in each project's memory file.
- **The Governor fixes small things itself** instead of calling a specialist who would reread the code.

Details: `sociedade/protocolos/registro.md` (section "Economia"), `votacao.md` and `orcamento.md`.

## What goes into git

Only the **structure** of the society is versioned: the constitution, protocols, templates, commands, agent contracts, shared memory and this README. Projects (`projetos/`), records (`sociedade/registro/`), votes (`sociedade/votacoes/`) and archived contracts stay on your machine and are listed in `.gitignore`.

On a fresh clone, copy the empty records from `sociedade/modelos/registro/` to `sociedade/registro/` (the Governor does this if the folder is empty).

## Safety and approvals

The Governor stops and waits for your approval before it:

- hires or dismisses a specialist;
- starts a plan or changes course;
- runs `git push`, deploys, sends e-mails or messages, shares files or installs software;
- spends money or raises a budget, and when a project reaches 80% of its budget;
- makes a final delivery.

`.claude/settings.json` also asks before `git push` from the Bash tool and blocks reading `.env` files. Specialists only get the tools listed in their contract. For example, the critic is read-only.

## Contributing

1. Fork the repository and create a branch.
2. Keep the society's files in Portuguese and follow the protocols in `sociedade/protocolos/`.
3. Never commit anything from `projetos/`, `sociedade/registro/` or `sociedade/votacoes/`.
4. Open a pull request describing what changed and why.
