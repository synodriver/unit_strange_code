# -*- coding: utf-8 -*-
import time

from fastapi import FastAPI, Request

from .routers import nsfw, tag, tagv2, tagv3

app = FastAPI(title="Nginx Unit test", description="This will fail on unit")


app.include_router(nsfw.router)
app.include_router(tag.router)
app.include_router(tagv2.router)
app.include_router(tagv3.router)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
