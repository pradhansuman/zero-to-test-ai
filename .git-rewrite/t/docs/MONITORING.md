# Logging & Monitoring Guide

This document covers logging configuration, monitoring setup, and alerting strategies.

---

## Structured Logging

The application uses JSON-formatted structured logging for easy parsing and aggregation.

### Log Format

```json
{
  "timestamp": "2024-01-01T12:00:00Z",
  "level": "INFO",
  "logger": "app.services.project_service",
  "message": "Project created successfully",
  "user_id": 123,
  "resource_id": 456,
  "operation": "create_project",
  "duration_ms": 145,
  "status": "success"
}
```

### Log Levels

| Level | Usage |
|-------|-------|
| DEBUG | Detailed diagnostic information |
| INFO | General informational messages |
| WARNING | Warning messages for recoverable issues |
| ERROR | Error messages for failures |
| CRITICAL | Critical system failures |

### Configuration

```python
# backend/app/utils/logger.py
from app.utils.logger import StructuredLogger

logger = StructuredLogger(__name__)

# Log with context
logger.info(
    "operation_name",
    user_id=user_id,
    resource_id=resource_id,
    operation="create",
    duration_ms=elapsed_time
)

# Log errors
logger.error(
    "operation_failed",
    error=str(e),
    error_type=type(e).__name__,
    user_id=user_id
)
```

---

## Health Checks

Health checks are used for readiness and liveness probes.

### Endpoints

| Endpoint | Purpose | Response |
|----------|---------|----------|
| `GET /health` | Basic health | 200 OK |
| `GET /health/ready` | Readiness probe | 200 OK (DB connected) |
| `GET /health/live` | Liveness probe | 200 OK (service alive) |
| `GET /health/db` | Database health | 200 OK (DB details) |

### Kubernetes Probes

```yaml
livenessProbe:
  httpGet:
    path: /health/live
    port: 8000
  initialDelaySeconds: 30
  periodSeconds: 10

readinessProbe:
  httpGet:
    path: /health/ready
    port: 8000
  initialDelaySeconds: 10
  periodSeconds: 5
```

---

## Metrics

Application metrics for monitoring performance and usage.

### Key Metrics

| Metric | Type | Description |
|--------|------|-------------|
| `request_count` | Counter | Total HTTP requests |
| `request_duration_seconds` | Histogram | Request latency |
| `database_queries` | Counter | Total database queries |
| `celery_tasks_total` | Counter | Total Celery tasks |
| `celery_task_duration_seconds` | Histogram | Task execution time |
| `redis_connections_active` | Gauge | Active Redis connections |

### Prometheus Integration

Metrics endpoint: `GET /metrics`

```bash
# Test metrics endpoint
curl http://localhost:8000/metrics
```

Sample response:

```
# HELP request_count_total Total HTTP requests
# TYPE request_count_total counter
request_count_total{method="GET",endpoint="/health",status="200"} 1234
request_count_total{method="POST",endpoint="/projects",status="200"} 56

# HELP request_duration_seconds Request latency in seconds
# TYPE request_duration_seconds histogram
request_duration_seconds_bucket{le="0.1",method="GET",endpoint="/projects"} 45
request_duration_seconds_bucket{le="0.5",method="GET",endpoint="/projects"} 48
request_duration_seconds_bucket{le="1.0",method="GET",endpoint="/projects"} 50
```

### Prometheus Configuration

```yaml
# prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'qa-backend'
    static_configs:
      - targets: ['localhost:8000']
    metrics_path: '/metrics'
```

---

## Distributed Tracing

Optional integration with Jaeger/OpenTelemetry for tracing requests across services.

### Setup

```python
# backend/app/main.py
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.exporter.jaeger.thrift import JaegerExporter

jaeger_exporter = JaegerExporter(
    agent_host_name="jaeger",
    agent_port=6831,
)

trace.set_tracer_provider(TracerProvider())
trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(jaeger_exporter)
)
```

### Jaeger UI

Access trace visualization:

```
http://localhost:16686
```

---

## Error Tracking

Integration with Sentry for error tracking and alerting.

### Setup

```bash
# pip install sentry-sdk
```

```python
# backend/app/main.py
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration

sentry_sdk.init(
    dsn=settings.sentry_dsn,
    integrations=[FastApiIntegration()],
    environment=settings.sentry_environment,
    traces_sample_rate=0.1,
)
```

### Configuration

```bash
# .env
SENTRY_DSN=https://key@sentry.io/123456
SENTRY_ENVIRONMENT=production
```

---

## Alerting

### Alert Rules

Key metrics that should trigger alerts:

