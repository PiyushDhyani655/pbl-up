import pandas as pd
import numpy as np
from typing import Dict, List, Any, Tuple
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

class HistoryAnalyzer:

    def __init__(self, database_manager):
        self.db_manager = database_manager

    def get_system_summary(self, hours: int = 24) -> Dict[str, Any]:
        df = self.db_manager.get_system_history(hours)

        if df.empty:
            return {
                'cpu_avg': 0.0,
                'cpu_max': 0.0,
                'memory_avg': 0.0,
                'memory_max': 0.0,
                'disk_avg': 0.0,
                'disk_max': 0.0,
                'processes_avg': 0,
                'start_time': datetime.now() - timedelta(hours=hours),
                'end_time': datetime.now(),
                'data_points': 0
            }

        summary = {
            'cpu_avg': df['cpu_percent'].mean(),
            'cpu_max': df['cpu_percent'].max(),
            'memory_avg': df['memory_percent'].mean(),
            'memory_max': df['memory_percent'].max(),
            'disk_avg': df['disk_percent'].mean(),
            'disk_max': df['disk_percent'].max(),
            'processes_avg': int(df['total_processes'].mean()),
            'start_time': df['timestamp'].min(),
            'end_time': df['timestamp'].max(),
            'data_points': len(df)
        }

        return summary

    def get_top_processes(self, limit: int = 5) -> pd.DataFrame:
        return self.db_manager.get_top_processes_by_cpu(limit)

    def get_process_analysis(self, process_name: str) -> Dict[str, Any]:
        df = self.db_manager.get_process_trend(process_name)

        if df.empty:
            return {
                'name': process_name,
                'cpu_avg': 0.0,
                'cpu_max': 0.0,
                'memory_avg': 0.0,
                'memory_max': 0.0,
                'data_points': 0,
                'trend_data': pd.DataFrame()
            }

        analysis = {
            'name': process_name,
            'cpu_avg': df['cpu_percent'].mean(),
            'cpu_max': df['cpu_percent'].max(),
            'memory_avg': df['memory_mb'].mean(),
            'memory_max': df['memory_mb'].max(),
            'data_points': len(df),
            'trend_data': df
        }

        return analysis

    def generate_cpu_usage_chart(self, hours: int = 24) -> plt.Figure:
        df = self.db_manager.get_system_history(hours)

        if df.empty:
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.text(0.5, 0.5, "No data available", ha='center', va='center')
            return fig

        fig, ax = plt.subplots(figsize=(10, 6))

        ax.plot(df['timestamp'], df['cpu_percent'], 'b-', linewidth=2)

        ax.set_xlabel('Time')
        ax.set_ylabel('CPU Usage (%)')
        ax.set_title(f'CPU Usage Over the Last {hours} Hours')

        ax.grid(True, alpha=0.3)

        plt.xticks(rotation=45)
        plt.tight_layout()

        return fig

    def generate_memory_usage_chart(self, hours: int = 24) -> plt.Figure:
        df = self.db_manager.get_system_history(hours)

        if df.empty:
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.text(0.5, 0.5, "No data available", ha='center', va='center')
            return fig

        fig, ax = plt.subplots(figsize=(10, 6))

        ax.plot(df['timestamp'], df['memory_percent'], 'r-', linewidth=2)

        ax.set_xlabel('Time')
        ax.set_ylabel('Memory Usage (%)')
        ax.set_title(f'Memory Usage Over the Last {hours} Hours')

        ax.grid(True, alpha=0.3)

        plt.xticks(rotation=45)
        plt.tight_layout()

        return fig

    def generate_top_processes_chart(self, limit: int = 5) -> plt.Figure:
        df = self.get_top_processes(limit)

        if df.empty:
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.text(0.5, 0.5, "No data available", ha='center', va='center')
            return fig

        fig, ax = plt.subplots(figsize=(10, 6))

        bars = ax.bar(df['name'], df['avg_cpu'], color='skyblue')

        ax.set_xlabel('Process Name')
        ax.set_ylabel('Average CPU Usage (%)')
        ax.set_title(f'Top {limit} Processes by CPU Usage')

        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                    f'{height:.1f}%', ha='center', va='bottom')

        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()

        return fig

    def generate_process_trend_chart(self, process_name: str) -> plt.Figure:
        df = self.db_manager.get_process_trend(process_name)

        if df.empty:
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.text(0.5, 0.5, f"No data available for {process_name}", ha='center', va='center')
            return fig

        fig, ax1 = plt.subplots(figsize=(10, 6))
        ax2 = ax1.twinx()

        ax1.plot(df['timestamp'], df['cpu_percent'], 'b-', linewidth=2, label='CPU Usage')
        ax1.set_xlabel('Time')
        ax1.set_ylabel('CPU Usage (%)', color='b')
        ax1.tick_params(axis='y', labelcolor='b')

        ax2.plot(df['timestamp'], df['memory_mb'], 'r-', linewidth=2, label='Memory Usage')
        ax2.set_ylabel('Memory Usage (MB)', color='r')
        ax2.tick_params(axis='y', labelcolor='r')

        plt.title(f'CPU and Memory Trends for {process_name}')

        lines1, labels1 = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')

        plt.xticks(rotation=45)
        plt.tight_layout()

        return fig
