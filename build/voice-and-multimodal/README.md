# Voice & multimodal

_Last updated: 2026-11-20_

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

## 🗞️ Latest

<!-- newest first: realtime/STT/TTS releases and prices, voice frameworks, vision and computer-use changes -->

## 📚 Reference

<!-- older or background entries -->
