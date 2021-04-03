from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional
from pathlib import Path

from selenium.webdriver.chrome.webdriver import WebDriver as CWebDriver
from selenium.webdriver.firefox.webdriver import WebDriver as FWebDriver


class Browser(ABC):
    @property
    @abstractmethod
    def driver_home(self) -> Path:
        pass

    @abstractmethod
    def get_version(self) -> Optional[str]:
        pass

    @abstractmethod
    def check_update(self) -> Optional[str]:
        pass

    @abstractmethod
    def get_driver(self, version: str) -> None:
        pass

    @abstractmethod
    def finish(self) -> CWebDriver | FWebDriver:
        pass
