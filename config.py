# -*- coding: utf-8 -*-
import os

def get_bind_and_port() -> str:
    bind_ = os.getenv("bind", "0.0.0.0")
    port = int(os.getenv("port", 9000))
    return f"{bind_}:{port}"


wsgi_app = os.getenv("wsgi_app", "main:app")
bind = get_bind_and_port()
timeout = int(os.getenv("timeout", 30))
workers = int(os.getenv("workers", 1))
# keyfile="./key.pem"
# certfile="./cert.pem"

worker_class = os.getenv("worker_class", "hypercorn.workers.HypercornUvloopWorker")
worker_connections = int(os.getenv("worker_connections", 10000))

loglever = os.getenv("loglever", "debug")
# accesslog = "access.log"

access_log_format = os.getenv("access_log_format", '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"')
errorlog = os.getenv("errorlog", "/log/error.log")
