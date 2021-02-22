from __future__ import annotations

import os
from pathlib import Path
from configparser import ConfigParser
from typing import Optional

from requests import Response
import requests
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.webdriver import WebDriver as FWebDriver

from browser import Browser

class FireFox(Browser):
    def __init__(self, cwd: Path) -> None:
        self.__driver_home: Path = Path(cwd) / 'drivers' / 'firefox'

    @property
    def driver_home(self) -> Path:
        return self.__driver_home

    def get_version(self) -> Optional[str]:
        program_files: Optional[str] = os.getenv('PROGRAMFILES')

        if program_files is None:
            raise RuntimeError("Error: could not get program file directory. maybe you're not windows?")

        firefox_64: Path = Path(program_files) / 'Mozilla Firefox' / 'application.ini'

        if firefox_64.exists():
            ini = ConfigParser()
            ini.read(firefox_64, 'utf-8')
            version: str = ini['App']['Version']

            if version is None:
                raise RuntimeError('Error: firefox config file is broken.')

            return version

        return None
    
    def check_update(self) -> Optional[str]:
        pass
    
    def get_driver(self, version: str):
        pass

    def finish(self):
        pass
