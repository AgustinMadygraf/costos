"""
Cliente liviano para lectura de Google Sheets.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


SHEETS_READONLY_SCOPE = "https://www.googleapis.com/auth/spreadsheets.readonly"


def extract_spreadsheet_id(spreadsheet_url_or_id: str) -> str:
    raw = spreadsheet_url_or_id.strip()
    marker = "/spreadsheets/d/"
    if marker in raw:
        tail = raw.split(marker, maxsplit=1)[1]
        return tail.split("/", maxsplit=1)[0]
    return raw


def build_sheets_service(service_account_file: str) -> Any:
    """
    Construye el servicio de Google Sheets API con credenciales de service account.
    Importes diferidos para no cargar dependencias fuera de uso.
    """
    from google.oauth2.service_account import Credentials
    from googleapiclient.discovery import build

    credentials = Credentials.from_service_account_file(
        service_account_file,
        scopes=[SHEETS_READONLY_SCOPE],
    )
    return build("sheets", "v4", credentials=credentials, cache_discovery=False)


@dataclass(frozen=True)
class GoogleSheetsReader:
    spreadsheet_id: str
    service: Any

    def read_range(self, a1_range: str) -> list[list[str]]:
        response = (
            self.service.spreadsheets()
            .values()
            .get(spreadsheetId=self.spreadsheet_id, range=a1_range)
            .execute()
        )
        values = response.get("values", [])
        return [list(map(str, row)) for row in values]

