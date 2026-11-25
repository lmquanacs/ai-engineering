# MCP servers for software development

_Last updated: 2026-11-26_

> Model Context Protocol servers worth connecting to coding agents, plus the protocol changes that affect anyone running or building them.

## 📣 Protocol news: the 2026-07-28 spec (MCP goes stateless)

The largest revision since launch. It is now the current spec and supersedes 2025-11-25.

- **Removed:** the `initialize` handshake, `Mcp-Session-Id`, stream resumability, `ping`, `logging/setLevel`.
- **Added:** every request carries the protocol version and client capabilities in `_meta`; `Mcp-Method` / `Mcp-Name` HTTP headers so load balancers can route without reading the body; cacheable list results; a `server/discover` endpoint; a formal feature lifecycle (Active / Deprecated / Removed).
- **Auth:** remote servers are formally OAuth 2.1 resource servers.
- **SDKs:** the TypeScript, Python, Go and C# Tier 1 SDKs supported it on launch day. Codex CLI opts in per server with `protocol_version = "2026-07-28"`.
- **Spring AI 2.0:** `spring.ai.mcp.server.protocol=STATELESS`.

**Skills over MCP reaches Claude Code (2026-11-24):** the official Skills extension (`io.modelcontextprotocol/skills`, SEP-2640, now Final) lets a server list and serve `SKILL.md` skills through `skills/list`, `skills/get` and `resources/read` on 2026-07-28 connections. Claude Code 2.1.332 loads them in public beta as `<server>:<skill>`. In auto mode a classifier decides whether a skill loads without a prompt; Anthropic scans skills only from some connectors, not from servers you add with `claude mcp add`. Control them with permission rules such as `Skill(mcp__docs__*)` (deny, ask or allow) or turn them off on managed devices with `disableDirectMcpSkills`. They don't work in `claude -p`, cloud sessions, the Agent SDK or through cloud providers. ([Claude Code: use skills from MCP servers](https://code.claude.com/docs/en/mcp#use-skills-from-mcp-servers) · [MCP Skills extension](https://modelcontextprotocol.io/extensions/skills/overview) · [SEP-2640](https://modelcontextprotocol.io/seps/2640-skills-extension))

