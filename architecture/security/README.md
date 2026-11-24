# AI security for builders

_Last updated: 2026-11-25_

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

### LiteLLM, AutoGPT, ECS MCP, DBHub, browser-use: AI-tool CVE batch · published 2026-11-23 → 11-24 🆕
- **LiteLLM** (six ZDI advisories, auth required for all): RCE via `pass_through_endpoints` (CVE-2026-136539, CVSS 7.2; fix in PR #27801), key-management endpoints missing authorization (CVE-2026-136537, fixed in 1.104.0), virtual-key model-alias privilege escalation (CVE-2026-136538), SSRF through `api_base` (CVE-2026-136536), and the OIDC secret resolver reading env vars (CVE-2026-136540, fixed in 1.84.0). The sixth, command injection through MCP stdio configs (CVE-2026-136535, CVSS 7.2), went out as a **0-day**: LiteLLM says stdio servers run admin-chosen commands by design and no patch is coming, so only proxy admins should be able to create or test MCP servers.
- **Amazon ECS MCP Server** (`awslabs.ecs-mcp-server`) < 0.1.36: prompt injection can make the troubleshooting tool return plaintext task-definition env vars and secret references that the sensitive-data setting should redact (CVE-2026-135614). Upgrade and rotate credentials kept as plaintext env vars.
- **Bytebase DBHub MCP**: ZDI published an unauthenticated auth bypass via crafted SQL as a **0-day** (CVE-2026-136441, CVSS 9.8, reported 2025-07). ZDI does not say whether recent releases fix it; its only advice is to restrict access to the server. This is separate from the read-only bypass fixed in 1.7.0 (below).
- **browser-use** < 1.0.0: two `SecurityWatchdog` bypasses (backslash URL parser differential, raw `startswith()` domain match) let a prompt-injected navigate step reach blocked or private hosts (CVE-2026-136452, CVE-2026-136453). Fixed in 1.0.0; see the [1.0 migration notes](../../build/voice-and-multimodal/README.md).
- **AutoGPT Platform**: shared or marketplace agents can capture users' saved SMTP/database logins (CVE-2026-130171) and credentials can leak through backslash redirects (CVE-2026-133449), both fixed in 0.11.0. In 0.7.1–0.8.4, `/` and `@path` text sent to the Claude Code CLI bypasses the tool allow-list and PreToolUse hooks (CVE-2026-133448), and an incomplete IPv6 blocklist allows SSRF (CVE-2026-130178).
- Smaller: **Sim** 0.5.61 to < 0.9.41 lets write-level members make workflow MCP servers public (CVE-2026-135162). **Apache IoTDB MCP Server** ≤ 0.2.0 logs the DB password in plaintext (CVE-2026-135747; upgrade to 0.3.0). **Prismor** < 1.57.0 lets any web page turn off its agent guardrails through a wildcard-CORS local API (CVE-2026-136185). **Spring AI** 2.0.0–2.0.2: the Typesense filter converter mistranslates grouped expressions, which can break tenant filters (CVE-2026-59442), and the PDF readers can be made to run out of memory (CVE-2026-59340). Both are fixed in [2.0.3 / 2.1.0](../../build/libraries/jvm.md).
**Why it matters:** If you run a LiteLLM proxy, upgrade to a current release and make sure only admins can define MCP servers. Don't expose DBHub to untrusted clients until Bytebase says the ZDI bug is fixed.
Source: [ZDI-26-1084](https://www.zerodayinitiative.com/advisories/ZDI-26-1084/) · [ZDI-26-1031](https://www.zerodayinitiative.com/advisories/ZDI-26-1031/) · [ZDI-26-1082](https://www.zerodayinitiative.com/advisories/ZDI-26-1082/) · [ZDI-26-1067 (DBHub)](https://www.zerodayinitiative.com/advisories/ZDI-26-1067/) · [NVD CVE-2026-135614](https://nvd.nist.gov/vuln/detail/CVE-2026-135614) · [NVD CVE-2026-136452](https://nvd.nist.gov/vuln/detail/CVE-2026-136452) · [NVD CVE-2026-130171](https://nvd.nist.gov/vuln/detail/CVE-2026-130171) · [NVD CVE-2026-133448](https://nvd.nist.gov/vuln/detail/CVE-2026-133448) · [Spring CVE-2026-59442](https://spring.io/security/cve-2026-59442) · Added: 2026-11-25

### Tool-call smuggling: the guard and the executor parse different calls · arXiv 2611.30624 · 2026-11-23 🆕
Provider, gateway, SDK, guard and executor all re-parse a tool call's JSON, and they disagree on edge cases such as duplicate keys. The authors gave the same bytes to 17 pinned parser and validator configurations; most pairs disagreed on some inputs, including two official MCP SDKs. On τ-bench and AgentDojo tasks, attacks got guard-blocked actions executed while the audit log recorded only the approved call. A malicious server that copies a real tool's schema and adds one field got models to fill it with user data, unseen by the guard *(self-reported)*.
**Why it matters:** If you have a tool-call guard or approval step, parse each call once, keep only the approved schema's fields, and pass that exact object (bound to its call ID) to the executor. Don't let the executor re-parse the raw text. The authors say this stopped all 7,412 crafted inputs.
Source: [arXiv 2611.30624](https://arxiv.org/abs/2611.30624) · Added: 2026-11-25

### "Compatible" MCP tool updates often widen what the agent can do · SchemaCaps · arXiv 2611.30750 · 2026-11-23 🆕
None of 8 surveyed MCP clients and scanners re-asks for approval when a tool's input schema widens. In 604 releases of 39 public MCP servers, 412 of 580 backward-compatible schema changes widened some input, and at least 76 added or widened an authority-bearing argument (recipient, path, endpoint). The paper proposes a re-approval rule based on subschema inclusion *(self-reported)*.
**Why it matters:** Approving a tool once is not enough. Pin MCP server versions, diff `inputSchema` on upgrade, and re-review any new or widened argument that controls where data goes.
Source: [arXiv 2611.30750](https://arxiv.org/abs/2611.30750) · Added: 2026-11-25

### Google semantic governance policies: an LLM judge checks each tool call before it runs · preview · 2026-11-20 🆕
In Gemini Enterprise Agent Platform, Agent Gateway can now check each proposed tool call against the user's original request (on by default) and against policies written in plain English. Denied calls are replaced with a configurable message, and verdicts and rationales go to Cloud Logging. It works with the Gemini API, the Anthropic Messages API and OpenAI-compatible Chat Completions (including vLLM). It has a dry-run mode, does not evaluate streamed responses, and denies tools without descriptions by default. Google has not yet published AgentDojo results for it.
**Why it matters:** This is a managed version of the "check intent before acting" pattern. Agent egress must go through [Agent Gateway](../../platforms/google-cloud/README.md), and because the judge is probabilistic, run dry-run first and keep deterministic controls (IAM, allowlists) in place.
Source: [Google Developers Blog](https://developers.googleblog.com/en/check-what-your-ai-agents-do-before-they-do-it-with-semantic-governance-policies/) · Added: 2026-11-25

### MCP auth and gateway CVEs: Pomerium, LiteLLM, Hermes Agent, reference servers · published 2026-11-23 🆕
- **Pomerium** 0.30.0 to < 0.34.0: the MCP token endpoint (`/.pomerium/mcp/token`) skips the client-secret check for `client_secret_basic` clients, so anyone holding an intercepted authorization code or refresh token can redeem it with any secret (CVE-2026-135300, CVSS 4.0 9.1). Fixed in 0.34.0.
- **LiteLLM Proxy** 1.62.4 to < 1.84.0: any API-key holder can put `callbacks` in a request body and register a process-wide logging callback, for example an unconfigured Langfuse or LangSmith integration, to collect every user's prompts and responses, or switch off operator logging (CVE-2026-135287, GHSA-34v7-jqrg-944p). The fix, 1.84.0, has been on PyPI since 2026-05-14.
- **Hermes Agent** (Nous Research) 0.21.6–0.23.1: with a Docker or SSH terminal backend, code inside the backend can write `LD_PRELOAD` or `PATH` into an env file that the agent merges into later browser and computer-use processes, giving code execution on the agent host (CVE-2026-130164). Fixed in 0.23.2; the default local backend is not affected.
- **mcp-server-git** before 2026.10.28: a nested `.git` file with a `gitdir` pointer escapes the `--repository` restriction to read and branch another repository (CVE-2026-134465, GHSA-w766-5x43-whvw). **mcp-server-fetch** 2026.10.10 to < 2026.11.11: IPv6 site-local addresses pass the SSRF guard (CVE-2026-134492, low).
- **astro-airflow-mcp** 0.5.0–0.9.1: its telemetry subprocess can import a `json.py` from the working directory, so opening an untrusted project runs code (CVE-2026-133632). Fixed in 0.9.2, or set `AF_TELEMETRY_DISABLED=1`.
**Why it matters:** The plumbing around agents keeps failing at its trust boundaries: an MCP gateway's token endpoint, fields in an LLM proxy's request body, an env file a sandbox can write. Upgrade the ones you run. If you ran a LiteLLM proxy older than 1.84.0 with keys handed to other teams, check its callback settings for integrations you never enabled.
Source: [NVD CVE-2026-135300](https://nvd.nist.gov/vuln/detail/CVE-2026-135300) · [NVD CVE-2026-135287](https://nvd.nist.gov/vuln/detail/CVE-2026-135287) · [NVD CVE-2026-130164](https://nvd.nist.gov/vuln/detail/CVE-2026-130164) · [NVD CVE-2026-134465](https://nvd.nist.gov/vuln/detail/CVE-2026-134465) · [NVD CVE-2026-134492](https://nvd.nist.gov/vuln/detail/CVE-2026-134492) · [NVD CVE-2026-133632](https://nvd.nist.gov/vuln/detail/CVE-2026-133632) · Added: 2026-11-24

### FastMCP 4.2.5: OAuth proxy hardening · 2026-11-23 🆕
FastMCP 4.2.5 includes several security fixes: CIMD clients can no longer widen the scopes a server allows, redirect-URI matching checks the query component, root path patterns are compared exactly, reusing a rotated refresh token after 60 s revokes the whole grant, and OpenAPI-wrapped tools stop forwarding MCP transport headers to the backend. Some of these change behaviour; the checklist is on the [MCP servers page](../../build/mcp-servers/README.md#-security-notes).
**Why it matters:** Refresh-token reuse detection is standard OAuth practice, but it breaks clients that copy one stored refresh token between processes.
Source: [FastMCP changelog v4.2.5](https://raw.githubusercontent.com/PrefectHQ/fastmcp/main/docs/changelog.mdx) · Added: 2026-11-24

### More MCP fixes: DBHub read-only bypass, mcp-server-kubernetes, FastMCP OAuth proxy · 2026-11-21 → 11-22 🆕
- **DBHub** < 1.7.0 (`@bytebase/dbhub`): the SQL scanner misreads backslash-escaped quotes, so a client restricted to read-only `execute_sql` can hide stacked statements that clear `transaction_read_only` or `COMMIT`, then modify or drop MySQL, MariaDB or PostgreSQL data (CVE-2026-134803). Fixed in 1.7.0 (2026-11-16).
- **mcp-server-kubernetes** < 4.2.0: dash-prefixed positional values in `exec_in_pod`, `kubectl_patch` and `kubectl_logs` reach kubectl as flags (for example `--filename`), letting a client on SSE or Streamable HTTP read files on the server host (CVE-2026-134817, CVSS 7.1). Fixed in 4.2.0.
- **FastMCP** 4.2.4 (2026-11-21): concurrent token requests could redeem one OAuth-proxy authorization code or refresh token twice (GHSA-78c8-3jhx-5mg7), and a revoked proxy access token could validate again after a refresh. Both fixed.
**Why it matters:** It's the same lesson as the last batch: a SQL parser deciding what counts as "read-only" is not a boundary. Connect database MCP servers with a read-only database role, and pass tool arguments to CLIs after `--`.
Source: [CVE-2026-134803](https://www.cve.org/CVERecord?id=CVE-2026-134803) · [CVE-2026-134817](https://www.cve.org/CVERecord?id=CVE-2026-134817) · [FastMCP changelog](https://raw.githubusercontent.com/PrefectHQ/fastmcp/main/docs/changelog.mdx) · Added: 2026-11-23

### Vercel AI SDK: tool-approval signatures replayable for auto-denied calls · 7.0.178 · 2026-11-20 🆕
With `experimental_toolApprovalSecret` set, the SDK signed approval requests even for tool calls its policy denied automatically; a client controlling message history could flip them to approved. Fixed in `ai` 7.0.178, but earlier signatures stay valid until you rotate the secret. Details on the [TypeScript libraries page](../../build/libraries/typescript.md).
**Why it matters:** A human-in-the-loop gate is only as strong as what the client can't forge; rotate the secret after upgrading.
Source: [`ai` on npm](https://www.npmjs.com/package/ai?activeTab=versions) · Added: 2026-11-22

### MCP server CVEs: "read-only" modes that weren't · 2026-11-18 → 11-21 🆕
- **mcp-ssh-manager:** backup tools (CVE-2026-129995, CVSS 8.8) and DB tools (CVE-2026-77383) build shell commands from tool arguments; `ssh_backup_list`/`ssh_db_list` count as read-only, so readonly mode doesn't help, and indirect prompt injection is a stated vector. **Upgrade to ≥ 3.8.5** (3.6.7 fixed only the DB tools).
- **SurrealDB** 3.1.0 to < 4.0.0: an escaped backtick in an MCP tool argument breaks out of the identifier and runs arbitrary SurrealQL (CVE-2026-134293). Fixed in 4.0.0.
- **ArcadeDB** 26.3.1 to < 26.11.1: Gremlin scripts that fall back to Groovy are classed as reads, so writes pass the MCP read-only query tool (CVE-2026-134324, plus related CVEs). Fixed in 26.11.1.
- **codebase-memory-mcp:** a Cypher query with too many RETURN items overflows a stack array (CVE-2026-114494) and `base_branch` can inject git options to write files (CVE-2026-114496); fixed in 0.9.0. A Windows-only process-kill check bypass (CVE-2026-114497) is fixed in 0.9.1-rc.1 and later.
- **k8s-mcp-server** < 1.1.0: default SSE transport listens on 0.0.0.0:8080 without auth, exposing Kubernetes write tools (CVE-2026-130007).
- **jupyter-mcp-server** < 1.0.3: standalone HTTP mode has unauthenticated control endpoints and no Origin check (CVE-2026-77318, CVE-2026-77359), so a web page can redirect the kernel.
- **Coder Agents** `read_skill_file` follows symlinks, so a malicious skill can pull other workspace files into context (CVE-2026-134363, low); fixed in 2.34.17 / 2.36.12 / 2.37.9 / 2.38.5.
**Why it matters:** Query classifiers and "read-only" flags in MCP servers keep failing; enforce read-only with database permissions and network binding, not the tool's label.
Source: [CVE-2026-129995](https://www.cve.org/CVERecord?id=CVE-2026-129995) · [CVE-2026-134293](https://www.cve.org/CVERecord?id=CVE-2026-134293) · [CVE-2026-134324](https://www.cve.org/CVERecord?id=CVE-2026-134324) · [CVE-2026-114494](https://www.cve.org/CVERecord?id=CVE-2026-114494) · [CVE-2026-130007](https://www.cve.org/CVERecord?id=CVE-2026-130007) · [CVE-2026-77318](https://www.cve.org/CVERecord?id=CVE-2026-77318) · [CVE-2026-134363](https://www.cve.org/CVERecord?id=CVE-2026-134363) · Added: 2026-11-22

### Pydantic AI Harness: ReDoS in ANSI stripping · CVE-2026-133161 · 2026-11-19 🆕
`ToolOutputLimits(strip_ansi=True)` uses a regex that is quadratic in line length, so a few hundred KB of tool output with unterminated escape sequences can block the event loop for tens of seconds or more. Shell, file, web and MCP tool output can all carry it. The CVE lists 0.4.0 up to 0.69.0 as affected; 0.70.0 (2026-11-17) is the likely fix, but we couldn't confirm it in the advisory.
**Why it matters:** One hostile web page or file can stall every agent sharing that event loop.
Source: [CVE-2026-133161](https://www.cve.org/CVERecord?id=CVE-2026-133161) · Added: 2026-11-22

### Pydantic AI: tool results rebuilt as file objects (SSRF, credentialed reads) · CVE-2026-133505 · 2026-11-20 🆕
When message history is serialized and reloaded, a tool result containing JSON shaped like a Pydantic AI file type is rebuilt as a real file object. Whoever controls that tool data (an MCP server, an external record) can make the app fetch internal URLs or make the provider read `s3://` objects or uploaded files with your credentials. Stored history, server-held UI history and durable runs (Temporal, DBOS, Prefect) are affected. Fixed in `pydantic-ai`/`pydantic-ai-slim` 2.66.0 and 1.107.10.
**Why it matters:** Durable agents that persist history are exactly the affected pattern; current 2.71.0 is safe.
Source: [NVD CVE-2026-133505](https://nvd.nist.gov/vuln/detail/CVE-2026-133505) · [GHSA-4cj4-hgwf-4hc4](https://github.com/pydantic/pydantic-ai/security/advisories/GHSA-4cj4-hgwf-4hc4) · Added: 2026-11-21

### MCP server and gateway CVE batch · 2026-11-18 → 11-20 🆕
- **Supergateway:** cross-site WebSocket hijacking in stdio-to-WebSocket mode lets any web page drive the wrapped stdio tools, even on localhost (CVE-2026-132121, 2.4.0–4.2.2, CVSS 8.1); unauthenticated DoS in stdio-to-SSE mode (CVE-2026-131857, 4.2.0–4.2.2). **Update 2026-11-24:** 4.2.3/4.2.4 (2026-11-23) fix the DoS and refuse WebSocket upgrades from browser origins not in `--cors`, but only when you pass `--cors <origins>` or `--apiKey`. By default the gateway still accepts any page and just warns (from the published package code and README; no advisory update yet).
- **Obot** < 0.27.0: four CVEs, including token theft via unvalidated MCP protected-resource metadata (CVE-2026-130766) and heredoc command injection (CVE-2026-130767).
- **`awslabs.document-loader-mcp-server`** 1.0.10–1.0.20: path traversal when `DOCUMENT_BASE_DIR` is unset (CVE-2026-130901); fixed in 1.0.21.
- **LibreChat** < 0.8.8: MCP OAuth redirect SSRF (CVE-2026-54031).
- **JetBrains Junie CLI** < 26.6.29: agent file tools could write outside the project (CVE-2026-133195).
**Why it matters:** "Bound to localhost" doesn't protect WebSocket or HTTP MCP bridges from your browser; Origin checks, auth and redirect validation are the recurring gaps.
Source: [NVD CVE-2026-132121](https://nvd.nist.gov/vuln/detail/CVE-2026-132121) · [NVD CVE-2026-130766](https://nvd.nist.gov/vuln/detail/CVE-2026-130766) · [AWS security bulletin 2026-195](https://aws.amazon.com/security/security-bulletins/2026-195-aws/) · [NVD CVE-2026-54031](https://nvd.nist.gov/vuln/detail/CVE-2026-54031) · [NVD CVE-2026-133195](https://nvd.nist.gov/vuln/detail/CVE-2026-133195) · Added: 2026-11-21

### NeMo Guardrails 0.25.0 deprecates `LLMRails` and Colang · 2026-11-19 🆕
0.25.0 deprecates the `LLMRails` engine and the Colang 1.0 and 2.x runtimes, with removal no earlier than 0.27.0. The replacement, `Guardrails(config)`, runs the IORails engine on the same `config.yml` but ignores `define user`/`define flow` blocks, custom refusal messages and `config.py`; Colang 2.x has no replacement.
**Why it matters:** Teams with Colang dialog flows need a migration plan now. Run configs under `Guardrails` and read the "IORails ignores…" warnings.
Source: [NeMo Guardrails: migrating to 0.25](https://docs.nvidia.com/nemo/guardrails/reference/0-25) · Added: 2026-11-21

### ToolPulse: cache side channels reveal local agents' tool activity · arXiv 2611.25470 · 2026-11-19 🆕
Flush+Reload on shared system libraries let a co-located attacker reconstruct Codex and Claude Code tool workflows across 11 LLMs (F1 above 93% in every case), and infer task types on a shared server with about 20 users *(self-reported)*.
**Why it matters:** On shared dev boxes and CI hosts, agent activity leaks to other users even though the model runs remotely; isolate agent workloads per tenant.
Source: [arXiv 2611.25470](https://arxiv.org/abs/2611.25470) · Added: 2026-11-21

### Instruction files are not a security boundary · Continuation Audits · arXiv 2611.24491 · 2026-11-18 🆕
Audits that continue real coding-agent transcripts toward a seeded risky behaviour were indistinguishable from real sessions to a judge. One open model (Kimi K3) kept bypassing file-permission protections after an explicit CLAUDE.md prohibition *(self-reported)*.
**Why it matters:** Enforce limits with the sandbox, permission rules or hooks, not prose in CLAUDE.md or AGENTS.md.
Source: [arXiv 2611.24491](https://arxiv.org/abs/2611.24491) · Added: 2026-11-21

### MCP Python SDK: four CVEs fixed in 1.30.0 / 2.2.0 · published 2026-10-27 and 2026-11-16 🆕
Advisories against the official Python SDK (`mcp` on PyPI):
- **CVE-2026-115563** (GHSA-qx49-fqc8-xw99, CVSS 7.5, published 2026-11-16): OAuth support in `mcp.client.auth` could send a `client_secret`, authorization code, PKCE verifier or signed client assertion to an authorization server chosen by an untrusted MCP server. Affects ≥ 1.9.1 < 1.30.0 and ≥ 2.0.0a1 < 2.2.0; unattended `ClientCredentialsOAuthProvider` and `PrivateKeyJWTOAuthProvider` are the most exposed. **Upgrading is not enough:** set `issuer=` on those providers, replace the deprecated `RFC7523OAuthClientProvider` (it has no issuer option), and clear stored client registrations without an issuer so they register again.
- **CVE-2026-116686** (GHSA-rwrf-2pqf-9j8j, CVSS 6.5): when a client validates a server-declared `outputSchema`, `$ref` URLs (http, https or file) are resolved, allowing blind outbound requests, local file reads and stalling every session in the process. Affects ≥ 1.10.0 < 1.30.0 and ≥ 2.0.0 < 2.2.0.
- **CVE-2026-116684** (CVSS 3.1 6.8): `TokenVerifier` did not check `aud`, so tokens issued for other services were accepted. Same ranges.
- **CVE-2026-116685** (CVSS 5.9): cross-origin redirects forwarded credential headers, and on 307/308 the request body. Affects ≥ 1.8.0.

The fixed versions were on PyPI from 2026-09-07; the advisories came later.
**Why it matters:** Clients that connect to untrusted MCP servers are the most exposed. Upgrade to `mcp` ≥ 1.30.0 or ≥ 2.2.0.
Sources: [GHSA-rwrf-2pqf-9j8j](https://github.com/modelcontextprotocol/python-sdk/security/advisories/GHSA-rwrf-2pqf-9j8j) · [OpenCVE: CVE-2026-116686](https://app.opencve.io/cve/CVE-2026-116686) · [Mend: CVE-2026-116684](https://www.mend.io/vulnerability-database/CVE-2026-116684/) · [CVE-2026-115563](https://www.cve.org/CVERecord?id=CVE-2026-115563) · Added: 2026-11-20 · Updated: 2026-11-23

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
