from selenium.webdriver import Chrome, ChromeOptions

from pathlib import Path

def init_selenium():
    cachedir: Path = Path.home() / '.cache' / 'saidai_ical_generator'

    options = ChromeOptions()
    options.add_argument(f'--user-data-dir={cachedir / "UserData"}')
    options.add_argument('--profile-directory=Profile')

    return Chrome(options=options)


def destruct_selenium(driver):
    driver.close()
    driver.quit()
