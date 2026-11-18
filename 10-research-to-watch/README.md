# 10 · Research to watch

_Last updated: 2026-11-18_

> Papers and experiments likely to reach day-to-day engineering within about a year. Each entry gives a "so what" for builders.

### Harness tricks under controlled conditions · Surge AI, FireFlash (UCLA), HarnessTax (UC Berkeley) · Nov 2026 🆕
Ablation studies of popular coding-agent workflow plugins and low-level harness techniques. Main findings: reasoning effort, end-of-turn goal checks, spec-first TDD and cache-friendly plumbing help. Multi-agent committees and heavyweight harnesses mostly add cost. Harness-consistent RL on a cheap open model beat a proprietary system at about 1/30th of the cost per run (as reported).
**So what:** Slim your harness before you scale it out. → [Agentic workflows](../03-agentic-workflows/README.md#-latest-evidence-what-actually-moves-the-needle)
Source: [yage.ai summary](https://yage.ai/share/agent-harness-tricks-benchmark-en-20261109.html) · Added: 2026-11-18

### Weight-space programming · MIT CSAIL · Nov 2026 🆕
A frontier model edited a 0.8B model's weights directly, with no gradient training, and raised MATH-500 from 7.9% to 48.1% while changing 0.016% of the weights (as reported).
**So what:** If this reproduces, small task-specific models could be "patched" by a larger model instead of fine-tuned.
Source: [Blog post](https://rikiyat.github.io/blog/weight-space-programming/) · Added: 2026-11-18

### Value-targeted fine-tuning with open evals · Nous Research Arete-27B · Nov 2026 🆕
A Qwen3.8-27B fine-tune that cut the measured propaganda rate from 22% to 0.9% with essentially unchanged general scores. Apache 2.0, and the eval and training data are released.
**So what:** It is a reproducible recipe for auditing and fixing behaviour on sensitive topics in open-weight models you self-host.
Source: [Hugging Face](https://huggingface.co/NousResearch/Arete-27B) · Added: 2026-11-18

### Structural instruction/data separation · IBM LLMON · Nov 2026 🆕
Post-training models on an object notation that separates executable instructions from passive data. → [AI security](../09-ai-security/README.md#ibm-granite-41-llmon-preview--2026-11-12-)
Added: 2026-11-18

### Prompt-injection threat taxonomy · arXiv 2602.10453 · Feb 2026
A survey of prompt-injection attacks (by payload generation) and defences (by intervention stage) in LLM agents.
**So what:** A good map for threat-modelling your agent.
Source: [arXiv](https://arxiv.org/abs/2602.10453) · Added: 2026-11-18
