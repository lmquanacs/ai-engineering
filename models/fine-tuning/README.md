# Fine-tuning & post-training

_Last updated: 2026-11-21_

> Adapting open-weight models: LoRA/QLoRA, preference tuning, RL with verifiable rewards, distillation and the data behind them. Lower priority unless you train models, but this is where open models get specialised.

## 🧭 Do you actually need to fine-tune?

| Your gap | Reach for |
|---|---|
| The model doesn't **know** your docs, products or policies | **RAG**: citations, instant updates, fewer hallucinated facts. → [Context engineering](../../architecture/context-and-memory/README.md) |
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

## 🗞️ Releases

### Hugging Face "harness adapters": RL a LoRA inside the harness you ship · 2026-11-20 🆕
Hugging Face trained one LoRA for Qwen3.8-27B per agent harness (pi, Hermes Agent, OpenCode), running RL inside the unmodified harness with TRL's `AsyncGRPOTrainer`, OpenEnv and Harbor-format tasks. With pi on Terminal-Bench 2.1, pass@1 rose from 39% to 55% while average tokens per task fell from 2.9K to 1.5K, and the three adapters merged into one "super adapter" that works under all three *(self-reported)*. Adapters, tasks and trajectories are on the Hub.
**Why it matters:** An open, reproducible recipe for tuning a frozen base model to the exact harness and task mix you run, with cheaper runs as a side effect.
Source: [HF blog: harness adapters](https://huggingface.co/blog/harness-adapters-at-scale) · Added: 2026-11-21

### Unsloth: AMD NPU support, video-model LoRA, faster QLoRA · 2026-11-19 🆕
Models converted to Q4NX can now run on AMD Ryzen AI NPUs. The release adds LoRA training for LTX-2.5 and MOSS-Image, makes diffusion LoRA up to 42% faster per step (now on T4 too), and QLoRA up to 25% faster *(self-reported)*.
**Why it matters:** Existing QLoRA jobs get a free speed-up on upgrade, and local video/image fine-tuning gets cheaper.
Source: [Unsloth changelog](https://unsloth.ai/docs/new/changelog) · Added: 2026-11-21

### TRL 1.18.0 → 1.18.2: async GRPO goes stable · 2026-11-13 → 11-19 🆕
- **1.18.0:** `AsyncGRPOTrainer` moves from `trl.experimental` to top-level `trl`. Breaking: `weight_transfer` and `rollout_worker` are removed and `max_inflight_tasks` is renamed `max_concurrent_rollouts`. MoE models saved by `SFTTrainer` from v1.7.0 to v1.17.1 keep `output_router_logits=True` in their config and need it reset by hand.
- **1.18.1** (2026-11-17): accuracy rewards are graded in a separate process, so a pathological answer can't hang training; follows the Transformers 5.23 rename of gradient checkpointing to activation checkpointing.
- **1.18.2** (2026-11-19): `BEMACallback` works with frozen parameters.

**Why it matters:** Async GRPO users must update their configs, and anyone who SFT-trained MoE models with TRL should check the saved `config.json`.
Source: [TRL v1.18.0 release](https://github.com/huggingface/trl/releases/tag/v1.18.0) · [v1.18.1](https://github.com/huggingface/trl/releases/tag/v1.18.1) · [PyPI](https://pypi.org/project/trl/) · Added: 2026-11-20

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
A Qwen3.8-27B fine-tune with the eval and training data released under Apache 2.0. It is a template for auditing and fixing behaviour in self-hosted models. → [Research to watch](../../learn/research/README.md)
Added: 2026-11-18
