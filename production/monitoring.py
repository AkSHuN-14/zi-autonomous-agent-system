"""
Monitoring and Logging System
Production-grade monitoring for the ZI Agent System
"""

import logging
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from enum import Enum
import traceback


class LogLevel(Enum):
    """Log levels"""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class MetricType(Enum):
    """Types of metrics to track"""
    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"


@dataclass
class LogEntry:
    """Structured log entry"""
    timestamp: str
    level: LogLevel
    component: str
    message: str
    context: Dict[str, Any] = field(default_factory=dict)
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    exception: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp,
            "level": self.level.value,
            "component": self.component,
            "message": self.message,
            "context": self.context,
            "user_id": self.user_id,
            "session_id": self.session_id,
            "exception": self.exception
        }


@dataclass
class Metric:
    """Performance metric"""
    name: str
    value: float
    metric_type: MetricType
    timestamp: str
    labels: Dict[str, str] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "value": self.value,
            "type": self.metric_type.value,
            "timestamp": self.timestamp,
            "labels": self.labels
        }


class MonitoringSystem:
    """
    Comprehensive monitoring and logging system
    """
    
    def __init__(
        self,
        log_file: str = "logs/agent_system.log",
        metrics_file: str = "logs/metrics.jsonl",
        enable_console: bool = True
    ):
        """
        Initialize monitoring system
        
        Args:
            log_file: Path to log file
            metrics_file: Path to metrics file
            enable_console: Whether to output to console
        """
        self.log_file = log_file
        self.metrics_file = metrics_file
        self.enable_console = enable_console
        
        self.logs: List[LogEntry] = []
        self.metrics: List[Metric] = []
        self.counters: Dict[str, float] = {}
        
        self._setup_logging()
    
    def _setup_logging(self):
        """Setup Python logging"""
        import os
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
        
        # Configure root logger
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.log_file),
                logging.StreamHandler() if self.enable_console else None
            ]
        )
        
        self.logger = logging.getLogger("ZIAgent")
    
    def log(
        self,
        level: LogLevel,
        component: str,
        message: str,
        context: Dict[str, Any] = None,
        user_id: str = None,
        session_id: str = None,
        exception: Exception = None
    ):
        """
        Log a message
        
        Args:
            level: Log level
            component: Component generating the log
            message: Log message
            context: Additional context
            user_id: User identifier
            session_id: Session identifier
            exception: Exception object if applicable
        """
        if context is None:
            context = {}
        
        exception_str = None
        if exception:
            exception_str = traceback.format_exc()
        
        log_entry = LogEntry(
            timestamp=datetime.now().isoformat(),
            level=level,
            component=component,
            message=message,
            context=context,
            user_id=user_id,
            session_id=session_id,
            exception=exception_str
        )
        
        self.logs.append(log_entry)
        
        # Log to Python logger
        log_level = getattr(logging, level.value)
        self.logger.log(log_level, f"{component}: {message}")
        
        # Store recent logs in memory (limit to 1000)
        if len(self.logs) > 1000:
            self.logs = self.logs[-1000:]
    
    def record_metric(
        self,
        name: str,
        value: float,
        metric_type: MetricType = MetricType.GAUGE,
        labels: Dict[str, str] = None
    ):
        """
        Record a metric
        
        Args:
            name: Metric name
            value: Metric value
            metric_type: Type of metric
            labels: Additional labels
        """
        if labels is None:
            labels = {}
        
        metric = Metric(
            name=name,
            value=value,
            metric_type=metric_type,
            timestamp=datetime.now().isoformat(),
            labels=labels
        )
        
        self.metrics.append(metric)
        
        # Update counters
        if metric_type == MetricType.COUNTER:
            self.counters[name] = self.counters.get(name, 0) + value
        
        # Keep recent metrics
        if len(self.metrics) > 1000:
            self.metrics = self.metrics[-1000:]
    
    def increment_counter(self, name: str, value: float = 1.0, labels: Dict[str, str] = None):
        """Increment a counter metric"""
        self.record_metric(name, value, MetricType.COUNTER, labels)
    
    def set_gauge(self, name: str, value: float, labels: Dict[str, str] = None):
        """Set a gauge metric"""
        self.record_metric(name, value, MetricType.GAUGE, labels)
    
    def get_recent_logs(
        self,
        level: LogLevel = None,
        component: str = None,
        limit: int = 100
    ) -> List[LogEntry]:
        """Get recent logs with optional filtering"""
        filtered_logs = self.logs
        
        if level:
            filtered_logs = [log for log in filtered_logs if log.level == level]
        
        if component:
            filtered_logs = [log for log in filtered_logs if log.component == component]
        
        return filtered_logs[-limit:]
    
    def get_metrics_summary(self) -> Dict[str, Any]:
        """Get summary of recorded metrics"""
        summary = {
            "counters": self.counters.copy(),
            "total_metrics": len(self.metrics),
            "recent_metrics": []
        }
        
        # Add recent metrics
        for metric in self.metrics[-10:]:
            summary["recent_metrics"].append(metric.to_dict())
        
        return summary
    
    def get_health_status(self) -> Dict[str, Any]:
        """Get system health status"""
        error_count = len([log for log in self.logs if log.level in [LogLevel.ERROR, LogLevel.CRITICAL]])
        
        health_status = "healthy"
        if error_count > 10:
            health_status = "degraded"
        if error_count > 50:
            health_status = "unhealthy"
        
        return {
            "status": health_status,
            "error_count": error_count,
            "total_logs": len(self.logs),
            "total_metrics": len(self.metrics),
            "uptime": self._get_uptime()
        }
    
    def _get_uptime(self) -> str:
        """Calculate system uptime"""
        if not self.logs:
            return "unknown"
        
        start_time = datetime.fromisoformat(self.logs[0].timestamp)
        uptime = datetime.now() - start_time
        
        hours, remainder = divmod(int(uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        
        return f"{hours}h {minutes}m {seconds}s"
    
    def export_logs(self, filepath: str):
        """Export logs to file"""
        import os
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'w') as f:
            for log_entry in self.logs:
                f.write(json.dumps(log_entry.to_dict()) + '\n')
    
    def export_metrics(self, filepath: str):
        """Export metrics to file"""
        import os
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'w') as f:
            for metric in self.metrics:
                f.write(json.dumps(metric.to_dict()) + '\n')


