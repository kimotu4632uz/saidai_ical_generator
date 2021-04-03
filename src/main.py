from __future__ import annotations

from pathlib import Path
from typing import Optional
from argparse import ArgumentParser
from datetime import date

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from net.lib import init_selenium, destruct_selenium

from html_parser.lecture_list import LectureList
from html_parser.regist_list import RegistList


def perform_auth(driver, user, passwd):
    driver.get('https://www.suisss.com/')

    action = ActionChains(driver)

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div.login-page button'))
    ).click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'kc-login'))
    )

    action.send_keys_to_element(
        driver.find_element_by_id('username'), user
    ).send_keys_to_element(
        driver.find_element_by_id('password'), passwd
    ).click(
        driver.find_element_by_id('kc-login')
    ).perform()

    WebDriverWait(driver, 100).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div#__layout a'))
    )

    driver.get('https://risyu.saitama-u.ac.jp/Test/OpenConnect.aspx')
    WebDriverWait(driver, 100).until(
        EC.presence_of_element_located((By.ID, 'ctl00_body'))
    )


def get_lecture_list(driver, year, id):
    driver.get(f'https://risyu.saitama-u.ac.jp/test/StudentApp/Lct/LectureList.aspx?lct_year={year}&lct_cd={id}')
    WebDriverWait(driver, 100).until(
        EC.presence_of_element_located((By.ID, 'ctl00_phContents_ucLctList_ucLctHeader_lblLctYear'))
    )

    return driver.page_source


def get_regist_list(driver):
    driver.get('https://risyu.saitama-u.ac.jp/Test/OpenConnect.aspx')
    WebDriverWait(driver, 100).until(
        EC.presence_of_element_located((By.ID, 'ctl00_bhHeader_LinkButtonRegist_Results'))
    ).click()
    WebDriverWait(driver, 100).until(
        EC.presence_of_element_located((By.ID, 'ctl00_bhHeader_HyperLinkSchedule'))
    ).click()
    WebDriverWait(driver, 100).until(
        EC.presence_of_element_located((By.ID, 'ctl00_phContents_rrMain_ttTable_lctMon1_ctl00_divDetail'))
    )

    return driver.page_source


def main():
    parser = ArgumentParser(description='Generate ical file from saidai-student-page.')
    parser.add_argument('-u', '--user', required=True, help='username')
    parser.add_argument('-p', '--password', required=True, help='password')
    parser.add_argument('-a', '--auto-mode', action='store_true',help='get classids from register page.')
    parser.add_argument('-i', '--ids', nargs='*', help='classids to generate ical.')
    parser.add_argument('-o', '--output', help='prefix of output ical file.')
    parser.add_argument('-y', '--year', help='year of target class. by default, use current UTC year.')

    args = parser.parse_args()

    if not args.auto_mode and args.ids is None:
        print('Error: Please set mode flag or ids.')
        exit(1)
    
    if args.auto_mode and args.year is not None:
        print('Error: Cannot use both auto mode and year option same time.')
        exit(1)
    
    file_prefix = '' if args.output is None else args.output + '_'
    year = str(date.today().year) if args.year is None else args.year

    driver = init_selenium()
    perform_auth(driver, args.user, args.password)

    if args.auto_mode:
        regist_list_html = get_regist_list(driver)
        ids = RegistList.parse_html(regist_list_html).ids
    else:
        ids = args.ids

    for classid in ids:
        lecture_list_html = get_lecture_list(driver, year, classid)
        lec = LectureList.parse_html(lecture_list_html)
        
        if lec is None:
            print(f'Warning: canoot get information about classid {classid}. skipping...')
        else:
            (Path.cwd() / (file_prefix + classid + '.ics')).write_text(lec.as_ical(), encoding='utf-8')
    
    destruct_selenium(driver)


if __name__ == '__main__':
    main()