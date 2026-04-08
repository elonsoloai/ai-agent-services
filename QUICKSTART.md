# Quick Start Guide

> Get your AI agent running in 5 minutes

## Prerequisites

```bash
pip install -r requirements.txt
```

## Run the Demo

```bash
cd agent
python examples/demo.py
```

## Configuration

Create a `.env` file:

```env
# API Keys (optional for demo)
OPENAI_API_KEY=your_key_here

# Email (optional)
SMTP_EMAIL=your@email.com
SMTP_PASSWORD=your_password

# Web Scraping (optional)
BROWSER_API_KEY=your_key_here
```

## Available Agents

| Agent | Purpose | Status |
|-------|---------|--------|
| `web_agent.py` | Web scraping & research | ✅ Ready |
| `email_agent.py` | Email automation | ✅ Ready |
| `data_agent.py` | Data processing | ✅ Ready |
| `scheduler_agent.py` | Calendar management | ✅ Ready |
| `report_generator.py` | Report generation | ✅ Ready |
| `notification_manager.py` | Multi-channel alerts | ✅ Ready |

## Next Steps

1. Read the [Starter Template](./STARTER_TEMPLATE.md)
2. Check the [Blog Posts](./blog/)
3. Join our [Discussions](https://github.com/elonsoloai/ai-agent-services/discussions)

---

*Questions? Open an issue!*
