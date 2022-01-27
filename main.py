import os
from app import app


def get_bind_and_port() -> str:
    bind_ = os.getenv("bind", "0.0.0.0")
    port = int(os.getenv("port", 9000))
    return f"{bind_}:{port}"


if __name__ == "__main__":
    import asyncio

    from hypercorn.asyncio import serve
    from hypercorn.config import Config

    conf = Config()
    conf.bind = [get_bind_and_port()]
    conf.accesslog = os.getenv("accesslog", "-")
    conf.errorlog = os.getenv("errorlog", "/log/error.log")
    asyncio.run(serve(app, conf))
