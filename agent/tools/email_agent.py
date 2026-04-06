"""
Email Automation Tool
Automate email processing, filtering, and responses
"""

import json
from datetime import datetime
from typing import List, Dict, Optional
from dataclasses import dataclass

@dataclass
class Email:
    sender: str
    subject: str
    body: str
    timestamp: str
    labels: List[str] = None

    def __post_init__(self):
        if self.labels is None:
            self.labels = []

class EmailAgent:
    """AI-powered email automation"""

    def __init__(self):
        self.rules: List[Dict] = []
        self.processed: List[Email] = []

    def add_rule(self, condition: str, action: str):
        """Add processing rule: if condition → do action"""
        self.rules.append({"condition": condition, "action": action})

    def classify(self, email: Email) -> str:
        """Classify email by content"""
        subject_lower = email.subject.lower()
        body_lower = email.body.lower()

        if any(w in subject_lower for w in ["invoice", "payment", "order"]):
            return "finance"
        elif any(w in subject_lower for w in ["urgent", "asap", "immediately"]):
            return "urgent"
        elif any(w in body_lower for w in ["unsubscribe", "opt-out"]):
            return "marketing"
        else:
            return "general"

    def generate_reply(self, email: Email, tone: str = "professional") -> str:
        """Generate auto-reply template"""
        templates = {
            "professional": f"Thank you for your email regarding '{email.subject}'. I'll review and respond within 24 hours.",
            "friendly": f"Hey! Got your message about '{email.subject}'. I'll get back to you soon!",
            "brief": f"Received. Will respond shortly."
        }
        return templates.get(tone, templates["professional"])

    def process(self, email: Email) -> Dict:
        """Process a single email"""
        category = self.classify(email)
        email.labels.append(category)
        self.processed.append(email)

        return {
            "email": email.subject,
            "category": category,
            "suggested_reply": self.generate_reply(email),
            "processed_at": datetime.now().isoformat()
        }

    def batch_process(self, emails: List[Email]) -> List[Dict]:
        """Process multiple emails at once"""
        return [self.process(e) for e in emails]


if __name__ == "__main__":
    agent = EmailAgent()

    # Demo
    emails = [
        Email("client@example.com", "Invoice #1234", "Please find attached invoice.", "2026-04-06"),
        Email("boss@company.com", "URGENT: Server down", "Production is down!", "2026-04-06"),
        Email("newsletter@spam.com", "Weekly deals", "Unsubscribe here", "2026-04-06"),
    ]

    results = agent.batch_process(emails)
    for r in results:
        print(f"[{r['category'].upper()}] {r['email']}")
        print(f"  → {r['suggested_reply']}\n")
