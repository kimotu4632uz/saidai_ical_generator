from selenium.webdriver import Chrome, ChromeOptions
import chromedriver_binary

from pathlib import Path

def init_selenium():
    cwd: Path = Path(__file__).resolve().parent

    options = ChromeOptions()
    options.add_argument(f'--user-data-dir={cwd / "UserData"}')
    options.add_argument('--profile-directory=Profile')

    return Chrome(options=options)


def perform_first_auth():
    cwd: Path = Path(__file__).resolve().parent
    print(f'please run chromium --user-data-dir={cwd / "UserData"} --profile-directory=Profile')


def destruct_selenium(driver):
    driver.close()
    driver.quit()