# Performance Monitor for specific components
class PerformanceMonitor:
    """Monitor performance of specific operations"""
    
    def __init__(self, monitoring_system: MonitoringSystem):
        """
        Initialize performance monitor
        
        Args:
            monitoring_system: Parent monitoring system
        """
        self.monitoring = monitoring_system
        self.operation_timings: Dict[str, List[float]] = {}
    
    def track_operation(self, operation_name: str):
        """Context manager for tracking operation performance"""
        import time
        
        class OperationTracker:
            def __init__(self, perf_monitor, op_name):
                self.perf_monitor = perf_monitor
                self.op_name = op_name
                self.start_time = None
            
            def __enter__(self):
                self.start_time = time.time()
                return self
            
            def __exit__(self, exc_type, exc_val, exc_tb):
                duration = time.time() - self.start_time
                
                if self.op_name not in self.perf_monitor.operation_timings:
                    self.perf_monitor.operation_timings[self.op_name] = []
                
                self.perf_monitor.operation_timings[self.op_name].append(duration)
                
                # Keep only last 100 timings
                if len(self.perf_monitor.operation_timings[self.op_name]) > 100:
                    self.perf_monitor.operation_timings[self.op_name] = \
                        self.perf_monitor.operation_timings[self.op_name][-100]
                
                # Record as metric
                self.perf_monitor.monitoring.record_metric(
                    f"{self.op_name}_duration",
                    duration,
                    MetricType.HISTOGRAM
                )
                
                if exc_type is not None:
                    self.perf_monitor.monitoring.log(
                        LogLevel.ERROR,
                        self.op_name,
                        f"Operation failed: {exc_val}",
                        exception=exc_val if exc_tb else None
                    )
        
        return OperationTracker(self, operation_name)
    
    def get_operation_stats(self, operation_name: str) -> Dict[str, float]:
        """Get statistics for an operation"""
        if operation_name not in self.operation_timings:
            return {}
        
        timings = self.operation_timings[operation_name]
        
        if not timings:
            return {}
        
        timings.sort()
        n = len(timings)
        
        return {
            "count": n,
            "min": min(timings),
            "max": max(timings),
            "avg": sum(timings) / n,
            "median": timings[n // 2],
            "p95": timings[int(n * 0.95)] if n >= 20 else timings[-1],
            "p99": timings[int(n * 0.99)] if n >= 100 else timings[-1]
        }


# Global monitoring instance
global_monitoring = MonitoringSystem()
global_performance_monitor = PerformanceMonitor(global_monitoring)


# Convenience functions
def log_info(component: str, message: str, **kwargs):
    """Log info message"""
    global_monitoring.log(LogLevel.INFO, component, message, **kwargs)


def log_error(component: str, message: str, exception: Exception = None, **kwargs):
    """Log error message"""
    global_monitoring.log(LogLevel.ERROR, component, message, exception=exception, **kwargs)


def log_debug(component: str, message: str, **kwargs):
    """Log debug message"""
    global_monitoring.log(LogLevel.DEBUG, component, message, **kwargs)


def record_metric(name: str, value: float, **kwargs):
    """Record a metric"""
    global_monitoring.record_metric(name, value, **kwargs)


def track_operation(operation_name: str):
    """Track operation performance"""
    return global_performance_monitor.track_operation(operation_name)


if __name__ == "__main__":
    # Test monitoring system
    log_info("TestComponent", "System started")
    log_error("TestComponent", "Test error", exception=Exception("Test exception"))
    record_metric("test_metric", 42.0)
    
    with track_operation("test_operation"):
        import time
        time.sleep(0.1)
    
    print("Health Status:", json.dumps(global_monitoring.get_health_status(), indent=2))
    print("Metrics Summary:", json.dumps(global_monitoring.get_metrics_summary(), indent=2))
    print("Operation Stats:", json.dumps(global_performance_monitor.get_operation_stats("test_operation"), indent=2))
