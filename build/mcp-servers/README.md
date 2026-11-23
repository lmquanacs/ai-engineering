# MCP servers for software development

_Last updated: 2026-11-24_

> Model Context Protocol servers worth connecting to coding agents, plus the protocol changes that affect anyone running or building them.

## 📣 Protocol news: the 2026-07-28 spec (MCP goes stateless)

The largest revision since launch. It is now the current spec and supersedes 2025-11-25.

- **Removed:** the `initialize` handshake, `Mcp-Session-Id`, stream resumability, `ping`, `logging/setLevel`.
- **Added:** every request carries the protocol version and client capabilities in `_meta`; `Mcp-Method` / `Mcp-Name` HTTP headers so load balancers can route without reading the body; cacheable list results; a `server/discover` endpoint; a formal feature lifecycle (Active / Deprecated / Removed).
- **Auth:** remote servers are formally OAuth 2.1 resource servers.
- **SDKs:** the TypeScript, Python, Go and C# Tier 1 SDKs supported it on launch day. Codex CLI opts in per server with `protocol_version = "2026-07-28"`.
- **Spring AI 2.0:** `spring.ai.mcp.server.protocol=STATELESS`.

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
**Do this:** Upgrade to ≥ 4.2.4 and start stdio-to-WebSocket mode with `--cors <your origins>` or `--apiKey`.
Source: [NVD CVE-2026-132121](https://nvd.nist.gov/vuln/detail/CVE-2026-132121) · [supergateway on npm](https://www.npmjs.com/package/supergateway?activeTab=versions) · Added: 2026-11-21 · Updated: 2026-11-24

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
