from __future__ import annotations

from pathlib import Path
from typing import Optional
from argparse import ArgumentParser
from datetime import date

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from .driver import init_selenium, destruct_selenium

from .html_parser.lecture_list import LectureList
from .html_parser.regist_list import RegistList


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
        driver.find_element(By.ID, 'username'), user
    ).send_keys_to_element(
        driver.find_element(By.ID, 'password'), passwd
    ).click(
        driver.find_element(By.ID, 'kc-login')
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
    parser = ArgumentParser(description='授業のスケジュールをicsファイルに出力する')
    parser.add_argument('-u', '--user', required=True, help='suポータルのユーザー名')
    parser.add_argument('-p', '--password', required=True, help='suポータルのパスワード')
    parser.add_argument('-a', '--auto-mode', action='store_true', help='履修している授業を自動で取得する')
    parser.add_argument('-i', '--ids', nargs='*', help='取得する授業のID')
    parser.add_argument('-o', '--output', help='出力ファイルのプレフィックス')
    parser.add_argument('-y', '--year', help='対象の授業の開講年。省略された場合、現在の年を用いる。')
    parser.add_argument('-b', '--bundle', help='出力ファイルをBUNDLEにまとめる。')

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

    ics_start = ['BEGIN:VCALENDAR', 'VERSION:2.0', 'PRODID:-//org//me//JP']

    for classid in ids:
        lecture_list_html = get_lecture_list(driver, year, classid)
        lec = LectureList.parse_html(lecture_list_html)
        
        if lec is None:
            print(f'Warning: canoot get information about classid {classid}. skipping...')
        else:
            if args.bundle is None:
                ics = '\n'.join(['BEGIN:VCALENDAR', 'VERSION:2.0', 'PRODID:-//org//me//JP', lec.as_ical(), 'END:VCALENDAR'])
                (Path.cwd() / (file_prefix + classid + '.ics')).write_text(ics, encoding='utf-8')
            else:
                ics_start.append(lec.as_ical())
    
    if args.bundle is not None:
        ics_start.append('END:VCALENDAR')
        (Path.cwd() / args.bundle).write_text('\n'.join(ics_start), encoding='utf-8')

    destruct_selenium(driver)


if __name__ == '__main__':
    main()