# Research to watch

_Last updated: 2026-11-21_

> Papers and experiments likely to reach day-to-day engineering within about a year. Each entry gives a "so what" for builders.

### Agent runtimes hold a VM while they wait · "Held While Waiting" · arXiv 2611.26480 · Nov 2026 🆕
On Bedrock AgentCore, agents waited a median 2.7 s per model reply and computed for an estimated 5–40 ms, but every conversation reserves its own VM, which stayed held about 15 minutes after a 33-second conversation unless closed. Simulating 64 conversations sharing one environment needed 59× fewer environments *(as reported)*.
**So what:** Close runtime sessions explicitly; expect session quotas, not CPU, to cap scale. → [Agent infrastructure](../../architecture/agent-infrastructure/README.md)
Source: [arXiv 2611.26480](https://arxiv.org/abs/2611.26480) · Added: 2026-11-21

### Coding agents overstate success in their reports · arXiv 2611.25760 · Nov 2026 🆕
Eleven kinds of false or unsupported claims in end-of-task reports from real sessions, each costing users extra turns.
**So what:** Verify against diffs and test output, not the summary. → [Evals](../../architecture/evals-and-observability/README.md)
Source: [arXiv 2611.25760](https://arxiv.org/abs/2611.25760) · Added: 2026-11-21

### Compaction and memory: CompAct-Bench, GrepMem, model-dependent memory budgets · arXiv 2611.25673 / 2611.25123 / 2611.26361 · Nov 2026 🆕
Compaction still loses task state for frontier models; a plain log plus regex search beats lossy memory; and weaker models do better with fewer injected guidelines.
**So what:** Test compaction on resume tasks and try the simplest memory first. → [Context engineering](../../architecture/context-and-memory/README.md)
Source: [arXiv 2611.25673](https://arxiv.org/abs/2611.25673) · [arXiv 2611.25123](https://arxiv.org/abs/2611.25123) · [arXiv 2611.26361](https://arxiv.org/abs/2611.26361) · Added: 2026-11-21

### Instruction files don't stop overeager agents · Continuation Audits · arXiv 2611.24491 · Nov 2026 🆕
Realistic audits built from real coding-agent transcripts found models differ in which risky behaviour they show, and one ignored an explicit CLAUDE.md prohibition.
**So what:** Enforce permissions in the sandbox or hooks. → [AI security](../../architecture/security/README.md)
Source: [arXiv 2611.24491](https://arxiv.org/abs/2611.24491) · Added: 2026-11-21

### Coding agents p-hack · "Inference after coding agents" · arXiv 2611.23174 · Nov 2026 🆕
Four frontier coding agents, asked for a compelling finding on simulated data with no real effect, reported significant p-values 54–98% of the time. The authors' fix (reset the agent and replay it on subsamples) brings false rejections back to about 5% (as reported).
**So what:** Treat agent-run data or eval analysis as a search over analyses, and check its findings on held-out data. → [Evals](../../architecture/evals-and-observability/README.md)
Source: [arXiv 2611.23174](https://arxiv.org/abs/2611.23174) · Added: 2026-11-20

### Context trimming vs prefix caching · arXiv 2611.22238 · Nov 2026 🆕
Over more than 20,000 open-model coding-agent runs, removing old tool output or adding retrieved code made runs **more** expensive (+38–116% and +33–42%) once cached input was priced at a tenth of uncached input, with no gain in resolve rate (as reported).
**So what:** Context hacks have to be judged on cost per resolved task with real cache pricing. → [Context engineering](../../architecture/context-and-memory/README.md#-latest-evidence)
Source: [arXiv](https://arxiv.org/abs/2611.22238) · Added: 2026-11-19

### Minimal RAG memory is often enough · "RAG in a Trenchcoat" · arXiv 2611.22179 · Nov 2026 🆕
A deliberately simple RAG memory (BRIDGE) matches prior state of the art on LongMemEval-S and BEAM within confidence intervals, beats the best baseline on EverMemBench by 5.7–6.3 points, and uses one LLM call per ingest or query. New probes that require *applying* a remembered rule or pattern show no design wins everywhere (as reported; authors include Dawn Song and Ce Zhang).
**So what:** Start agent memory with plain retrieval over well-chunked notes, and evaluate on the behaviour you need (rule application, pattern induction), not on recall benchmarks alone.
Source: [arXiv](https://arxiv.org/abs/2611.22179) · Added: 2026-11-19

### Reversibility classes for agent tool calls · arXiv 2611.22075 · Nov 2026 🆕
Proposes labelling each tool action on a five-level "can it be undone?" scale, with argument-sensitive rules and a contract to capture prior state. A registry covers 536 tools across 20 MCP servers. A session guard built on it gated all 29 attributable attack runs (versus 18 for a plain read/write split) while adding nine approval prompts over 1,209 benign runs (as reported; the authors say registry-wide accuracy is not established).
**So what:** "Read vs write" is too coarse for approval gates. Gating on irreversibility is a cheap upgrade to human-in-the-loop policies. → [AI security](../../architecture/security/README.md)
Source: [arXiv](https://arxiv.org/abs/2611.22075) · Added: 2026-11-19

### Faster sandbox cold starts with learned snapshot sets · Readie · arXiv 2611.22171 · Nov 2026 🆕
Instead of one large pre-warmed image, Readie learns a set of small snapshots that together cover most agent-generated scripts. On 15K scripts it cut startup latency 3–22× and end-to-end runtime 1.3–3.3× at the same storage budget (as reported).
**So what:** Expect sandbox providers to adopt workload-aware snapshot pools. If you run your own sandboxes, profile which packages your agents actually import. → [Agent infrastructure](../../architecture/agent-infrastructure/README.md)
Source: [arXiv](https://arxiv.org/abs/2611.22171) · Added: 2026-11-19

### Harness tricks under controlled conditions · Surge AI, FireFlash (UCLA), HarnessTax (UC Berkeley) · Nov 2026 🆕
Ablation studies of popular coding-agent workflow plugins and low-level harness techniques. Main findings: reasoning effort, end-of-turn goal checks, spec-first TDD and cache-friendly plumbing help. Multi-agent committees and heavyweight harnesses mostly add cost. Harness-consistent RL on a cheap open model beat a proprietary system at about 1/30th of the cost per run (as reported).
**So what:** Slim your harness before you scale it out. → [Agentic workflows](../../architecture/agentic-workflows/README.md#-latest-evidence-what-actually-moves-the-needle)
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
Post-training models on an object notation that separates executable instructions from passive data. → [AI security](../../architecture/security/README.md#ibm-granite-41-llmon-preview--2026-11-12-)
Added: 2026-11-18

### Prompt-injection threat taxonomy · arXiv 2602.10453 · Feb 2026
A survey of prompt-injection attacks (by payload generation) and defences (by intervention stage) in LLM agents.
**So what:** A good map for threat-modelling your agent.
Source: [arXiv](https://arxiv.org/abs/2602.10453) · Added: 2026-11-18
