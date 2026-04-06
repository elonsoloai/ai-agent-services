"""
Data Processing Agent
Clean, transform, and analyze business data automatically
"""

import csv
import json
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class DataReport:
    total_rows: int
    cleaned_rows: int
    duplicates_removed: int
    issues_found: List[str]
    summary: Dict[str, Any]

class DataAgent:
    """Automated data cleaning and analysis"""

    def __init__(self):
        self.issues: List[str] = []

    def load_csv(self, filepath: str) -> List[Dict]:
        """Load CSV file"""
        rows = []
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                rows.append(dict(row))
        return rows

    def clean(self, data: List[Dict]) -> List[Dict]:
        """Clean data: remove empty rows, strip whitespace"""
        cleaned = []
        for row in data:
            # Strip whitespace from all values
            row = {k: v.strip() if isinstance(v, str) else v for k, v in row.items()}
            # Skip completely empty rows
            if any(v for v in row.values()):
                cleaned.append(row)
        return cleaned

    def remove_duplicates(self, data: List[Dict], key: str) -> List[Dict]:
        """Remove duplicate rows based on key field"""
        seen = set()
        unique = []
        for row in data:
            val = row.get(key, "")
            if val not in seen:
                seen.add(val)
                unique.append(row)
        return unique

    def validate(self, data: List[Dict], required_fields: List[str]) -> List[str]:
        """Check for missing required fields"""
        issues = []
        for i, row in enumerate(data):
            for field in required_fields:
                if not row.get(field):
                    issues.append(f"Row {i+1}: missing '{field}'")
        return issues

    def summarize(self, data: List[Dict]) -> Dict[str, Any]:
        """Generate data summary"""
        if not data:
            return {}

        fields = list(data[0].keys())
        summary = {"total": len(data), "fields": fields}

        # Count non-empty values per field
        for field in fields:
            filled = sum(1 for row in data if row.get(field))
            summary[f"{field}_filled"] = f"{filled}/{len(data)}"

        return summary

    def process(self, data: List[Dict], key_field: str = "id",
                required_fields: List[str] = None) -> DataReport:
        """Full processing pipeline"""
        original_count = len(data)

        # Clean
        cleaned = self.clean(data)

        # Remove duplicates
        deduped = self.remove_duplicates(cleaned, key_field)
        duplicates_removed = len(cleaned) - len(deduped)

        # Validate
        issues = self.validate(deduped, required_fields or [])

        # Summarize
        summary = self.summarize(deduped)

        return DataReport(
            total_rows=original_count,
            cleaned_rows=len(deduped),
            duplicates_removed=duplicates_removed,
            issues_found=issues,
            summary=summary
        )


if __name__ == "__main__":
    agent = DataAgent()

    # Demo with sample data
    sample_data = [
        {"id": "001", "name": "  Alice  ", "email": "alice@example.com"},
        {"id": "002", "name": "Bob", "email": "bob@example.com"},
        {"id": "001", "name": "Alice", "email": "alice@example.com"},  # duplicate
        {"id": "003", "name": "", "email": ""},  # empty
        {"id": "004", "name": "Charlie", "email": ""},  # missing email
    ]

    report = agent.process(sample_data, key_field="id", required_fields=["name", "email"])

    print(f"Total rows: {report.total_rows}")
    print(f"After cleaning: {report.cleaned_rows}")
    print(f"Duplicates removed: {report.duplicates_removed}")
    print(f"Issues found: {len(report.issues_found)}")
    for issue in report.issues_found:
        print(f"  - {issue}")
    print(f"Summary: {json.dumps(report.summary, indent=2)}")
