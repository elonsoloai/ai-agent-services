"""
Scheduler Agent
Run tasks on a schedule without manual intervention
"""

import time
import threading
from datetime import datetime, timedelta
from typing import Callable, List, Dict, Optional
from dataclasses import dataclass

@dataclass
class ScheduledTask:
    name: str
    func: Callable
    interval_seconds: int
    last_run: Optional[datetime] = None
    run_count: int = 0
    enabled: bool = True

class SchedulerAgent:
    """Run tasks automatically on a schedule"""

    def __init__(self):
        self.tasks: List[ScheduledTask] = []
        self.running = False
        self._thread: Optional[threading.Thread] = None
        self.log: List[Dict] = []

    def add_task(self, name: str, func: Callable, interval_seconds: int):
        """Add a task to run every N seconds"""
        task = ScheduledTask(
            name=name,
            func=func,
            interval_seconds=interval_seconds
        )
        self.tasks.append(task)
        print(f"Scheduled: '{name}' every {interval_seconds}s")
        return task

    def _should_run(self, task: ScheduledTask) -> bool:
        if not task.enabled:
            return False
        if task.last_run is None:
            return True
        elapsed = (datetime.now() - task.last_run).total_seconds()
        return elapsed >= task.interval_seconds

    def _run_task(self, task: ScheduledTask):
        try:
            result = task.func()
            task.last_run = datetime.now()
            task.run_count += 1
            self.log.append({
                "task": task.name,
                "status": "success",
                "result": str(result)[:100],
                "timestamp": task.last_run.isoformat()
            })
        except Exception as e:
            self.log.append({
                "task": task.name,
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            })

    def _loop(self):
        while self.running:
            for task in self.tasks:
                if self._should_run(task):
                    self._run_task(task)
            time.sleep(1)

    def start(self):
        """Start the scheduler in background"""
        self.running = True
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()
        print(f"Scheduler started with {len(self.tasks)} tasks")

    def stop(self):
        """Stop the scheduler"""
        self.running = False
        print("Scheduler stopped")

    def status(self) -> List[Dict]:
        """Get status of all tasks"""
        return [{
            "name": t.name,
            "interval": f"every {t.interval_seconds}s",
            "last_run": t.last_run.isoformat() if t.last_run else "never",
            "run_count": t.run_count,
            "enabled": t.enabled
        } for t in self.tasks]


if __name__ == "__main__":
    scheduler = SchedulerAgent()

    # Demo tasks
    def check_emails():
        return f"Checked emails at {datetime.now().strftime('%H:%M:%S')}"

    def generate_report():
        return f"Report generated at {datetime.now().strftime('%H:%M:%S')}"

    scheduler.add_task("email_check", check_emails, interval_seconds=5)
    scheduler.add_task("daily_report", generate_report, interval_seconds=10)

    scheduler.start()

    # Run for 15 seconds
    time.sleep(15)
    scheduler.stop()

    print("\nTask Status:")
    for s in scheduler.status():
        print(f"  {s['name']}: ran {s['run_count']} times, last: {s['last_run']}")
