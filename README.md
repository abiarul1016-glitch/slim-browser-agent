# slim-browser-agent

A slim browser agent that maximizes browsing speed and efficiency.

---

<!-- colour purple - 300059 -->

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
[![Ollama](https://img.shields.io/badge/Ollama-fff?style=for-the-badge&logo=ollama&logoColor=000)](#)
[![Playwright](https://custom-icon-badges.demolab.com/badge/Playwright-2EAD33?style=for-the-badge&logo=playwright&logoColor=fff)](#)
![Qwen](https://custom-icon-badges.demolab.com/badge/Qwen-605CEC?style=for-the-badge&logo=qwen&logoColor=fff)

---

## What and why?

MCP servers, as great as they are for extending your model's functionality, are typically too large and clunky, heavily slowing your model down by increasing its overhead. It was due to this same problem that I faced with Playwright's MCP server and Chrome DevTools MCP server that led me to create this slimmed-down browser agent.

By allowing the agent to only access a maximum of **three simple tools** — navigating to URLs, extracting the visible text from a page, and clicking a button with certain text (only if enabled) — the reasoning overhead on the model is greatly reduced, increasing its performance. Furthermore, since we force it to use tools such as navigating via URLs (the clicking function is turned off by default and can be enabled manually for more complex tasks), and since the LLM understands URL structures and how additional parameters can be passed in as an HTTP GET request, we completely avoid the issue of creating an element tree for the model, having it decide which element to click, and worst of all, loading it all into memory each time.

Admittedly, on much more powerful machines, these issues are not that grave. But when running models locally, the savings this slimmed edition allows for are greatly noticeable — allowing browsing tasks to be completed in the background with minimum resource utilization. Most importantly, due to these savings, the immense data analysis capabilities of the LLM are retained, as it can focus more on returning a detailed response rather than waiting infinitely to decide which button to click.

---

## What is it?

Browser agents are often bloated with dozens of tools, leaving the LLM confused about which one to use. **slim-browser-agent** takes a different approach: a minimal, focused toolset of at most **three tools** so the model can act quickly and decisively.

Paste a task, and the agent navigates, extracts text, and clicks — iterating with the LLM until the job is done.

---

## Features

- **Minimal tool set** — only `navigate_to_url`, `extract_text_from_page`, and optionally `click_button_with_text`. Fewer tools mean less model confusion and faster decisions.
- **Local-first AI** — runs entirely on-device via Ollama (Qwen 3.5 / Qwen 3.6 models). No API keys, no cloud dependencies.
- **Persistent browser state** — cookies and storage are saved to `state.json`, so the agent picks up where it left off across sessions.
- **Iterative reasoning loop** — the agent alternates between tool calls and LLM inference until it reaches a final answer.
- **Toggleable click mode** — enable or disable the click tool via a single `CLICK` flag for lighter or heavier browsing.

---

## How it works

Initially, the program was written as a simple `while` loop, allowing the model via Ollama to keep calling tools to answer a query. It was later refactored into classes — `BrowserManager` and `WebAgent` — so the page context did not need to be juggled around, rapidly improving the performance of the application.

The agent runs a ReAct-style loop:

1. The user provides a task via the CLI prompt.
2. The LLM receives the task along with the page text (or previous tool results) and decides which tool to call, if any.
3. The selected tool executes against the Playwright browser instance.
4. The tool result is fed back to the LLM, and the cycle repeats.
5. When the LLM decides no more tools are needed, it returns a final answer.

By limiting the tool set to three or fewer, the model spends less time reasoning about _which_ tool to use and more time actually solving the task.

---

## Tech stack

| Layer                  | Technology                   | Purpose                                          |
| ---------------------- | ---------------------------- | ------------------------------------------------ |
| **Language**           | Python 3.12+                 | Agent orchestration and LLM integration          |
| **Local LLM**          | Ollama (Qwen 3.5 / Qwen 3.6) | On-device reasoning and tool selection           |
| **Browser Automation** | Playwright (Sync API)        | Headful Chromium browsing with state persistence |

---

## Running locally

```bash
# Clone the repo
git clone https://github.com/yourusername/slim-browser-agent.git
cd slim-browser-agent

# Install dependencies
pip install -r requirements.txt
# or
uv pip install -r requirements.txt

# Start the agent
python slim_browser_agent.py
```

Then answer prompts in the CLI. Type `quit` to exit.

> **Note:** Make sure Ollama is running locally with the desired model pulled (e.g., `ollama pull qwen3.6:35b-a3b-coding-nvfp4`).

---

## Project structure

```
slim_browser_agent.py   # Main agent logic: BrowserManager + WebAgent classes
browser_tools.py        # Playwright tool definitions (navigate, extract, click)
state.json              # Saved browser cookies and storage
playwright/             # Playwright auth state directory
```

---

## What's next

- [ ] Add more tools (e.g., fill forms, download files) while keeping the total ≤ 3
- [ ] Support headless mode for background automation
- [ ] Add structured output parsing for extracted data
- [ ] Export browsing sessions as markdown reports

---

<div align="center">

browse light. • 🪶

_Slim tools. Fast browsing. No bloat._

</div>
