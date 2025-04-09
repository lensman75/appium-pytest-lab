from celery import Celery

app = Celery(
    'tasks',
    broker='amqp://guest:guest@localhost:5672//',
    backend="rpc://",
    # backend="redis://localhost:6379/0",
    include=["api.tasks"]
)

# Use JSON serialization
app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
)