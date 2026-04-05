"""
Demo: Full AI Agent Example
"""

import sys
import os

# Add parent to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.agent import Agent
from tools.web import WebTool


def main():
    # Create agent
    agent = Agent(name="WebScraperAgent")

    # Register tools
    web = WebTool()
    agent.register_tool("web_fetch", web.fetch)
    agent.register_tool("web_extract_text", web.extract_text)

    print(f"Agent: {agent.name}")
    print(f"Tools: {list(agent.tools.keys())}")
    print()

    # Add tasks
    t1 = agent.add_task("Fetch example.com")
    t2 = agent.add_task("Extract content")
    t3 = agent.add_task("Save results")

    # Execute
    agent.start_task(t1.id)
    html = web.fetch("https://example.com")
    if html:
        agent.complete_task(t1.id)
        print(f"✓ {t1.description}")

        agent.start_task(t2.id)
        text = web.extract_text(html)
        agent.complete_task(t2.id)
        print(f"✓ {t2.description}")

        agent.start_task(t3.id)
        agent.save_state("demo_output.json")
        with open("demo_content.txt", "w") as f:
            f.write(text)
        agent.complete_task(t3.id)
        print(f"✓ {t3.description}")

    # Final status
    print(f"\nFinal Status: {agent.get_status()}")


if __name__ == "__main__":
    main()
