# Voice & multimodal

_Last updated: 2026-11-23_

> Building beyond text chat: realtime voice agents, speech-to-text and text-to-speech, vision and document understanding, and agents that drive a screen or browser.

## 🧭 Voice agent architectures

| Approach | How it works | Trade-off |
|---|---|---|
| **Cascaded (STT → LLM → TTS)** | Three models chained, often with streaming between them | Most control (swap any part, inspect text, use any LLM); latency adds up across hops |
| **Speech-to-speech (realtime APIs)** | One model takes and returns audio | Lowest latency and keeps tone; less control and harder to debug or evaluate |
| **Hybrid** | Realtime model for conversation, text LLM for tool-heavy reasoning | Best of both, more moving parts |

**What breaks in production:** turn-taking and interruptions (barge-in), latency budgets per hop, telephony audio quality, and evaluating conversations rather than single replies. Frameworks such as Pipecat and LiveKit Agents handle transport, voice activity detection and turn-taking for you.

## 🧭 Vision, documents & computer use

- **Documents:** for PDFs with tables and charts, compare a vision model reading page images against a parser + text model; the right answer depends on layout complexity. → [RAG & retrieval](../../architecture/rag-and-retrieval/README.md)
- **Computer and browser use:** powerful but slow and costly per task; run it in a sandbox and with narrow permissions. → [Agent infrastructure](../../architecture/agent-infrastructure/README.md) · [AI security](../../architecture/security/README.md)

---

## ⏰ Action items

| Date | What | Do |
|---|---|---|
| 2026-11-26 | ElevenAgents API (`/v1/convai`) starts enforcing server-side request timeouts; slow requests can return HTTP 504 | Retry 504s with backoff |
| 2026-12-13 | Vertex AI support for `gemini-live-2.5-flash-native-audio` retires | Migrate to Gemini 3.8 Live ([model page](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/models/gemini/2-5-flash-live-api)) |
| 2026-12-15 | ElevenLabs agents on `gpt-4.1`, `gpt-4.1-mini`, `gpt-4o` or `gpt-4o-mini` start sending 10% of requests to `gpt-6-luna` (all from 2027-01-09; shutdown 2027-01-14) | Pick and test a replacement LLM now |

## 🗞️ Latest

<!-- newest first: realtime/STT/TTS releases and prices, voice frameworks, vision and computer-use changes -->

### Deepgram: pay per request through AWS Marketplace with x402 · 2026-11-20 🆕
Agents can now buy Deepgram Nova-3 speech-to-text, Flux TTS and Aura-2 text-to-speech per request through AWS Marketplace, paying over x402 with no Deepgram API key; charges land on the AWS account. In the same week Nova-3 gained 36 new monolingual languages (2026-11-16) and improved models for German and Hindi (2026-11-17), and improved models for 15 more languages on 2026-11-12.
**Why it matters:** An agent can use speech services without you issuing and storing another vendor key, which suits AgentCore's new agentic payments ([AWS](../../platforms/aws/README.md)). Set spending limits first. If you use the Deepgram CLI's MCP server, note that `dg mcp` dropped the SSE transport in CLI 0.4.1.
Source: [Deepgram changelog](https://developers.deepgram.com/changelog) · Added: 2026-11-23

### browser-use 1.0: rewritten engine, cloud browser by default · 1.0.7 on 2026-11-21 🆕
The open-source browser-agent library reached 1.0 on 2026-11-10 and has shipped point releases since (1.0.7 on 2026-11-21). Per the PyPI docs, `Browser()` now starts a Browser Use **Cloud** browser by default and the default model is `bu-4.0` on the Browser Use gateway, both using one `BROWSER_USE_API_KEY`. A local browser is `Browser('chromium')`. Requires Python 3.11+.
**Why it matters:** An unpinned `pip install browser-use` now moves you from 0.x to 1.0, and with default settings, pages and prompts go to Browser Use's cloud. Pin the version, pass an explicit local browser and LLM if data must stay with you, and read the project's MIGRATING.md before upgrading.
```bash
pip install 'browser-use==1.0.7'
```
Source: [PyPI: browser-use](https://pypi.org/project/browser-use/) · 1.0.0 released 2026-11-10 · Added: 2026-11-23

### ElevenLabs: cheaper Scribe pricing, agent timeouts and LLM fallbacks · 2026-11-16/17 🆕
Speech to Text now costs $0.20 per hour of audio for batch and $0.22 per hour for realtime, for every Scribe model on self-serve and Business plans (Enterprise unchanged). That includes Scribe v3 (`scribe_v3`) and Scribe v3 Live (`scribe_v3_live`), released 2026-11-09. Also: the ElevenAgents API enforces request timeouts from 2026-11-26, the GPT-4.1/4o agent LLMs move to `gpt-6-luna` on a schedule, and stream-input WebSockets now close with 1008 `model_not_found` for an unknown `model_id` (previously 1011).
**Why it matters:** Re-run your STT cost comparison. Agents must handle 504s, and any client that checks WebSocket close codes needs updating. Dates are in the action items above.
Source: [ElevenLabs changelog, 2026-11-17](https://elevenlabs.io/docs/changelog/2026/11/17) · [Changelog](https://elevenlabs.io/docs/changelog) · Added: 2026-11-23

### Pipecat 1.16.0 and LiveKit Agents 1.8.13: framework upgrades · 2026-11-12 / 2026-11-18 🆕
**Pipecat 1.16.0** (2026-11-12) has several breaking changes. A function call that returns `""`, `{}` or `False` now triggers an LLM reply (return `None` to finish silently). Diarization moves from `user_id` to `frame.speaker`. `resampy`, `soxr` and `audioop-lts` are no longer core dependencies. `SonioxSTTService` defaults to `stt-rt-v6`. New: Zoom AI realtime speech-to-speech, HeyGen TTS, Rime STT, and `EvalRubric` for judging conversations. **LiveKit Agents** reached 1.8.13 on 2026-11-18, alongside a 2.0.0b2 pre-release; its docs cover OpenAI GPT-Live with backend delegation through the OpenAI plugin or LiveKit Inference.
**Why it matters:** Check tool handlers that return empty values before upgrading Pipecat, because they will now make the bot speak. Treat LiveKit 2.0 as a beta to test, not to deploy. GPT-Live API changes: [LLM APIs](../llm-apis/README.md).
```bash
uv add "livekit-agents[openai]~=1.8"
```
Sources: [PyPI: pipecat-ai](https://pypi.org/project/pipecat-ai/) · [Pipecat releases](https://github.com/pipecat-ai/pipecat/releases) · [PyPI: livekit-agents](https://pypi.org/project/livekit-agents/) · [LiveKit docs: GPT-Live](https://docs.livekit.io/agents/models/realtime/gpt-live) · Added: 2026-11-23

**Elsewhere this week:** Amazon Textract Insights for schema-driven document extraction is on the [AWS](../../platforms/aws/README.md) page. The Anthropic computer-use tool migration to `computer_toolset_20260801` is on the [LLM APIs](../llm-apis/README.md) page.

## 📚 Reference

<!-- older or background entries -->
