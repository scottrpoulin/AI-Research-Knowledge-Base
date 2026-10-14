# Code repos

Each repo is a **shallow git submodule** pinned to the commit that was current
when it was added. Fetch them after cloning this knowledge base with:

```bash
git submodule update --init --depth 1
```

To bump one to its latest upstream commit:

```bash
git submodule update --remote --depth 1 repos/<category>/<name>
```

## paper-code — official code for papers in `papers/`

| Repo | Paper | Upstream |
|---|---|---|
| `paper-code/dream-rsi` | Dream-RSI: Recursive Self-Improvement through Evolving Worlds — `papers/non-arxiv/dream-rsi.pdf` | [zhengkid/Dream-RSI](https://github.com/zhengkid/Dream-RSI) |
| `paper-code/skill2env` | Skill2Env: Reinforcing Agents with Collective Skills — `papers/non-arxiv/skill2env.pdf` | [NVlabs/Skill2Env](https://github.com/NVlabs/Skill2Env) |
| `paper-code/kimi-k3` | Kimi K3 Technical Report — `papers/non-arxiv/kimi-k3-tech-report.pdf` | [MoonshotAI/Kimi-K3](https://github.com/MoonshotAI/Kimi-K3) |
| `paper-code/2608.12875-embedders-dilemma` | The Embedder's Dilemma: LLMs Are Better, but at What Cost? — `papers/2608.12875_the-embedders-dilemma-llms-are-better-but-at-what-cost.pdf` | [embeddings-benchmark/embedders-dilemma](https://github.com/embeddings-benchmark/embedders-dilemma) |
| `paper-code/2609.04852-kvmem` | KVMem: Virtualizing Million-Token Agent Workspaces on a Consumer GPU — `papers/2609.04852_kvmem-virtualizing-million-token-agent-workspaces-on-a-consumer-gpu.pdf` | [kvmem/kvmem-qw3](https://github.com/kvmem/kvmem-qw3) |
| `paper-code/2609.08944-skilladam` | SkillAdam: Stable and Efficient Skill Evolution for Agents — `papers/2609.08944_skilladam-stable-and-efficient-skill-evolution-for-agents.pdf` | [ruc-datalab/SkillAdam](https://github.com/ruc-datalab/SkillAdam) |
| `paper-code/2609.11677-ecdysis` | Ecdysis: Efficient and Effective Training of Runtime Harnesses for LLM Agents — `papers/2609.11677_ecdysis-efficient-and-effective-training-of-runtime-harnesses-for-llm-agents.pdf` | [cuiyu-ai/Ecdysis](https://github.com/cuiyu-ai/Ecdysis) |
| `paper-code/2609.14857-modularrsi` | ModularRSI: Modular and Generalizable Recursive Harness Self-Improvement — `papers/2609.14857_modularrsi-modular-and-generalizable-recursive-harness-self-improvement.pdf` | [IQuestLab/ModularRSI](https://github.com/IQuestLab/ModularRSI) |
| `paper-code/2609.15396-skilllift` | SkillLift: Learning Dense Rubrics from Sparse Oracles for Efficient Skill Evolution — `papers/2609.15396_skilllift-learning-dense-rubrics-from-sparse-oracles-for-efficient-skill-evoluti.pdf` | [WalteR-MittY-pro/SkillLift](https://github.com/WalteR-MittY-pro/SkillLift) |
| `paper-code/2609.15779-evoontology` | EvoOntology: A Self-Evolving Ontology Layer for Data Agents — `papers/2609.15779_evoontology-a-self-evolving-ontology-layer-for-data-agents.pdf` | [ruc-datalab/EvoOntology](https://github.com/ruc-datalab/EvoOntology) |
| `paper-code/2609.17699-nemo-data-designer` | NeMo Data Designer: An Extensible Framework for Multimodal Synthetic Data Generation — `papers/2609.17699_nemo-data-designer-an-extensible-framework-for-multimodal-synthetic-data-generat.pdf` | [NVIDIA-NeMo/DataDesigner](https://github.com/NVIDIA-NeMo/DataDesigner) |
| `paper-code/2609.23986-jev-mem` | Jev-Mem: System-One-Controlled Agentic Memory for Efficient AI Agents — `papers/2609.23986_jev-mem-system-one-controlled-agentic-memory-for-efficient-ai-agents.pdf` | [libingzheren/Jev-Mem](https://github.com/libingzheren/Jev-Mem) |
| `paper-code/2609.24972-rrsi` | RRSI: Regularized Recursive Self-Improvement of Agent Harnesses — `papers/2609.24972_rrsi-regularized-recursive-self-improvement-of-agent-harnesses.pdf` | [google-research/rrsi](https://github.com/google-research/rrsi) |
| `paper-code/2609.24974-harness-zero` | Harness-Zero: Harness Distillation via Agent-as-Harness — `papers/2609.24974_harness-zero-harness-distillation-via-agent-as-harness.pdf` | [metaevo-ai/harness-zero](https://github.com/metaevo-ai/harness-zero) |
| `paper-code/2609.33439-raven` | Raven: The Harness of Harnesses for Composable Agentic Intelligence — `papers/2609.33439_raven-the-harness-of-harnesses-for-composable-agentic-intelligence.pdf` | [EverMind-AI/Raven](https://github.com/EverMind-AI/Raven) |
| `paper-code/2609.37725-context-language-models` | Context Language Models — `papers/2609.37725_context-language-models.pdf` | [facebookresearch/context-language-models](https://github.com/facebookresearch/context-language-models) |

Related repos cited by papers but not their own code (not vendored):
- [THUDM/slime](https://github.com/THUDM/slime) — RL post-training framework FrogNano (2609.07925) is trained with
- [theseus-labs-rsi/awesome-rsi](https://github.com/theseus-labs-rsi/awesome-rsi) — RSI reading list from *The Last AI Built by Humans* (2609.11873)

## agent-harness — skill/rule layers for coding agents

| Repo | What it is | Upstream |
|---|---|---|
| `agent-harness/autoharness` | Self-learning skill layer for Claude Code: distills skills from real sessions, updates and prunes them | [tigerless-labs/autoharness](https://github.com/tigerless-labs/autoharness) |
| `agent-harness/abide` | Makes a coding agent follow all of a project's rules | [coldteadotai/abide](https://github.com/coldteadotai/abide) |

## agent-research — agents that research and analyze

| Repo | What it is | Upstream |
|---|---|---|
| `agent-research/hyperresearch` | Agent-driven research knowledge base: collect, search and synthesize web research into a persistent wiki | [jordan-gibbs/hyperresearch](https://github.com/jordan-gibbs/hyperresearch) |
| `agent-research/rea` | Reverse engineer anything with agents, from app behavior down to native binaries | [morluto/rea](https://github.com/morluto/rea) |

## efficient-inference — running huge models on small hardware

| Repo | What it is | Upstream |
|---|---|---|
| `efficient-inference/airllm` | Large-model inference on a single 4GB GPU via layer-wise loading | [lyogavin/airllm](https://github.com/lyogavin/airllm) |
| `efficient-inference/kimi-k3-in-c` | 2.78T-param Kimi K3 inference on one CPU in 8.24 GB RAM, portable C99 | [FareedKhan-dev/kimi-k3-in-c](https://github.com/FareedKhan-dev/kimi-k3-in-c) |

## models-and-world-models — training from scratch and world models

| Repo | What it is | Upstream |
|---|---|---|
| `models-and-world-models/mini-agi` | Continual-learning model trained from scratch on an 8GB-VRAM laptop with a batch-1 data stream | [volotat/mini-AGI](https://github.com/volotat/mini-AGI) |
| `models-and-world-models/utopia` | Open-source enterprise world model | [deeplethe/utopia](https://github.com/deeplethe/utopia) |
