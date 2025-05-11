"""
History dialog module for TaskMaster.
Displays historical process and system data with analysis.
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QTabWidget, QWidget, QComboBox,
    QTableWidget, QTableWidgetItem, QHeaderView,
    QSplitter, QFrame
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

import matplotlib
matplotlib.use('QtAgg')
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from src.core.history_analyzer import HistoryAnalyzer

class HistoryDialog(QDialog):
    """Dialog for displaying process and system history."""
    
    def __init__(self, history_analyzer, parent=None):
        """Initialize the history dialog.
        
        Args:
            history_analyzer: History analyzer instance
            parent: Parent widget
        """
        super().__init__(parent)
        
        self.history_analyzer = history_analyzer
        self.setWindowTitle("Process History and Analysis")
        self.resize(1000, 700)
        
        # Set up the UI
        self._setup_ui()
        
        # Load initial data
        self._load_data()
    
    def _setup_ui(self):
        """Set up the user interface."""
        # Create main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        # Add title
        title_label = QLabel("Process History and Analysis")
        title_label.setFont(QFont('Arial', 14, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)
        
        # Create tab widget
        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)
        
        # Add system overview tab
        self.system_tab = QWidget()
        self.tab_widget.addTab(self.system_tab, "System Overview")
        self._setup_system_tab()
        
        # Add process history tab
        self.process_tab = QWidget()
        self.tab_widget.addTab(self.process_tab, "Process History")
        self._setup_process_tab()
        
        # Add top processes tab
        self.top_tab = QWidget()
        self.tab_widget.addTab(self.top_tab, "Top Processes")
        self._setup_top_tab()
        
        # Add process analysis tab
        self.analysis_tab = QWidget()
        self.tab_widget.addTab(self.analysis_tab, "Process Analysis")
        self._setup_analysis_tab()
        
        # Add close button
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.close)
        close_button.setStyleSheet("""
            QPushButton {
                background-color: #3E4154;
                color: white;
                border: 1px solid #4F5D75;
                padding: 5px 15px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #4F5D75;
            }
            QPushButton:pressed {
                background-color: #5C6B8C;
            }
        """)
        button_layout.addWidget(close_button)
        
        main_layout.addLayout(button_layout)
        
        # Set dark theme
        self.setStyleSheet("""
            QDialog {
                background-color: #1E1E1E;
                color: white;
            }
            QTabWidget::pane {
                border: 1px solid #4F5D75;
                background-color: #2D2D30;
            }
            QTabBar::tab {
                background-color: #3E4154;
                color: white;
                padding: 8px 12px;
                border: 1px solid #4F5D75;
                border-bottom: none;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background-color: #2D2D30;
                border-bottom: 1px solid #2D2D30;
            }
            QLabel {
                color: white;
            }
            QTableWidget {
                background-color: #2D2D30;
                color: white;
                gridline-color: #4F5D75;
                border: none;
            }
            QTableWidget::item {
                padding: 4px;
            }
            QTableWidget::item:selected {
                background-color: #4F5D75;
            }
            QHeaderView::section {
                background-color: #3E4154;
                color: white;
                padding: 4px;
                border: 1px solid #4F5D75;
            }
            QComboBox {
                background-color: #3E4154;
                color: white;
                border: 1px solid #4F5D75;
                padding: 4px;
                border-radius: 3px;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox QAbstractItemView {
                background-color: #3E4154;
                color: white;
                selection-background-color: #4F5D75;
            }
        """)
    
    def _setup_system_tab(self):
        """Set up the system overview tab."""
        layout = QVBoxLayout(self.system_tab)
        
        # Add time period selector
        period_layout = QHBoxLayout()
        period_layout.addWidget(QLabel("Time Period:"))
        
        self.period_combo = QComboBox()
        self.period_combo.addItems(["Last 6 Hours", "Last 24 Hours", "Last 3 Days", "Last 7 Days"])
        self.period_combo.setCurrentIndex(1)  # Default to 24 hours
        self.period_combo.currentIndexChanged.connect(self._load_system_data)
        period_layout.addWidget(self.period_combo)
        period_layout.addStretch()
        
        layout.addLayout(period_layout)
        
        # Add summary section
        summary_frame = QFrame()
        summary_frame.setFrameShape(QFrame.Shape.StyledPanel)
        summary_frame.setStyleSheet("background-color: #2D3142; padding: 10px;")
        summary_layout = QVBoxLayout(summary_frame)
        
        summary_title = QLabel("System Performance Summary")
        summary_title.setFont(QFont('Arial', 12, QFont.Weight.Bold))
        summary_layout.addWidget(summary_title)
        
        # Create grid for summary stats
        stats_layout = QHBoxLayout()
        
        # CPU stats
        cpu_layout = QVBoxLayout()
        cpu_layout.addWidget(QLabel("CPU Usage"))
        self.cpu_avg_label = QLabel("Avg: 0.0%")
        self.cpu_max_label = QLabel("Max: 0.0%")
        cpu_layout.addWidget(self.cpu_avg_label)
        cpu_layout.addWidget(self.cpu_max_label)
        stats_layout.addLayout(cpu_layout)
        
        # Memory stats
        mem_layout = QVBoxLayout()
        mem_layout.addWidget(QLabel("Memory Usage"))
        self.mem_avg_label = QLabel("Avg: 0.0%")
        self.mem_max_label = QLabel("Max: 0.0%")
        mem_layout.addWidget(self.mem_avg_label)
        mem_layout.addWidget(self.mem_max_label)
        stats_layout.addLayout(mem_layout)
        
        # Disk stats
        disk_layout = QVBoxLayout()
        disk_layout.addWidget(QLabel("Disk Usage"))
        self.disk_avg_label = QLabel("Avg: 0.0%")
        self.disk_max_label = QLabel("Max: 0.0%")
        disk_layout.addWidget(self.disk_avg_label)
        disk_layout.addWidget(self.disk_max_label)
        stats_layout.addLayout(disk_layout)
        
        # Process stats
        proc_layout = QVBoxLayout()
        proc_layout.addWidget(QLabel("Processes"))
        self.proc_avg_label = QLabel("Avg: 0")
        self.data_points_label = QLabel("Data Points: 0")
        proc_layout.addWidget(self.proc_avg_label)
        proc_layout.addWidget(self.data_points_label)
        stats_layout.addLayout(proc_layout)
        
        summary_layout.addLayout(stats_layout)
        layout.addWidget(summary_frame)
        
        # Add charts
        charts_layout = QVBoxLayout()
        
        # CPU usage chart
        cpu_chart_label = QLabel("CPU Usage Over Time")
        cpu_chart_label.setFont(QFont('Arial', 11, QFont.Weight.Bold))
        charts_layout.addWidget(cpu_chart_label)
        
        self.cpu_chart_canvas = FigureCanvas(Figure(figsize=(8, 4)))
        charts_layout.addWidget(self.cpu_chart_canvas)
        
        # Memory usage chart
        mem_chart_label = QLabel("Memory Usage Over Time")
        mem_chart_label.setFont(QFont('Arial', 11, QFont.Weight.Bold))
        charts_layout.addWidget(mem_chart_label)
        
        self.mem_chart_canvas = FigureCanvas(Figure(figsize=(8, 4)))
        charts_layout.addWidget(self.mem_chart_canvas)
        
        layout.addLayout(charts_layout)
    
    def _setup_process_tab(self):
        """Set up the process history tab."""
        layout = QVBoxLayout(self.process_tab)
        
        # Add process selector
        selector_layout = QHBoxLayout()
        selector_layout.addWidget(QLabel("Select Process:"))
        
        self.process_combo = QComboBox()
        self.process_combo.setMinimumWidth(200)
        self.process_combo.currentIndexChanged.connect(self._load_process_data)
        selector_layout.addWidget(self.process_combo)
        
        selector_layout.addStretch()
        
        # Add time period selector
        selector_layout.addWidget(QLabel("Time Period:"))
        
        self.process_period_combo = QComboBox()
        self.process_period_combo.addItems(["Last 6 Hours", "Last 24 Hours", "Last 3 Days", "Last 7 Days"])
        self.process_period_combo.setCurrentIndex(1)  # Default to 24 hours
        self.process_period_combo.currentIndexChanged.connect(self._load_process_data)
        selector_layout.addWidget(self.process_period_combo)
        
        layout.addLayout(selector_layout)
        
        # Add process trend chart
        self.process_chart_canvas = FigureCanvas(Figure(figsize=(8, 6)))
        layout.addWidget(self.process_chart_canvas)
        
        # Add process stats
        stats_frame = QFrame()
        stats_frame.setFrameShape(QFrame.Shape.StyledPanel)
        stats_frame.setStyleSheet("background-color: #2D3142; padding: 10px;")
        stats_layout = QVBoxLayout(stats_frame)
        
        stats_title = QLabel("Process Statistics")
        stats_title.setFont(QFont('Arial', 12, QFont.Weight.Bold))
        stats_layout.addWidget(stats_title)
        
        # Create grid for stats
        grid_layout = QHBoxLayout()
        
        # CPU stats
        cpu_layout = QVBoxLayout()
        cpu_layout.addWidget(QLabel("CPU Usage"))
        self.process_cpu_avg_label = QLabel("Avg: 0.0%")
        self.process_cpu_max_label = QLabel("Max: 0.0%")
        cpu_layout.addWidget(self.process_cpu_avg_label)
        cpu_layout.addWidget(self.process_cpu_max_label)
        grid_layout.addLayout(cpu_layout)
        
        # Memory stats
        mem_layout = QVBoxLayout()
        mem_layout.addWidget(QLabel("Memory Usage"))
        self.process_mem_avg_label = QLabel("Avg: 0.0 MB")
        self.process_mem_max_label = QLabel("Max: 0.0 MB")
        mem_layout.addWidget(self.process_mem_avg_label)
        mem_layout.addWidget(self.process_mem_max_label)
        grid_layout.addLayout(mem_layout)
        
        # Data points
        data_layout = QVBoxLayout()
        data_layout.addWidget(QLabel("Data"))
        self.process_data_points_label = QLabel("Data Points: 0")
        data_layout.addWidget(self.process_data_points_label)
        data_layout.addStretch()
        grid_layout.addLayout(data_layout)
        
        stats_layout.addLayout(grid_layout)
        layout.addWidget(stats_frame)
    
    def _setup_top_tab(self):
        """Set up the top processes tab."""
        layout = QVBoxLayout(self.top_tab)
        
        # Add controls
        controls_layout = QHBoxLayout()
        
        controls_layout.addWidget(QLabel("Number of Processes:"))
        
        self.top_count_combo = QComboBox()
        self.top_count_combo.addItems(["5", "10", "15", "20"])
        self.top_count_combo.setCurrentIndex(0)  # Default to 5
        self.top_count_combo.currentIndexChanged.connect(self._load_top_data)
        controls_layout.addWidget(self.top_count_combo)
        
        controls_layout.addStretch()
        
        layout.addLayout(controls_layout)
        
        # Add chart
        self.top_chart_canvas = FigureCanvas(Figure(figsize=(8, 5)))
        layout.addWidget(self.top_chart_canvas)
        
        # Add table
        table_label = QLabel("Top Processes by CPU Usage")
        table_label.setFont(QFont('Arial', 11, QFont.Weight.Bold))
        layout.addWidget(table_label)
        
        self.top_table = QTableWidget()
        self.top_table.setColumnCount(4)
        self.top_table.setHorizontalHeaderLabels(["Process Name", "Avg CPU %", "Avg Memory (MB)", "Count"])
        self.top_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.top_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.top_table)
    
    def _setup_analysis_tab(self):
        """Set up the process analysis tab."""
        layout = QVBoxLayout(self.analysis_tab)
        
        # Add info label
        info_label = QLabel("Select a process from the 'Process History' tab to view detailed analysis.")
        info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(info_label)
        
        # This tab will be populated dynamically when a process is selected
        self.analysis_layout = layout
    
    def _load_data(self):
        """Load initial data for all tabs."""
        self._load_system_data()
        self._load_process_list()
        self._load_top_data()
    
    def _load_system_data(self):
        """Load system overview data."""
        # Get time period
        period_index = self.period_combo.currentIndex()
        hours = [6, 24, 72, 168][period_index]  # 6h, 24h, 3d, 7d
        
        # Get system summary
        summary = self.history_analyzer.get_system_summary(hours)
        
        # Update summary labels
        self.cpu_avg_label.setText(f"Avg: {summary['cpu_avg']:.1f}%")
        self.cpu_max_label.setText(f"Max: {summary['cpu_max']:.1f}%")
        self.mem_avg_label.setText(f"Avg: {summary['memory_avg']:.1f}%")
        self.mem_max_label.setText(f"Max: {summary['memory_max']:.1f}%")
        self.disk_avg_label.setText(f"Avg: {summary['disk_avg']:.1f}%")
        self.disk_max_label.setText(f"Max: {summary['disk_max']:.1f}%")
        self.proc_avg_label.setText(f"Avg: {summary['processes_avg']}")
        self.data_points_label.setText(f"Data Points: {summary['data_points']}")
        
        # Update CPU chart
        cpu_fig = self.history_analyzer.generate_cpu_usage_chart(hours)
        self.cpu_chart_canvas.figure = cpu_fig
        self.cpu_chart_canvas.draw()
        
        # Update memory chart
        mem_fig = self.history_analyzer.generate_memory_usage_chart(hours)
        self.mem_chart_canvas.figure = mem_fig
        self.mem_chart_canvas.draw()
    
    def _load_process_list(self):
        """Load the list of processes for the combo box."""
        # Get top processes
        df = self.history_analyzer.get_top_processes(20)
        
        # Clear and populate combo box
        self.process_combo.clear()
        if not df.empty:
            for name in df['name']:
                self.process_combo.addItem(name)
    
    def _load_process_data(self):
        """Load data for the selected process."""
        # Get selected process
        if self.process_combo.count() == 0:
            return
        
        process_name = self.process_combo.currentText()
        
        # Get time period
        period_index = self.process_period_combo.currentIndex()
        hours = [6, 24, 72, 168][period_index]  # 6h, 24h, 3d, 7d
        
        # Get process analysis
        analysis = self.history_analyzer.get_process_analysis(process_name)
        
        # Update stats labels
        self.process_cpu_avg_label.setText(f"Avg: {analysis['cpu_avg']:.1f}%")
        self.process_cpu_max_label.setText(f"Max: {analysis['cpu_max']:.1f}%")
        self.process_mem_avg_label.setText(f"Avg: {analysis['memory_avg']:.1f} MB")
        self.process_mem_max_label.setText(f"Max: {analysis['memory_max']:.1f} MB")
        self.process_data_points_label.setText(f"Data Points: {analysis['data_points']}")
        
        # Update chart
        fig = self.history_analyzer.generate_process_trend_chart(process_name)
        self.process_chart_canvas.figure = fig
        self.process_chart_canvas.draw()
    
    def _load_top_data(self):
        """Load data for the top processes tab."""
        # Get number of processes
        count = int(self.top_count_combo.currentText())
        
        # Get top processes
        df = self.history_analyzer.get_top_processes(count)
        
        # Update chart
        fig = self.history_analyzer.generate_top_processes_chart(count)
        self.top_chart_canvas.figure = fig
        self.top_chart_canvas.draw()
        
        # Update table
        self.top_table.setRowCount(len(df))
        
        for row, (_, process) in enumerate(df.iterrows()):
            # Name
            self.top_table.setItem(row, 0, QTableWidgetItem(process['name']))
            
            # CPU %
            self.top_table.setItem(row, 1, QTableWidgetItem(f"{process['avg_cpu']:.1f}"))
            
            # Memory MB
            self.top_table.setItem(row, 2, QTableWidgetItem(f"{process['avg_memory']:.1f}"))
            
            # Count
            self.top_table.setItem(row, 3, QTableWidgetItem(str(int(process['count']))))
    
    def closeEvent(self, event):
        """Handle dialog close event."""
        event.accept()
