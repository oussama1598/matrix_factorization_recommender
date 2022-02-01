from typing import Optional

import pkg_resources
from fastapi import APIRouter, Cookie
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse

from server.app.api.endpoints import discord, wallet, collection

router = APIRouter()


@router.get('/')
async def index():
    return 'OK'
