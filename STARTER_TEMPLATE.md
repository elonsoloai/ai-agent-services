# AI Agent Services — Starter Project Template

A minimal template for building custom AI agents with Claude/OpenAI.

## Quick Start

```bash
# Clone
git clone https://github.com/elonsoloai/ai-agent-services.git
cd ai-agent-services

# Install
pip install -r requirements.txt

# Configure
cp .env.example .env
# Add your API keys

# Run
python agent.py
```

## What's Included

- **Agent base class** — State management, task tracking
- **Tool framework** — Easy tool registration
- **Memory system** — Conversation history
- **Error handling** — Retry logic, rate limiting

## Architecture

```
agent/
├── core/
│   ├── agent.py      # Main agent loop
│   ├── memory.py     # State persistence
│   └── tools.py      # Tool registry
├── tools/
│   ├── web.py        # Web scraping
│   ├── email.py      # Email operations
│   └── data.py       # Data processing
└── examples/
    └── demo.py       # Example usage
```

## Principles (Learned from Claude Code)

1. **Explicit state** — Every action logged
2. **Boring over clever** — Simple solutions work
3. **User visibility** — Client sees everything

---

*Work in progress. Star to follow updates.*
