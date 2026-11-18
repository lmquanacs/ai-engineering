# 09 · AI security for builders

_Last updated: 2026-11-18_

> Prompt injection, supply-chain risk from skills and MCP servers, and agent permissions: the practical side.

## 🧠 Mental models

### Prompt injection is unsolved, so design for containment
OWASP ranks prompt injection as **LLM01:2025**, and for agents it escalates to **ASI01 Agent Goal Hijack**, because multi-step execution multiplies the damage. The 2026 research consensus is that no filter reliably stops adaptive attacks. Treat injection as a persistent architectural risk and limit the blast radius.
Sources: [OWASP-based overview](https://blckalpaca.at/en/knowledge-base/ai-agents/prompt-engineering-for-agents/prompt-injection-defense-techniques) · [HOL: what works beyond detection](https://hol.org/blog/prompt-injection-defense-2026-what-works) · Added: 2026-11-18

### The lethal trifecta / Agents Rule of Two
An agent session should have **no more than two** of these three properties:
**[A]** processes untrusted input · **[B]** has access to sensitive data or systems · **[C]** can change state or communicate externally.
If you need all three, add a human approval step or split the work across sessions.
Source: [Simon Willison on Meta's Rule of Two](https://simonwillison.net/2025/nov/2/new-prompt-injection-papers) · Added: 2026-11-18

## ✅ Builder checklist

- [ ] Untrusted content (web pages, issues, emails, tool output) is **data, not instructions**; mark it as such in prompts.
- [ ] Tools are least-privilege: read-only DB roles, scoped OAuth tokens, per-repo access.
- [ ] Irreversible actions (send, deploy, delete, pay) require human confirmation.
- [ ] Egress is allow-listed, so agents can't post data to arbitrary URLs.
- [ ] Every third-party `SKILL.md`, bundled script and MCP server is reviewed before install. Prefer vendor-official ones.
- [ ] Secrets are never in `.env` files the agent can read or in plaintext MCP JSON configs.
- [ ] Agent CLIs are kept current: security fixes ship weekly (see below).

## 🚨 Recent items

### Claude Code 2.1.319 security fixes · Nov 2026 🆕
Fixes a sandbox escape during worktree creation and a Bash permission bypass using crafted environment prefixes. Auto mode now fails closed when the server-side check is unavailable. **Upgrade.**
Source: [Claude Code changelog](https://code.claude.com/docs/en/changelog#2-1-319) · Added: 2026-11-18

### IBM Granite 4.1 LLMON preview · 2026-11-12 🆕
3B and 8B preview models post-trained on **LLMON (LLM Object Notation)** to enforce a structural separation between executable instructions and passive data. Claims are self-reported in an IBM preprint.
**Why it matters:** It tries to give LLMs the "this is data" channel that fixed SQL injection. Worth tracking, but not yet proven against adaptive attacks.
Source: [techjacksolutions release tracker](https://techjacksolutions.com/ai-news/technology/?per=100&tag=neocloud) · Added: 2026-11-18

### AI-found vulnerabilities at scale · OpenAI, Nov 2026 🆕
One autonomous agent run produced **948 working Linux kernel root exploits** (about $1.2M in API credits), and humans reviewed the reports before disclosure. GPT-6 Cyber reports 81 new high-severity Firefox bugs.
**Why it matters:** Discovery is getting cheaper for everyone, so patch velocity and dependency hygiene matter more.
Sources: [OpenAI: a thousand fewer paths to root](https://openai.com/index/a-thousand-fewer-paths-to-root/) · [GPT-6 Cyber](https://openai.com/index/introducing-gpt-6-cyber/) · Added: 2026-11-18

### MCP ecosystem hygiene (2026 data)
- 30+ CVEs against MCP servers in January–February 2026; one scan found security findings in 66% of popular servers. ([Toolradar](https://toolradar.com/blog/best-mcp-servers-2026))
- 48% of more than 19,000 MCP server codebases recommend insecure secret storage (Trend Micro). ([Amplitude summary](https://amplitude.com/compare/best-mcp-servers))
- The MCP 2026-07-28 spec makes remote servers formal **OAuth 2.1 resource servers**. Prefer servers that implement it. → [MCP servers](../04-mcp-servers/README.md)

## 📚 Further reading
- [The Landscape of Prompt Injection Threats in LLM Agents (arXiv 2602.10453)](https://arxiv.org/abs/2602.10453): a taxonomy of attacks and defences.
- [Prompt injection in 2026: self-replicating attacks and agent defences](https://redreamality.com/blog/prompt-injection-2026-survey-self-replicating/)
