"""
AI Agent Base Class
Minimal implementation with state management and task tracking
"""

import json
import os
from datetime import datetime
from typing import Optional, List, Dict, Any
from dataclasses import dataclass, asdict
from enum import Enum

class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

@dataclass
class Task:
    id: str
    description: str
    status: TaskStatus = TaskStatus.PENDING
    created_at: str = ""
    completed_at: str = ""

    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()

@dataclass
class Memory:
    """Simple conversation memory"""
    messages: List[Dict[str, str]]

    def add(self, role: str, content: str):
        self.messages.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })

    def get_context(self, max_messages: int = 10) -> List[Dict[str, str]]:
        """Get recent messages for context"""
        return self.messages[-max_messages:]

class Agent:
    """Base AI Agent with task tracking"""

    def __init__(self, name: str = "Agent"):
        self.name = name
        self.tasks: List[Task] = []
        self.memory = Memory(messages=[])
        self.tools: Dict[str, Any] = {}

    def add_task(self, description: str) -> Task:
        """Add a new task to track"""
        task = Task(
            id=f"task_{len(self.tasks) + 1}",
            description=description
        )
        self.tasks.append(task)
        return task

    def start_task(self, task_id: str):
        """Mark task as in progress"""
        for task in self.tasks:
            if task.id == task_id:
                task.status = TaskStatus.IN_PROGRESS
                return task
        return None

    def complete_task(self, task_id: str):
        """Mark task as completed"""
        for task in self.tasks:
            if task.id == task_id:
                task.status = TaskStatus.COMPLETED
                task.completed_at = datetime.now().isoformat()
                return task
        return None

    def register_tool(self, name: str, func: callable):
        """Register a tool function"""
        self.tools[name] = func

    def get_status(self) -> Dict[str, Any]:
        """Get current agent status"""
        completed = sum(1 for t in self.tasks if t.status == TaskStatus.COMPLETED)
        in_progress = sum(1 for t in self.tasks if t.status == TaskStatus.IN_PROGRESS)
        pending = sum(1 for t in self.tasks if t.status == TaskStatus.PENDING)

        return {
            "name": self.name,
            "total_tasks": len(self.tasks),
            "completed": completed,
            "in_progress": in_progress,
            "pending": pending
        }

    def save_state(self, filepath: str):
        """Save agent state to file"""
        state = {
            "name": self.name,
            "tasks": [asdict(t) for t in self.tasks],
            "memory": self.memory.messages
        }
        with open(filepath, 'w') as f:
            json.dump(state, f, indent=2)

    def load_state(self, filepath: str):
        """Load agent state from file"""
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                state = json.load(f)
            self.name = state.get("name", self.name)
            self.tasks = [
                Task(**{**t, "status": TaskStatus(t["status"])})
                for t in state.get("tasks", [])
            ]
            self.memory.messages = state.get("memory", [])


if __name__ == "__main__":
    # Demo
    agent = Agent(name="DemoAgent")

    # Add tasks
    t1 = agent.add_task("Analyze client data")
    t2 = agent.add_task("Generate report")

    # Start first task
    agent.start_task(t1.id)
    print(f"Started: {t1.description}")

    # Complete first task
    agent.complete_task(t1.id)
    print(f"Completed: {t1.description}")

    # Status
    print(f"\nStatus: {agent.get_status()}")

    # Save
    agent.save_state("agent_state.json")
    print("\nState saved to agent_state.json")