**FastMCP 4.2.6 (2026-11-25):** adds an experimental client-side `CodeModeClient` that chains tools across servers in one `execute` block. Two breaking changes: Authlib is no longer installed with fastmcp, so declare it yourself if your code imports it, and the experimental events API moved to a separate `fastmcp-events` package (`pip install "fastmcp[events]"`) with Pydantic-model event types. ([FastMCP changelog](https://raw.githubusercontent.com/PrefectHQ/fastmcp/main/docs/changelog.mdx))

**Spring AI 2.1 (2026-11-20)** speaks 2026-07-28 on both sides: set `spring.ai.mcp.server.protocol=MODERN` and existing `@McpTool`/`@McpResource`/`@McpPrompt` beans are served statelessly on WebMVC, WebFlux or STDIO, and clients can mix legacy and modern Streamable HTTP connections. ([Spring AI 2.1.0 GA](https://spring.io/blog/2026/11/20/spring-ai-2-1-0-GA-available-now) · details in [JVM libraries](../libraries/jvm.md))

**MCP Ruby SDK 1.11.0 (2026-11-19):** the Streamable HTTP transport can resume SSE streams from `Last-Event-ID` when given an `event_store:` (SEP-1699), and several OAuth issuer-validation bugs are fixed. Upgrade for the auth fixes. ([Ruby SDK changelog](https://raw.githubusercontent.com/modelcontextprotocol/ruby-sdk/main/CHANGELOG.md))

**Next spec:** from 2026-11-11 the MCP project moves to a predictable cycle of a spec release about every six months (roughly late March and September), with a Release Manager role and fixed deadlines for proposals and SDK betas. ([MCP blog](https://blog.modelcontextprotocol.io/posts/mcp-release-cycle/))

**Do this:** If you run a remote MCP server behind more than one instance, migrate, because it removes sticky sessions. Clients still negotiate older versions, but don't let that delay you.
Sources: [MCP blog: the 2026-07-28 specification](https://blog.modelcontextprotocol.io/posts/2026-07-28/) · [Cloudflare: the next generation of MCP](https://blog.cloudflare.com/mcp-v2/) · [WorkOS breakdown](https://workos.com/blog/mcp-stateless-spec-2026-07-28) · Added: 2026-11-18

---

## ⭐ Start here: the core six

Most developers need about six servers: filesystem, Git, GitHub, one database (read-only), Playwright and a live-docs server. Everything else depends on your stack. ([Scrimba](https://scrimba.com/articles/best-mcp-servers-for-developers-2026/))

### GitHub MCP Server · official
Repos, issues, PRs, code search, Actions and CI-failure investigation. It is hosted remotely, so there is nothing to run locally.
```bash
# read-only, project scope (Claude Code)
claude mcp add -s project --transport http github https://api.githubcopilot.com/mcp/readonly \
  -H 'Authorization: Bearer ${GITHUB_PAT}'
```
**Tip:** The 5 default toolsets load about 42 tools. Enable only the toolsets you need, because some clients cap at around 40 tools.
Source: [github/github-mcp-server](https://github.com/github/github-mcp-server) · ~33K ⭐ (Sep 2026) · Added: 2026-11-18

### Context7 · Upstash
Pulls current, version-specific library documentation into the prompt, so agents stop writing code against APIs that no longer exist. Only 2 tools.
Remote: `https://mcp.context7.com/mcp` · Local: `npx -y @upstash/context7-mcp`
Source: [upstash/context7](https://github.com/upstash/context7) · ~62K ⭐ · Added: 2026-11-18

### Playwright MCP · Microsoft
Browser automation from the accessibility tree: navigate, click, fill, screenshot. Agents use it to verify the UIs they build.
```bash
npx @playwright/mcp@latest
```
Source: [microsoft/playwright-mcp](https://github.com/microsoft/playwright-mcp) · ~37K ⭐ · Added: 2026-11-18

### Chrome DevTools MCP · Google
Console, network, performance traces and DOM inspection in a live Chrome. It ranked #1 in one September 2026 composite popularity leaderboard.
Source: [itechguides summary of rankings](https://www.itechguides.com/?p=868184) · Added: 2026-11-18

### Database (read-only)
- **Postgres MCP Pro**: community standard for Postgres, with schema exploration, query plans and index advice. `pipx install postgres-mcp`
- **Supabase MCP** (official, remote): `https://mcp.supabase.com/mcp`

Always connect with a **read-only role** unless the task requires writes.
Source: [mcp.so best MCP servers](https://mcp.so/blog/best-mcp-servers) · Added: 2026-11-18

### Filesystem + Git (reference servers)
Maintained by the MCP team in [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers). Several early reference servers (GitHub, Postgres, Puppeteer, Slack…) were archived in favour of vendor-official ones.

---

## 🧰 Situational picks

| Server | Use for | Endpoint / install |
|---|---|---|
| Sentry (official) | Errors, stack traces, release correlation | remote (OAuth) |
| Figma (official) | Design → code, tokens, component mapping | remote |
| GitLab (official) | GitLab instead of GitHub | `https://gitlab.com/api/v4/mcp` |
| draw.io · `jgraph/drawio-mcp` | Architecture diagrams as code; also ships a skill | `npx -y skills add jgraph/drawio-mcp --skill drawio` |
| Firecrawl / Exa | Web search and scraping into clean markdown | remote |
| Datadog (official) | Metrics, logs and traces from your agent | remote |
| **AWS MCP Server** (managed, GA May 2026) + [awslabs/mcp](https://github.com/awslabs/mcp) | Operating your AWS account: APIs, CloudWatch, IAM, EKS, CDK, Cost Explorer | `pip install awslabs-mcp-proxy` · `uvx awslabs.cloudwatch-mcp-server@latest`. See [AWS](../../platforms/aws/README.md#-aws-mcp-servers) |

## 🏗️ Build your own

- **Java/Kotlin:** Spring AI 2.0 includes MCP annotations in core (`@McpTool`, `@McpResource`, `@McpPrompt`) and the WebMVC/WebFlux transports. Start from `spring-ai-starter-mcp-server-webmvc`. ([Spring AI 2.0 GA](https://spring.io/blog/2026/06/12/spring-ai-2-0-0-GA-available-now/))
- **Plain Java:** the official [MCP Java SDK](https://java.sdk.modelcontextprotocol.io/latest/) 2.2.0 (2026-11-13, Maven Central) implements the stateless 2026-07-28 spec and the older 2025-11-25 spec in one module.
- **Python / TypeScript:** official SDKs at [modelcontextprotocol](https://github.com/modelcontextprotocol). FastMCP is popular in Python.
- **Let the agent do it:** the `mcp-builder` skill from [anthropics/skills](https://github.com/anthropics/skills).

## 🔒 Security notes

### GitLab MCP OAuth SSRF, Electerm MCP widget RCE, another AutoGPT MCP credential bug · published 2026-11-24 → 11-25 🆕
- **GitLab EE** 18.10 to before 19.4.11, 19.5 before 19.5.9 and 19.6 before 19.6.2: an authenticated user can make the MCP server's OAuth token endpoint send requests to internal hosts (CVE-2026-135221, CVSS 6.3).
- **Electerm** < 5.9.0: a web page can use DNS rebinding to reach its unauthenticated MCP Server widget on port 30837 and run commands locally and in open SSH sessions (CVE-2026-136630, CVSS 4.0 7.7).
- **AutoGPT** 0.6.49 to < 0.11.0: a shared agent's `MCPToolBlock` could use the runner's own connected MCP credentials for any read, write or delete (CVE-2026-133462).
- **pain001-mcp** 0.0.72 to < 0.0.80: path traversal in `commit_payment_batch` (CVE-2026-136620, CVSS 7.1).

**Do this:** Self-managed GitLab EE to 19.6.2 / 19.5.9 / 19.4.11; Electerm to ≥ 5.9.0 (or keep its MCP widget off); AutoGPT ≥ 0.11.0 (already required by yesterday's entry); pain001-mcp ≥ 0.0.80. Write-ups belong in [AI security](../../architecture/security/README.md).
Source: [GitLab patch release 19.6.2](https://docs.gitlab.com/releases/patches/patch-release-gitlab-19-6-2-released/) · [NVD CVE-2026-135221](https://nvd.nist.gov/vuln/detail/CVE-2026-135221) · [NVD CVE-2026-136630](https://nvd.nist.gov/vuln/detail/CVE-2026-136630) · [NVD CVE-2026-133462](https://nvd.nist.gov/vuln/detail/CVE-2026-133462) · [NVD CVE-2026-136620](https://nvd.nist.gov/vuln/detail/CVE-2026-136620) · Added: 2026-11-26

### LiteLLM MCP stdio and DBHub zero-days, plus IoTDB, AutoGPT, Sim and Chats CVEs · published 2026-11-23 → 11-24 🆕
- **LiteLLM** (ZDI-26-1031, CVE-2026-136535, CVSS 7.2): a proxy admin can run commands through MCP stdio server configs. LiteLLM disputes that it's a vulnerability and isn't shipping a separate patch. Its suggested mitigation is v1.104.0+, which turns stdio MCP servers off unless `LITELLM_ENABLE_MCP_STDIO=true` is set in the environment, plus a strong master key.
- **DBHub** (ZDI-26-1067, CVE-2026-136441, CVSS 9.8): an authorization bypass when the MCP server parses untrusted SQL, published as a 0-day after ZDI got no vendor fix. The advisory names no affected or fixed version. It's separate from the read-only bypass fixed in 1.7.0 below.
- **Apache IoTDB MCP Server** ≤ 0.2.0 writes the database password to its startup log (CVE-2026-135747); fixed in 0.3.0.
- MCP clients inside other apps: **AutoGPT** 0.6.1–0.10.0 can send a connected MCP server's credential to a third party via a crafted redirect (CVE-2026-133449, fixed in 0.11.0); **Sim** < 0.9.41 lets write-level members make workflow MCP servers public (CVE-2026-135162); **sdcb Chats** < 1.17.1 lets assigned users read other users' MCP bearer headers (CVE-2026-135432).

**Do this:** On LiteLLM, upgrade to ≥ 1.104.0 and leave `LITELLM_ENABLE_MCP_STDIO` unset unless you need stdio servers. Keep DBHub on a private network with a read-only database role until Bytebase responds. Upgrade IoTDB MCP (≥ 0.3.0), AutoGPT (≥ 0.11.0), Sim (≥ 0.9.41) and Chats (≥ 1.17.1), and rotate any password IoTDB has already logged. An Amazon ECS MCP Server redaction flaw (CVE-2026-135614, fixed in `awslabs.ecs-mcp-server` 0.1.36) is written up on the [AI security page](../../architecture/security/README.md).
Source: [ZDI-26-1031](https://www.zerodayinitiative.com/advisories/ZDI-26-1031/) · [ZDI-26-1067](https://www.zerodayinitiative.com/advisories/ZDI-26-1067/) · [NVD CVE-2026-135747](https://nvd.nist.gov/vuln/detail/CVE-2026-135747) · [GHSA-hp9v-vh5x-5jv3](https://github.com/Significant-Gravitas/AutoGPT/security/advisories/GHSA-hp9v-vh5x-5jv3) · [NVD CVE-2026-135162](https://nvd.nist.gov/vuln/detail/CVE-2026-135162) · [NVD CVE-2026-135432](https://nvd.nist.gov/vuln/detail/CVE-2026-135432) · Added: 2026-11-25

### FastMCP 4.2.5: OAuth hardening, listen streams on by default · 2026-11-23 🆕
Security fixes: a CIMD client's metadata can no longer widen allowed scopes, redirect URIs must match an allowed pattern's query exactly (and an exact root pattern now matches only that path), reusing a rotated refresh token more than 60 s later ends the whole grant, and OpenAPI tools stop forwarding MCP transport headers to the wrapped API (new `forward_client_headers`). On 2026-07-28 connections, servers now serve `subscriptions/listen` by default, so clients hold one open stream per connection (up to 1024 per process).
**Do this:** Upgrade, then check three things: set `valid_scopes` if you have CIMD clients (with no scopes configured they can now request none), add `/*` to root redirect patterns that need sub-paths, and pass `token_issuer` to a multi-tenant `AzureProvider`, which no longer checks the issuer. On serverless or small worker pools, consider `FASTMCP_ENABLE_SUBSCRIPTIONS_LISTEN=false`.
Source: [FastMCP changelog v4.2.5](https://raw.githubusercontent.com/PrefectHQ/fastmcp/main/docs/changelog.mdx) · [PyPI](https://pypi.org/project/fastmcp/) · Added: 2026-11-24

### Reference servers, Pomerium and astro-airflow-mcp CVEs · published 2026-11-23 🆕
**mcp-server-git** before 2026.10.28: a nested `.git` file pointing elsewhere bypasses `--repository` (CVE-2026-134465); already fixed if you took the 2026.11.18 upgrade below. **mcp-server-fetch** 2026.10.10 to < 2026.11.11 treats IPv6 site-local addresses as public in its SSRF guard (CVE-2026-134492, low). **Pomerium** 0.30.0 to < 0.34.0 skips client-secret checks at its MCP token endpoint, so an intercepted code or refresh token can be redeemed (CVE-2026-135300, CVSS 4.0 9.1). **astro-airflow-mcp** 0.5.0–0.9.1 can run a `json.py` from the working directory (CVE-2026-133632). Details in [AI security](../../architecture/security/README.md#-recent-items).
**Do this:** Upgrade to `mcp-server-git` ≥ 2026.11.18, `mcp-server-fetch` ≥ 2026.11.11, Pomerium ≥ 0.34.0, `astro-airflow-mcp` ≥ 0.9.2 (or set `AF_TELEMETRY_DISABLED=1`).
Source: [NVD CVE-2026-134465](https://nvd.nist.gov/vuln/detail/CVE-2026-134465) · [NVD CVE-2026-134492](https://nvd.nist.gov/vuln/detail/CVE-2026-134492) · [NVD CVE-2026-135300](https://nvd.nist.gov/vuln/detail/CVE-2026-135300) · [NVD CVE-2026-133632](https://nvd.nist.gov/vuln/detail/CVE-2026-133632) · Added: 2026-11-24

### DBHub read-only bypass, mcp-server-kubernetes flag injection, FastMCP OAuth proxy fix · 2026-11-21 → 11-22 🆕
**DBHub** (Bytebase's database MCP server) < 1.7.0 lets a client limited to read-only `execute_sql` hide write and DDL statements behind backslash-escaped quotes (CVE-2026-134803); upgrade to ≥ 1.7.0. **mcp-server-kubernetes** < 4.2.0 passes dash-prefixed values in tools such as `exec_in_pod` and `kubectl_logs` to kubectl as flags, so a client on SSE or Streamable HTTP can make kubectl read host files (CVE-2026-134817, CVSS 7.1); upgrade to ≥ 4.2.0. **FastMCP 4.2.4** (2026-11-21) fixes two concurrent requests redeeming one OAuth-proxy authorization code or refresh token twice (GHSA-78c8-3jhx-5mg7) and stops a revoked proxy access token from becoming valid again after a refresh. Details in [AI security](../../architecture/security/README.md#-recent-items).
**Do this:** Upgrade the ones you run. If you use FastMCP's OAuth proxy, move to ≥ 4.2.4.
Source: [CVE-2026-134803](https://www.cve.org/CVERecord?id=CVE-2026-134803) · [CVE-2026-134817](https://www.cve.org/CVERecord?id=CVE-2026-134817) · [FastMCP changelog](https://raw.githubusercontent.com/PrefectHQ/fastmcp/main/docs/changelog.mdx) · Added: 2026-11-23

### More MCP server CVEs: mcp-ssh-manager, SurrealDB, ArcadeDB, codebase-memory-mcp · 2026-11-18 → 11-21 🆕
Command injection in **mcp-ssh-manager** backup and DB tools, including ones allowed in read-only mode (upgrade to ≥ 3.8.5); SQL injection through **SurrealDB**'s MCP identifier check (≥ 4.0.0); writes through **ArcadeDB**'s read-only MCP query tool (≥ 26.11.1); memory-safety and argument-injection bugs in **codebase-memory-mcp** (≥ 0.9.0); unauthenticated **k8s-mcp-server** SSE on 0.0.0.0 (≥ 1.1.0) and **jupyter-mcp-server** HTTP mode (≥ 1.0.3). Details in [AI security](../../architecture/security/README.md#-recent-items).
**Do this:** Upgrade any of these you run, and don't treat a server's "read-only" mode as a security boundary.
Source: [CVE-2026-129995](https://www.cve.org/CVERecord?id=CVE-2026-129995) · [CVE-2026-134293](https://www.cve.org/CVERecord?id=CVE-2026-134293) · Added: 2026-11-22

### MCP bridge and server CVE wave · Supergateway, Obot, LibreChat · 2026-11-18 → 11-20 🆕
NVD published a batch of MCP-related CVEs: **Supergateway** cross-site WebSocket hijacking in stdio-to-WebSocket mode (CVE-2026-132121, 2.4.0–4.2.2) and a DoS in stdio-to-SSE mode (CVE-2026-131857); **Obot** < 0.27.0; **LibreChat** < 0.8.8 (MCP OAuth redirect SSRF). Upgrade lines and the AWS document-loader server are in [AI security](../../architecture/security/README.md#-recent-items).
**Update 2026-11-24:** Supergateway **4.2.3** and **4.2.4** (2026-11-23) are on npm. In the published code, SSE sessions are now kept in a `Map` (the DoS used prototype keys), and WebSocket upgrades from a browser `Origin` not listed in `--cors` get a 403. The WebSocket check is opt-in: with neither `--cors <origins>` nor `--apiKey`, any web page can still connect, and the gateway only prints a warning. No release notes or advisory update yet.
**Update 2026-11-25:** Supergateway **4.3.0** (npm, 2026-11-24) closes the opt-in gap for local use. Without `--apiKey`, browser requests that reach the gateway on a loopback address are refused (403) when they come through DNS rebinding (SSE, WebSocket and Streamable HTTP), or, without `--cors`, from a web page on another site over WebSocket. Pages on `localhost` and browser extensions still connect, and clients that aren't browsers are unaffected. This comes from the published package's README and code; there are still no release notes.
**Do this:** Upgrade to ≥ 4.3.0. If other machines, containers or a proxy can reach the gateway, still set `--apiKey`. If you serve a page through a tunnel on this machine on a public name, allow it with `--cors <origin>`.
Source: [NVD CVE-2026-132121](https://nvd.nist.gov/vuln/detail/CVE-2026-132121) · [supergateway on npm](https://www.npmjs.com/package/supergateway?activeTab=versions) · Added: 2026-11-21 · Updated: 2026-11-25

### MCP Python SDK: four CVEs fixed in 1.30.0 / 2.2.0 · published 2026-10-27 and 2026-11-16 🆕
CVE-2026-116686 (schema `$ref` SSRF and file reads), CVE-2026-116684 (no token-audience check), CVE-2026-116685 (credentials sent on cross-origin redirects) and CVE-2026-115563 (OAuth clients could send credentials to an authorization server the MCP server chose).
**Do this:** run `mcp` ≥ 1.30.0 (1.x) or ≥ 2.2.0 (2.x). For CVE-2026-115563 upgrading isn't enough: set `issuer=` on `ClientCredentialsOAuthProvider`/`PrivateKeyJWTOAuthProvider`, replace the deprecated `RFC7523OAuthClientProvider`, and clear stored client registrations that lack an issuer. Details → [AI security](../../architecture/security/README.md#-recent-items)
Source: [CVE-2026-115563](https://www.cve.org/CVERecord?id=CVE-2026-115563) · Added: 2026-11-20 · Updated: 2026-11-23

### MCP TypeScript SDK: four CVEs fixed in 1.32.0 / 2.3.0 · 2026-10-20 🆕
Advisories published on 2026-10-20 cover the official TypeScript SDK:
- **CVE-2026-111768** (CVSS 7.5): one request within the default 4 MiB limit can exhaust heap during tool-input validation and crash the server. No credentials needed. Fixed in `@modelcontextprotocol/sdk` 1.32.0 / `@modelcontextprotocol/server` 2.3.0.
- **CVE-2026-111770** (CVSS 7.7): a shared stateless transport or shared `McpServer` instance can send one client's responses to another, because JSON-RPC ids collide. Fixed in `server` 2.3.0.
- **CVE-2026-111771** (CVSS 6.8): bearer auth didn't check the token's audience, so tokens issued for other services were accepted. Fixed in `sdk` 1.32.0.
- **CVE-2026-111769** (CVSS 6.5): HTTP client transports and OAuth requests followed cross-origin redirects, leaking custom headers and, on 307/308, request bodies with refresh tokens. Fixed in `sdk` 1.32.0.

**Do this:** If you run a remote TypeScript MCP server, upgrade to `sdk` ≥ 1.32.0 or `server` ≥ 2.3.0. Then create a server and transport per request or session rather than sharing one.
Sources: [GitLab advisory: CVE-2026-111768](https://advisories.gitlab.com/npm/@modelcontextprotocol/sdk/CVE-2026-111768/) · [CVE-2026-111770](https://advisories.gitlab.com/npm/@modelcontextprotocol/server/CVE-2026-111770/) · [CVE-2026-111771](https://advisories.gitlab.com/npm/@modelcontextprotocol/sdk/CVE-2026-111771/) · [CVE-2026-111769](https://advisories.gitlab.com/npm/@modelcontextprotocol/sdk/CVE-2026-111769/) · Added: 2026-11-19

### mcp-go: OAuth token-replay flaw fixed in v1.2.1 · 2026-11-05 🆕
**CVE-2026-123272** in `mark3labs/mcp-go` (≥ v0.48.0, < v1.2.1): `OAuthHandler.fetchServerMetadata` trusted the resource a malicious server declared in its well-known metadata. That server could get a token minted for a *different* MCP server and replay it there.
**Do this:** Go MCP clients using mcp-go's OAuth handler should upgrade to v1.2.1.
Source: [VulnCheck advisory](https://www.vulncheck.com/advisories/mcp-go-before-1.2.1-origin-validation-error-via-unvalidated-well-known-protected-resource-metadata) · CVSS 4.0 5.1 · Added: 2026-11-19

**Background:**
- More than 30 CVEs were filed against MCP servers in January–February 2026 alone. ([Toolradar](https://toolradar.com/blog/best-mcp-servers-2026))
- Trend Micro found that 48% of more than 19,000 MCP server codebases recommend storing secrets in `.env` files or plaintext JSON. Prefer OAuth or scoped tokens. ([Amplitude summary](https://amplitude.com/compare/best-mcp-servers))
- The official registry lists more than 30,000 servers but checks namespaces, not quality. Prefer vendor-official servers.
→ More in [AI security](../../architecture/security/README.md)