| Condition | Alert | Action |
|-----------|-------|--------|
| Error rate > 5% | High Error Rate | Page on-call engineer |
| Response time > 1s | Slow API | Investigate performance |
| Database unreachable | Database Down | Critical - page everyone |
| Disk space > 90% | Disk Full | Immediate cleanup |
| Memory usage > 85% | High Memory | Restart service |

### Slack Notifications

```python
# Setup in Sentry/Prometheus
# Send alerts to Slack channel
```

### Email Alerts

Configure in Prometheus Alertmanager:

```yaml
# alertmanager.yml
route:
  receiver: 'email'

receivers:
  - name: 'email'
    email_configs:
      - to: 'team@example.com'
        from: 'alerts@example.com'
        smarthost: 'smtp.gmail.com:587'
        auth_username: 'email@gmail.com'
        auth_password: '${ALERTMANAGER_EMAIL_PASSWORD}'
```

---

## Log Aggregation

### ELK Stack (Elasticsearch, Logstash, Kibana)

#### Filebeat Configuration

```yaml
# filebeat.yml
filebeat.inputs:
- type: log
  enabled: true
  paths:
    - /var/log/qa-backend/*.log
  fields:
    service: qa-backend

output.elasticsearch:
  hosts: ["elasticsearch:9200"]
  index: "qa-backend-%{+yyyy.MM.dd}"

processors:
  - add_kubernetes_metadata:
  - add_docker_metadata:
  - add_host_metadata:
```

#### Kibana Dashboard

Access logs:

```
http://localhost:5601
```

Create dashboard to visualize:
- Request count over time
- Error rate by endpoint
- Response time distribution
- Log volume by level

### CloudWatch (AWS)

```python
# backend/app/utils/logger.py
import watchtower

logging.basicConfig(
    level=logging.INFO,
    handlers=[
        watchtower.CloudWatchLogHandler()
    ]
)
```

---

## Performance Monitoring

### Request Metrics

Monitor via middleware:

```python
# backend/app/middleware/metrics.py
from time import time

@app.middleware("http")
async def add_process_time_header(request, call_next):
    start_time = time()
    response = await call_next(request)
    process_time = time() - start_time
    
    logger.info(
        "request_completed",
        method=request.method,
        path=request.url.path,
        status_code=response.status_code,
        duration_ms=int(process_time * 1000)
    )
    
    return response
```

### Database Performance

```python
# Monitor slow queries
# Set log_min_duration_statement in PostgreSQL
```

### Celery Task Monitoring

```python
# Task execution tracking
@task.bind
def execute_tests(self, project_id):
    logger.info(
        "task_started",
        task_id=self.request.id,
        task_name=self.name,
        project_id=project_id
    )
    
    try:
        # Execute tests
        result = run_tests(project_id)
        logger.info(
            "task_completed",
            task_id=self.request.id,
            result=result
        )
        return result
    except Exception as e:
        logger.error(
            "task_failed",
            task_id=self.request.id,
            error=str(e)
        )
        raise
```

---

## Monitoring Checklist

- [ ] Structured logging enabled
- [ ] Health check endpoints working
- [ ] Metrics endpoint (`/metrics`) accessible
- [ ] Kubernetes probes configured
- [ ] Error tracking (Sentry) enabled
- [ ] Log aggregation (ELK/CloudWatch) configured
- [ ] Alerts set up for critical metrics
- [ ] Dashboard created for key metrics
- [ ] On-call rotation configured
- [ ] Runbooks created for common alerts

---

## Runbooks

### Database Connection Lost

1. Check connectivity: `pg_isready -h postgres -U qa_user`
2. Check credentials in `.env`
3. Verify PostgreSQL is running: `docker-compose ps postgres`
4. Restart PostgreSQL: `docker-compose restart postgres`
5. Check logs: `docker-compose logs postgres`

### High Error Rate

1. Check error logs for patterns
2. Review recent deployments
3. Check resource utilization (CPU, memory)
4. Restart service: `docker-compose restart backend`
5. Rollback if needed

### Slow API Responses

1. Check database query logs
2. Monitor CPU and memory usage
3. Check Redis connectivity
4. Review active connections
5. Restart if necessary

---

## Best Practices

1. **Always log structured data** - Use consistent key names
2. **Include context** - Add user_id, resource_id, operation
3. **Log at appropriate levels** - DEBUG for development, INFO for production
4. **Avoid logging secrets** - Never log passwords, tokens, API keys
5. **Set retention policies** - Archive old logs for compliance
6. **Monitor the monitors** - Ensure logging system is working
7. **Test alerts** - Verify alerts trigger correctly
8. **Document dashboards** - Explain what each metric means
9. **Review logs regularly** - Look for patterns and anomalies
10. **Automate response** - Trigger automatic remediation when possible
