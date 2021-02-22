from __future__ import annotations

import os
import re
from io import BytesIO
from pathlib import Path
from zipfile import ZipFile
from typing import Optional

from requests import Response
import requests
from selenium.webdriver import Chrome as SChrome
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.webdriver import WebDriver as CWebDriver

from browser import Browser

class Chrome(Browser):
    def __init__(self, cwd: Path) -> None:
        self.__driver_home: Path = cwd / 'drivers' / 'chrome'

    @property
    def driver_home(self) -> Path:
        return self.__driver_home

    def get_version(self) -> Optional[str]:
        program_files: Optional[str] = os.getenv('PROGRAMFILES')

        if program_files is None:
            raise RuntimeError("Error: could not get program directory. maybe you're not windows?")

        chrome_64: Path = Path(program_files) / 'Google' / 'Chrome' / 'Application'

        program_files_32: Optional[str] = os.getenv('PROGRAMFILES(X86)')

        if program_files_32 is None:
            raise RuntimeError("Error: could not get program file directory for 32bit. maybe you're not windows?")

        chrome_32: Path = Path(program_files_32) / 'Google' / 'Chrome' / 'Application'

        if chrome_64.exists():
            for entry in chrome_64.iterdir():
                if entry.is_dir() and re.fullmatch(r'[0-9.]*', entry.name):
                    return entry.name

        if chrome_32.exists():
            for entry in chrome_32.iterdir():
                if entry.is_dir() and re.fullmatch(r'[0-9.]*', entry.name):
                    return entry.name

        return None


    def check_update(self) -> Optional[str]:
        driver_version: str = (self.driver_home / 'version').read_text()
        browser_version: Optional[str] = self.get_version()

        if browser_version is None:
            raise RuntimeError('Error: could not find chrome')

        version_resp: Response = requests.get('https://chromedriver.storage.googleapis.com/LATEST_RELEASE_' + browser_version.rsplit('.')[0])
        version_resp.raise_for_status()
        
        if version_resp.text == driver_version:
            return None
        else:
            return version_resp.text


    def get_driver(self, version: str) -> None:
        version_resp: Response = requests.get('https://chromedriver.storage.googleapis.com/LATEST_RELEASE_' + version.rsplit('.')[0])
        version_resp.raise_for_status()

        if re.fullmatch(r'[0-9.]*', version_resp.text):
            driver_resp: Response = requests.get(f'https://chromedriver.storage.googleapis.com/{version_resp.text}/chromedriver_win32.zip')
            driver_resp.raise_for_status()

            self.driver_home.mkdir(parents=True, exist_ok=True)
            ZipFile(BytesIO(driver_resp.content)).extractall(path=self.driver_home)
            (self.driver_home / 'version').write_text(version_resp.text)

    
    def finish(self) -> CWebDriver:
        options = ChromeOptions()
        #options.add_argument('--headless')
        options.add_argument(f'--user-data-dir={self.driver_home / "UserData"}')
        options.add_argument('--profile-directory=Profile')

        return SChrome(executable_path=self.driver_home / 'chromedriver', options=options)
