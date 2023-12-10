import os
from dotenv import load_dotenv
from typing import List
import requests

load_dotenv('.env')


def send_email(subject:str, message:str, to: List[str]):
    auth = ("api", os.environ["SERVICES_MAILGUN_SECRET"])
    data = {
        "from": "MojAdvokat <noreply@mojadvokat.me>",
        "to": to,
        "subject": subject,
        "text": message
    }
    return requests.post(
        f"https://api.eu.mailgun.net/v3/{os.environ['SERVICES_MAILGUN_DOMAIN']}/messages",
        auth = auth,
        data = data
    )
