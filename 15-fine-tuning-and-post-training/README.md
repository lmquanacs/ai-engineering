# 15 · Fine-tuning & post-training

_Last updated: 2026-11-18_

> Adapting open-weight models: LoRA/QLoRA, preference tuning, RL with verifiable rewards, distillation and the data behind them. Lower priority unless you train models, but this is where open models get specialised.

## 🧭 Do you actually need to fine-tune?

| Your gap | Reach for |
|---|---|
| The model doesn't **know** your docs, products or policies | **RAG**: citations, instant updates, fewer hallucinated facts. → [Context engineering](../11-context-engineering-and-memory/README.md) |
| The model doesn't **behave** the way you need (format, style, tool-use habits, domain reasoning) | **Fine-tuning**: LoRA/QLoRA first, full fine-tuning rarely |
| The model needs to get **better at verifiable tasks** (code, math, tool calls) | **RL with verifiable rewards** (GRPO / RLVR) |
| You need a **small, cheap** model with frontier-like behaviour on one task | **Distillation** from a larger model |

Base models in 2026 handle many tasks out of the box that needed fine-tuning 18 months ago, so try prompting, skills and RAG first.
Sources: [Fine-tuning guide (Jose Nobile)](https://josenobile.pages.dev/guides/fine-tuning/) · [EVAL #003: fine-tuning in 2026](https://buttondown.com/ultradune/archive/eval-003-fine-tuning-in-2026-axolotl-vs-unsloth) · Added: 2026-11-18

## 🧰 Toolchain

| Tool | Role | Pick when |
|---|---|---|
| [**TRL**](https://github.com/huggingface/trl) (v1.0, 2026-03-31) | The canonical post-training library: SFT, DPO, GRPO and 75+ methods, plus a CLI and a stability contract | Full control, custom or verifier rewards, research |
| [**Unsloth**](https://github.com/unslothai/unsloth) | Custom kernels for single-GPU speed: about 2× faster with 70% less VRAM, and MoE up to 12× faster *(self-reported)*. Supports LoRA/QLoRA, full fine-tuning, RL and FP8, plus **Unsloth Studio**, a local web UI | Fast, cheap fine-tunes on one GPU |
| **Axolotl** | Config-driven wrapper over TRL; multi-GPU | Reproducible YAML recipes at team scale |
| **LLaMA-Factory** | Broad model coverage, a web UI, Megatron support | Many model families, GUI-first teams |
| **OpenRLHF / verl** | Large-scale RL (PPO, GRPO variants) used by open-weight labs | RL at cluster scale |

Sources: [Hugging Face: TRL v1.0](https://huggingface.co/blog/trl-v1) · [Unsloth on PyPI](https://pypi.org/project/unsloth/2026.8.1/) · [Open RLHF toolchain 2026](https://presenc.ai/research/open-rlhf-finetuning-toolchain-2026) · Added: 2026-11-18

## 📈 Trends

### Verifier rewards replace learned reward models for code, math and tools
TRL's v1.0 notes say that for math, code and tool use, rewards increasingly come from verifiers and deterministic checks rather than learned reward models. GRPO and RLVR are the fastest-growing methods.
**Why it matters:** If you can write a test for the task, you can probably RL-tune a small open model on it.
Source: [Hugging Face: TRL v1.0](https://huggingface.co/blog/trl-v1) · Added: 2026-11-18

### Harness-consistent RL beats bigger proprietary systems on cost · Nov 2026 🆕
FireFlash (UCLA) reported that RL with unit tests matching the eval harness lifted an open Flash-class model to 46.2 on Terminal-Bench 4.0 at $0.72 per run, ahead of a proprietary system at 44.5 for $22.02 per run *(as reported)*.
**Why it matters:** Train in the same harness you deploy in.
Source: [yage.ai summary](https://yage.ai/share/agent-harness-tricks-benchmark-en-20261109.html) · Added: 2026-11-18

### Open data for behaviour fine-tunes · Nous Arete-27B · Nov 2026 🆕
A Qwen3.8-27B fine-tune with the eval and training data released under Apache 2.0. It is a template for auditing and fixing behaviour in self-hosted models. → [Research to watch](../10-research-to-watch/README.md)
Added: 2026-11-18
