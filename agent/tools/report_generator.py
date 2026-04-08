"""
AI Agent: Report Generator
Auto-generates business reports from data sources
"""

import json
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path


class ReportGenerator:
    """Generate automated business reports"""
    
    def __init__(self, output_dir: str = "reports"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
    
    def generate_sales_report(
        self,
        data: List[Dict],
        period: str = "monthly",
        format: str = "markdown"
    ) -> str:
        """Generate sales report from order data"""
        
        total_revenue = sum(item.get('amount', 0) for item in data)
        total_orders = len(data)
        avg_order = total_revenue / total_orders if total_orders > 0 else 0
        
        # Top products
        products = {}
        for item in data:
            name = item.get('product', 'Unknown')
            products[name] = products.get(name, 0) + item.get('quantity', 0)
        top_products = sorted(products.items(), key=lambda x: x[1], reverse=True)[:5]
        
        report = f"""# Sales Report - {period.title()}

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}

## Summary

| Metric | Value |
|--------|-------|
| Total Revenue | ${total_revenue:,.2f} |
| Total Orders | {total_orders} |
| Average Order | ${avg_order:,.2f} |

## Top Products

| Product | Quantity Sold |
|---------|---------------|
"""
        for product, qty in top_products:
            report += f"| {product} | {qty} |\n"
        
        # Save report
        filename = f"sales_report_{datetime.now().strftime('%Y%m%d')}.md"
        filepath = self.output_dir / filename
        filepath.write_text(report)
        
        return str(filepath)
    
    def generate_client_summary(
        self,
        clients: List[Dict],
        interactions: List[Dict]
    ) -> str:
        """Generate client activity summary"""
        
        active_clients = len(set(i['client_id'] for i in interactions))
        total_clients = len(clients)
        
        report = f"""# Client Activity Report

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}

## Overview

- Total Clients: {total_clients}
- Active This Period: {active_clients}
- Activity Rate: {active_clients/total_clients*100:.1f}%

## Client List

| ID | Name | City | Status |
|----|------|------|--------|
"""
        for client in clients[:20]:  # Show first 20
            status = "🟢 Active" if client['id'] in [i['client_id'] for i in interactions] else "⚪ Inactive"
            report += f"| {client['id']} | {client['name']} | {client.get('city', '-')} | {status} |\n"
        
        if len(clients) > 20:
            report += f"\n*... and {len(clients) - 20} more clients*\n"
        
        filename = f"client_report_{datetime.now().strftime('%Y%m%d')}.md"
        filepath = self.output_dir / filename
        filepath.write_text(report)
        
        return str(filepath)


# Example usage
if __name__ == "__main__":
    generator = ReportGenerator()
    
    # Sample data
    sample_orders = [
        {"product": "Succulent A", "quantity": 50, "amount": 2500},
        {"product": "Succulent B", "quantity": 30, "amount": 1800},
        {"product": "Succulent A", "quantity": 25, "amount": 1250},
    ]
    
    report_path = generator.generate_sales_report(sample_orders)
    print(f"Report saved: {report_path}")
