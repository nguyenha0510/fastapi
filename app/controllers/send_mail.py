from fastapi import APIRouter, Body
from models.email_data import *
from config import config

import requests

router = APIRouter()


@router.post("/send_mail", response_description="Send Email")
async def send_mail(email_data: EmailData = Body(...)):
    url_mail = config.get('URL_MAIL')
    data_send = dict(email_data)
    send = requests.post(url=url_mail, data=data_send)
    return send.json()
