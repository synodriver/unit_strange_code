# -*- coding: utf-8 -*-
from typing import List, IO
import asyncio

from fastapi import APIRouter, Query, File, UploadFile, Form
from fastapi.responses import UJSONResponse

from .models import OutputData
from .crud import classify, model, download_from_url

router = APIRouter(prefix="/api/v1")


@router.get("/nsfw",
            response_class=UJSONResponse,
            response_model=List[OutputData],
            response_model_exclude_none=True)
async def process_pic_url(urls: List[str] = Query(..., description="pic url"),
                          image_dim: int = Query(224, description="size")):
    """
    输入多个url
    :param image_dim: 像素 默认224
    :param urls: 多个url
    :return:
    """
    tasks = [asyncio.create_task(download_from_url(url)) for url in urls]
    data: List[IO] = await asyncio.gather(*tasks)
    return classify(model, data, image_dim)


@router.post("/nsfw", description="input picture",
             response_class=UJSONResponse,
             response_model=List[OutputData],
             response_model_exclude_none=True)
def process_pic(data: UploadFile = File(..., description="pic"),
                image_dim: int = Form(224, description="size")):
    ret = classify(model, data.file, image_dim)
    return ret
