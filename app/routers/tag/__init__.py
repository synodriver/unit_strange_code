# -*- coding: utf-8 -*-
from io import BytesIO
from typing import IO, List

import aiohttp
from fastapi import APIRouter, File, Form, Query, UploadFile
from fastapi.responses import UJSONResponse

from .crud import predict_file

router = APIRouter(prefix="/api/v1")


async def download_from_url(url: str) -> IO:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                return BytesIO(await resp.read())
    except aiohttp.ClientError as e:
        print(e)


@router.get("/tag", description="input picture with url", response_class=UJSONResponse)
async def process_pic_url(
    url: str = Query(..., description="pic url"),
    limit: float = Query(0.7, description="the threshold to output"),
):
    """
    输入一个url
    :param url: 一个url
    :return:
    """
    data = await download_from_url(url)
    return predict_file(data, limit)


@router.post("/tag", description="input picture", response_class=UJSONResponse)
def process_pic(
    data: UploadFile = File(..., description="pic"),
    limit: float = Form(0.7, description="the threshold to output"),
):
    ret = predict_file(data.file, limit)
    return ret
