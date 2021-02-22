from __future__ import annotations

from pathlib import Path
from typing import Optional
import time

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import net

from html_parser.lecture_list import LectureList
from html_parser.regist_list import RegistList

def main():
    #html: str = Path('RegistList.html').read_text(encoding='utf-8')
    #print(RegistList.parse_html(html))


    html: str = Path('LectureList.html').read_text(encoding='utf-8')
    print(LectureList.parse_html(html).as_ical())

    #driver = net.lib.init_selenium()

    #driver.get('https://www.suisss.com/members/')

    #driver.get('https://www.suisss.com/')

    #action = ActionChains(driver)

    #WebDriverWait(driver, 10).until(
    #    EC.presence_of_element_located((By.CSS_SELECTOR, 'div.login-page button'))
    #).click()

    #WebDriverWait(driver, 10).until(
    #    EC.presence_of_element_located((By.ID, 'kc-login'))
    #)

    #action.send_keys_to_element(
    #    driver.find_element_by_id('username'), 'kimotu4632uz@gmail.com'
    #).send_keys_to_element(
    #    driver.find_element_by_id('password'), '120680314a'
    #).click(
    #    driver.find_element_by_id('kc-login')
    #).perform()

    #WebDriverWait(driver, 100).until(
    #    EC.presence_of_element_located((By.CSS_SELECTOR, 'div#__layout a'))
    #)

    #(Path.cwd() / 'out.html').write_text(driver.page_source, encoding='utf-8')
    #driver.close()
    #driver.quit()

if __name__ == '__main__':
    main()