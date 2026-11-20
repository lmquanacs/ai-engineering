# AI security for builders

_Last updated: 2026-11-20_

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

### MCP Python SDK: three CVEs fixed in 1.30.0 / 2.2.0 · published 2026-10-27 🆕
Advisories against the official Python SDK (`mcp` on PyPI):
- **CVE-2026-116686** (GHSA-rwrf-2pqf-9j8j, CVSS 6.5): when a client validates a server-declared `outputSchema`, `$ref` URLs (http, https or file) are resolved, allowing blind outbound requests, local file reads and stalling every session in the process. Affects ≥ 1.10.0 < 1.30.0 and ≥ 2.0.0 < 2.2.0.
- **CVE-2026-116684** (CVSS 3.1 6.8): `TokenVerifier` did not check `aud`, so tokens issued for other services were accepted. Same ranges.
- **CVE-2026-116685** (CVSS 5.9): cross-origin redirects forwarded credential headers, and on 307/308 the request body. Affects ≥ 1.8.0.

The fixed versions were on PyPI from 2026-09-07; the advisories came later.
**Why it matters:** Clients that connect to untrusted MCP servers are the most exposed. Upgrade to `mcp` ≥ 1.30.0 or ≥ 2.2.0.
Sources: [GHSA-rwrf-2pqf-9j8j](https://github.com/modelcontextprotocol/python-sdk/security/advisories/GHSA-rwrf-2pqf-9j8j) · [OpenCVE: CVE-2026-116686](https://app.opencve.io/cve/CVE-2026-116686) · [Mend: CVE-2026-116684](https://www.mend.io/vulnerability-database/CVE-2026-116684/) · Added: 2026-11-20

### Claude Code 2.1.326 → 2.1.329 sandbox hardening · Nov 2026 🆕
Sandboxed commands write to fewer home folders, sign-in files are write-protected, and bypass mode now asks about some commands.
**Why it matters:** Re-test unattended jobs. Details → [Coding agents](../../build/coding-agents/README.md)
Added: 2026-11-20

### Reference Git MCP server: command-execution advisories · 2026-11-18 🆕
The MCP project published a batch of advisories against `mcp-server-git`. In each one, attacker-controlled Git configuration in the repository the agent operates on can make the server run a program. Triggers include a config include created by a merged branch (`git_merge`, GHSA-9vjp-x34c-xg6v), a promisor setting during a lazy fetch (GHSA-87qg-cmw8-jc5m) and a submodule's own config on `git_diff`, `git_checkout` and `git_add` (GHSA-8wv7-r664-7594). All are fixed in `mcp-server-git` **2026.11.18** (repo release v2.5.0). The same release fixes an SSRF-guard gap in `server-everything` 2.3.1 (GHSA-38j4-j742-j7r3), and two earlier `mcp-server-git` advisories were fixed in v2.4.0 on 2026-11-11.
**Why it matters:** The Git server is in most "core six" MCP setups. Pointing an agent at an untrusted clone or branch was enough to get code execution. **Upgrade now**, and don't run it against untrusted repositories outside a sandbox.
Sources: [GHSA-9vjp-x34c-xg6v (#5575)](https://github.com/modelcontextprotocol/servers/issues/5575) · [GHSA-87qg-cmw8-jc5m (#5574)](https://github.com/modelcontextprotocol/servers/issues/5574) · [GHSA-8wv7-r664-7594 (#5578)](https://github.com/modelcontextprotocol/servers/issues/5578) · [GHSA-38j4-j742-j7r3 (#5579)](https://github.com/modelcontextprotocol/servers/issues/5579) · Added: 2026-11-19

### Microsoft `agent-framework` PyPI compromise · 2026-11-17 🆕
Two malicious releases of Microsoft Agent Framework's PyPI meta-package, **1.26.1 and 1.26.2**, were uploaded on 2026-11-17 between about 20:35 and 21:08 UTC and were quarantined within the hour. Each drops a `.pth` file (`agent_framework_meta.pth` or `af_runtime_diag.pth`), so the stealer runs on **every Python start**, even if nothing imports the package. It takes secret-looking environment variables, credential files (Azure CLI, npm, pip, netrc, git, Docker, Hugging Face) and freshly minted Azure managed-identity and Azure DevOps OIDC tokens. 1.26.2 also takes GitHub Actions OIDC tokens. The data goes to a webhook.site URL. The last clean version is **1.26.0**. How the attacker got publishing access is not yet known.
**Why it matters:** Any CI runner or dev box that resolved an unpinned `agent-framework` during that window should be treated as compromised. Pin to 1.26.0, check site-packages for those `.pth` files, search egress logs for webhook.site, rotate every secret on affected hosts, and review Entra ID federated credentials and sign-in logs. Rotating stored secrets alone is not enough, because the malware minted new tokens.
Sources: [Wiz](https://www.wiz.io/blog/malicious-version-of-microsofts-agent-framework-published-to-pypi) · [StepSecurity](https://www.stepsecurity.io/blog/microsoft-agent-framework-pypi-package-compromised) · Added: 2026-11-19

### Claude Code 2.1.319 → 2.1.325 security fixes · Nov 2026 🆕
**2.1.319** fixes a sandbox escape during worktree creation and a Bash permission bypass using crafted environment prefixes, and auto mode now fails closed when the server-side check is unavailable. **2.1.321** fixes MCP OAuth requests sending secrets such as refresh tokens to another host after a server redirect, a read-only Bash command running outside the sandbox without a prompt, and deny rules not applying to the target of `cp`/`mv` into a directory. **2.1.325** fixes zstd response decoding, a Bash allow rule that could run a different program than it names, and compound commands running without asking; sandboxed Bash now prompts by default. **Upgrade to ≥ 2.1.325.** Details: [Coding agents](../../build/coding-agents/README.md).
Sources: [Claude Code changelog](https://code.claude.com/docs/en/changelog#2-1-319) · [Claude Code CHANGELOG (v2.1.325 tag)](https://raw.githubusercontent.com/anthropics/claude-code/v2.1.325/CHANGELOG.md) · Added: 2026-11-18 · Updated: 2026-11-19

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
- The MCP 2026-07-28 spec makes remote servers formal **OAuth 2.1 resource servers**. Prefer servers that implement it. → [MCP servers](../../build/mcp-servers/README.md)

## 📚 Further reading
- [The Landscape of Prompt Injection Threats in LLM Agents (arXiv 2602.10453)](https://arxiv.org/abs/2602.10453): a taxonomy of attacks and defences.
- [Prompt injection in 2026: self-replicating attacks and agent defences](https://redreamality.com/blog/prompt-injection-2026-survey-self-replicating/)
