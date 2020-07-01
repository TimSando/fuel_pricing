import base64
import json
import logging
import os
import requests
import sqlite3
import uuid

from datetime import datetime, timezone

from settings import BusinessRules

log = logging.getLogger(__name__)


class FuelAPI:
    def __init__(
        self, api_key, api_secret, url="https://api.onegov.nsw.gov.au", grant_type="client_credentials"
    ):
        self.api_key = api_key
        self.api_secret = api_secret
        self.url = url
        self.grant_type = grant_type
        self.auth()

    def auth(self):
        auth_bytes = f"{self.api_key}:{self.api_secret}".encode("utf-8")
        auth_b64 = base64.b64encode(auth_bytes)
        api_auth = auth_b64.decode("utf-8")
        r = requests.get(
            url=f"{self.url}{BusinessRules.ENDPOINTS['Auth']}",
            params={"grant_type": self.grant_type},
            headers={"Authorization": api_auth},
        )
        resp = r.json()
        self._token = resp["access_token"]

    def allresults(self):
        t = datetime.now(timezone.utc)
        stime = t.strftime("%d/%m/%Y %I:%M:%S")
        headers = {
            "Authorization": f"Bearer {self._token}",
            "Content-Type": "application/json",
            "apikey": self.api_key,
            "transactionid": str(uuid.uuid4()),
            "requesttimestamp": stime,
        }
        r = requests.get(url=f"{self.url}{BusinessRules.ENDPOINTS['AllPrices']}", headers=headers)
        resp = r.json()
        with open("prices.json", "w") as f:
            json.dump(resp, f)


if __name__ == "__main__":
    f = FuelAPI(BusinessRules.API_KEY, BusinessRules.API_SECRET)
    if os.path.exists("prices.json"):
        fmod = os.path.getmtime("prices.json")
        fmodd = datetime.fromtimestamp(fmod).date()
        d = datetime.now().date()
        if fmodd < d:
            f.allresults()
            log.info("Price data has been updated")
        log.info("Price data wasn't updated")
    else:
        f.allresults()
