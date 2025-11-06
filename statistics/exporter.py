"""Export statistics to various formats."""

import csv
import json
from typing import Dict, List, Any
from pathlib import Path


class StatisticsExporter:
    """Exports statistics to CSV and JSON formats."""

    @staticmethod
    def export_to_csv(data: List[Dict[str, Any]], filepath: str, fieldnames: List[str] = None):
        """Export data to CSV file."""
        if not data:
            return

        # Create directory if needed
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)

        if fieldnames is None:
            fieldnames = list(data[0].keys())

        with open(filepath, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)

    @staticmethod
    def export_to_json(data: Any, filepath: str, indent: int = 2):
        """Export data to JSON file."""
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)

        with open(filepath, 'w') as jsonfile:
            json.dump(data, jsonfile, indent=indent)

    @staticmethod
    def export_time_series(time_points: List[float], metrics: Dict[str, List[float]], 
                          filepath: str):
        """Export time series data to CSV."""
        rows = []
        for i, t in enumerate(time_points):
            row = {'time': t}
            for metric_name, values in metrics.items():
                if i < len(values):
                    row[metric_name] = values[i]
            rows.append(row)

        StatisticsExporter.export_to_csv(rows, filepath)

    @staticmethod
    def export_summary_report(summary: Dict[str, Any], filepath: str):
        """Export summary report as JSON."""
        StatisticsExporter.export_to_json(summary, filepath, indent=2)
