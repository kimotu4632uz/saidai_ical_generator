from __future__ import annotations

from pathlib import Path
from typing import Optional
from dataclasses import dataclass

from bs4 import BeautifulSoup, Tag

@dataclass
class RegistList:
    ids: list[str]

    @classmethod
    def parse_html(cls, html: str) -> RegistList:
        doc = BeautifulSoup(html, 'html.parser')

        idlist: set[str] = set()

        for day in ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]:
            for time in range(1, 8):
                for id_div in doc.select(f'#ctl00_phContents_rrMain_ttTable_td{day}{time} > div'):
                    id_first: str = id_div['id'].rsplit('_', 1)[0]
                    span: Optional[Tag] = doc.select_one(f'span#{id_first}_lblLctCd')

                    if span is not None:
                        if len(span.text) > 0:
                            idlist.add(span.text)

        return cls(list(idlist))
