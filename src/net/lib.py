from __future__ import annotations

from pathlib import Path
from typing import Optional

from chrome import Chrome
from firefox import FireFox

def init_selenium(ignore_default=False):
    default: Path = Path.cwd() / 'drivers' / 'default'

    if ignore_default or not default.exists():
        for name, instance in [('chrome', Chrome(Path.cwd())), ('firefox', FireFox(Path.cwd()))]:
            version: Optional[str] = instance.get_version()

            if version is None:
                continue

            default.parent.mkdir(parents=True, exist_ok=True)
            default.write_text(name)
            instance.get_driver(version)
            return instance.finish()

        print("Error: any browser found")
        exit(1)

    else:
        default_browser: str = default.read_text()

        if default_browser == 'chrome':
            instance = Chrome(Path.cwd())
        elif default_browser == 'firefox':
            instance = FireFox(Path.cwd())

        version_result: Optional[str] = instance.check_update()

        if version_result is not None:
            instance.get_driver(version_result)

        return instance.finish()
