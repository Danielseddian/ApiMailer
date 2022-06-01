import requests

from DjangoApiMailer.settings import MAILING_URL, MAILING_TOKEN


def send_message(message_body, url=MAILING_URL, token=MAILING_TOKEN):
    header = {"Authorization": f"Bearer {token}"}
    return requests.post(url, message_body, )
