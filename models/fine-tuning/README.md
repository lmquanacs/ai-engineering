# Fine-tuning & post-training

_Last updated: 2026-11-27_

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

### Training multi-agent teams with GRPO on two GPUs · Hugging Face "Swarms, Flocks, Gangs" · 2026-11-26 🆕
The first post in a Hugging Face series trains four agents that share one model with a team reward, using the TRL example `examples/async_grpo_s3_aggregation` on Hugging Face Jobs. The run takes about five hours on two H200s, roughly $50. Training success rose from 6.6% to 82.3% over 75 steps, the team solved 26 of 32 held-out problems, and it used 37.4% fewer tokens per attempt *(self-reported)*. The post's script falls back to a TRL pull request if the example isn't on `main` yet.
**Why it matters:** a cheap, reproducible starting point if you want to test whether training (rather than prompting) makes a multi-agent setup worth its cost. The post also asks the right control question: did cooperation help, or did you just spend more tokens?
Source: [Hugging Face blog](https://huggingface.co/blog/training-swarms) · Added: 2026-11-27

### Nemotron 3.5 Parse: open synthetic document datasets and the SFT → GRPO recipe · 2026-11-26 🆕
NVIDIA published the data and method behind its document parser: synthetic chart, table and multilingual-OCR datasets on Hugging Face (`nvidia/Synthetic-Charts-V1`, `nvidia/Synthetic-Tables-V1`, `nvidia/OCR-Synthetic-Multilingual-v2`), and a recipe of SFT followed by RL with verifiable rewards using GRPO. The rewards score extraction quality and penalise repetition loops. On development checkpoints, loop-flagged pages fell from 126 to 29 and the overall score rose from 66.24 to 71.38 *(self-reported)*. The parser model itself is covered in [RAG & retrieval](../../architecture/rag-and-retrieval/README.md).
**Why it matters:** if an open parser fails on your document types, this is a template for adapting it: synthetic pages for SFT, then GRPO with rewards that check structure and stop looping. Check each dataset's licence on its card before you train on it.
Source: [Hugging Face blog](https://huggingface.co/blog/nvidia/building-on-nemotron-35-parse-open-data-fine-tunin) · [Synthetic-Charts-V1](https://huggingface.co/datasets/nvidia/Synthetic-Charts-V1) · Added: 2026-11-27

### TRL 1.19.0: multi-teacher distillation, packed SFT fix for SDPA · 2026-11-25 🆕
`DistillationTrainer` can now take a dict of teacher models, and a `teacher_id` column picks the teacher for each example. It also accepts an `environment_factory`, so you can distil against stateful environments. In SFT with BFD packing, packed examples now stay as separate rows, so SDPA attention no longer spans the whole packed batch. The release notes say this roughly halves step time, and flash-attention runs are unaffected *(self-reported)*.
**Why it matters:** If you pack SFT data on SDPA (no flash attention), upgrade for the speed-up and re-run a short eval to compare against your earlier checkpoints. Routing each example to its own teacher makes it easier to distil several specialist models into one student. No breaking changes are listed.
Source: [PyPI trl 1.19.0](https://pypi.org/project/trl/) · [release notes (releases.sh mirror)](https://releases.sh/hugging-face/fine-tuning) · [release PR #8587](https://github.com/huggingface/trl/pull/8587) · Added: 2026-11-26

### PEFT 0.22.0: Python 3.11+, stricter `modules_to_save`, new PaCA method · 2026-11-19 🆕
PEFT now needs Python 3.11 or newer. The release adds PaCA (Partial Connection Adaptation), which tunes selected input columns of the existing weights instead of adding adapter layers, plus Astra and NoRA initialisations for LoRA. Two changes can break existing setups. `modules_to_save` now matches whole sub-module names rather than suffixes. A fix to the OFT Conv2d forward pass can also change outputs from existing Conv2d OFT checkpoints. 0.21.3 (2026-11-13) made `save_pretrained` on tensor-parallel (DTensor) models gather only the adapter weights.
**Why it matters:** Pin `peft<0.22` on Python 3.10 images. Before upgrading, check that `modules_to_save` still selects the modules you expect, because a suffix that used to match may now match nothing.
Source: [PyPI peft 0.22.0](https://pypi.org/project/peft/) · [release notes (releases.sh mirror)](https://releases.sh/hugging-face/peft) · Added: 2026-11-25

### Together Post-Training: hosted SFT and RL on open models · 2026-10-19 (missed earlier) 🆕
Together's managed trainer runs SFT and RL, with built-in cross-entropy, GRPO, CISPO and DPPO losses. You can also compute a custom loss locally and send the gradients. It supports LoRA, including several adapters sharing one GPU, and full-weight training for selected models. Launch models were Muse Spark Open, GLM 5.3, Kimi K3 and Qwen 3.8-27B. Together says moving from Tinker takes a one-line import change, and trained checkpoints can be served as merged FP4. Pricing was discounted to $9 per B200 GPU-hour for the first eight weeks after launch.
**Why it matters:** It is another managed option alongside Tinker for RL on large open MoE models without running your own cluster. Check that FP4 serving of your checkpoint matches your evals.
Source: [Together blog](https://together.ai/blog/together-post-training) · Added: 2026-11-25

### TOUMAII: 4.5M tool-calling preference pairs for DPO · arXiv 2611.26722 · Nov 2026 🆕
A preference dataset of about 4.5M validated pairs built from the Toucan-1.5M tool-use conversations, covering single- and multi-turn, parallel and sequential function calls, plus TOUMAII-Gen, a pipeline that turns any tool-calling SFT set into preference pairs based on the mistakes models actually make. A 3B model trained with DPO on it performed on par with other high-quality tool-calling preference sets *(self-reported)*. A smaller ToolACE-derived set shows the generator works on other sources. The poster page doesn't state a licence for the new data or code; check before commercial use.
**Why it matters:** If your SFT'd small model still mis-calls tools, this gives you ready DPO data, or a way to make pairs from your own SFT traces.
Source: [arXiv 2611.26722](https://arxiv.org/abs/2611.26722) · [NeurIPS 2026 workshop poster](https://neurips.cc/virtual/2026/160067) · [toumaii-gen code](https://github.com/toumaii/toumaii-gen) · Added: 2026-11-24

### Hugging Face "harness adapters": RL a LoRA inside the harness you ship · 2026-11-20 🆕
Hugging Face trained one LoRA for Qwen3.8-27B per agent harness (pi, Hermes Agent, OpenCode), running RL inside the unmodified harness with TRL's `AsyncGRPOTrainer`, OpenEnv and Harbor-format tasks. With pi on Terminal-Bench 2.1, pass@1 rose from 39% to 55% while average tokens per task fell from 2.9K to 1.5K, and the three adapters merged into one "super adapter" that works under all three *(self-reported)*. Adapters, tasks and trajectories are on the Hub.
**Why it matters:** An open, reproducible recipe for tuning a frozen base model to the exact harness and task mix you run, with cheaper runs as a side effect.
Source: [HF blog: harness adapters](https://huggingface.co/blog/harness-adapters-at-scale) · Added: 2026-11-21

### Unsloth: faster AsyncGRPO, Inkling fine-tuning, AMD NPU support · 2026-11-19 → 11-23 🆕
- **2026-11-23 (changelog v0.1.923-beta):** AsyncGRPO runs take 40% less time, and GRPO rollouts are 2× faster on Strix Halo. Thinking Machines' Inkling models can now be fine-tuned, multi-GPU diffusion LoRA roughly doubles samples per second on two GPUs, and Inkling 2 Mini decodes up to 1.9× faster on 8–12 GB GPUs *(self-reported)*.
- **2026-11-19:** Models converted to Q4NX can now run on AMD Ryzen AI NPUs. The release adds LoRA training for LTX-2.5 and MOSS-Image, makes diffusion LoRA up to 42% faster per step (now on T4 too), and QLoRA up to 25% faster *(self-reported)*.

**Why it matters:** Existing QLoRA and async GRPO jobs get faster when you upgrade, and local video and image fine-tuning gets cheaper.
Source: [Unsloth changelog](https://unsloth.ai/docs/new/changelog) · [PyPI](https://pypi.org/project/unsloth/) · Added: 2026-11-21 · Updated: 2026-11-25

### TRL 1.18.0 → 1.18.2: async GRPO goes stable · 2026-11-13 → 11-19
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

### Harness-consistent RL beats bigger proprietary systems on cost · Nov 2026
FireFlash (UCLA) reported that RL with unit tests matching the eval harness lifted an open Flash-class model to 46.2 on Terminal-Bench 4.0 at $0.72 per run, ahead of a proprietary system at 44.5 for $22.02 per run *(as reported)*.
**Why it matters:** Train in the same harness you deploy in.
Source: [yage.ai summary](https://yage.ai/share/agent-harness-tricks-benchmark-en-20261109.html) · Added: 2026-11-18

### Open data for behaviour fine-tunes · Nous Arete-27B · Nov 2026
A Qwen3.8-27B fine-tune with the eval and training data released under Apache 2.0. It is a template for auditing and fixing behaviour in self-hosted models. → [Research to watch](../../learn/research/README.md)
Added: 2026-11-18
