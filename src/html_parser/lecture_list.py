from __future__ import annotations

from pathlib import Path
from typing import Optional, cast
from dataclasses import dataclass
from datetime import date, time, datetime, timedelta
import re

from bs4 import BeautifulSoup, Tag
import itertools
from tzlocal import get_localzone

@dataclass(frozen=True)
class DateTimeSet:
    start_date: date
    end_date: date
    start_time: time
    end_time: time
    exclude_dates: list[date]


@dataclass(frozen=True)
class LectureList:
    name: str
    teacher: str
    code: str
    timetable: list[DateTimeSet]

    @classmethod
    def parse_html(cls, html: str) -> Optional[LectureList]:
        doc = BeautifulSoup(html, 'html.parser')

        name_e: Optional[Tag] = doc.select_one('a#ctl00_phContents_ucLctList_ucLctHeader_lnkSbjNm')
        teacher_e: Optional[Tag] = doc.select_one('#ctl00_phContents_ucLctList_ucLctHeader_lblStaffNm')
        code_e: Optional[Tag] = doc.select_one('#ctl00_phContents_ucLctList_ucLctHeader_lblLctCdy')

        if name_e is None and teacher_e is None and code_e is None:
            return None
        
        name: str = '' if name_e is None else name_e.text
        teacher: str = '' if teacher_e is None else teacher_e.text
        code: str = '' if code_e is None else code_e.text

        open_days: Optional[Tag] = doc.select_one('#ctl00_phContents_ucLctList_ucLctHeader_lblDayPeriodShort')
        open_days_list: list[str] = cast(Tag, open_days).text.split(',')

        timetable_days: dict[str, list[date]] = dict(itertools.zip_longest(map(lambda s: s[0], open_days_list), [[]], fillvalue=[]))

        start_time: Optional[time] = None
        end_time: Optional[time] = None

        re_date = re.compile(r'(\d{4})/(\d{2})/(\d{2})\((.{1})\)')
        re_time = re.compile(r'(\d{2}):(\d{2})～(\d{2}):(\d{2})')

        first = True
        for line in doc.select_one(r'#ctl00_phContents_ucLctList_gv').children:
            if line.name == 'tr':
                if first:
                    first = False
                else:
                    for item in line.children:
                        if item.name == 'td':
                            cap = re_date.fullmatch(item.text)

                            if cap is not None:
                                if cap[4] in timetable_days:
                                    timetable_days[cap[4]].append(date(int(cap[1]), int(cap[2]), int(cap[3])))
                
                            else:
                                cap = re_time.fullmatch(item.text)

                                if cap is not None and start_time is None:
                                    start_time = time(int(cap[1]), int(cap[2]))
                                    end_time = time(int(cap[3]), int(cap[4]))

        timetable: list[DateTimeSet] = []

        for dates in timetable_days.values():
            start_date = dates[0]
            end_date = dates[-1]
            exclude_dates: list[date] = []

            current = start_date + timedelta(weeks=1)

            for target_date in dates[1:]:
                while True:
                    if current < target_date:
                        exclude_dates.append(current)
                        current += timedelta(weeks=1)
                    else:
                        current += timedelta(weeks=1)
                        break
            
            timetable.append(DateTimeSet(start_date, end_date, cast(time, start_time), cast(time, end_time), exclude_dates))
        
        return cls(name, teacher, code, timetable)
 

    def as_ical(self) -> str:
        ical = ['BEGIN:VCALENDAR', 'VERSION:2.0', 'PRODID:-//org//me//JP']

        tz_local = get_localzone()

        for date in self.timetable:
            vevent = ['BEGIN:VEVENT']

            dtstart = tz_local.localize(datetime.combine(date.start_date, date.start_time))
            dtend = tz_local.localize(datetime.combine(date.start_date, date.end_time))
            rrule_until = tz_local.localize(datetime.combine(date.end_date, date.end_time))

            vevent.append(f"DTSTART;TZID={tz_local.zone}:{dtstart.strftime(r'%Y%m%dT%H%M%S')}")
            vevent.append(f"DTEND;TZID={tz_local.zone}:{dtend.strftime(r'%Y%m%dT%H%M%S')}")
            vevent.append(f"RRULE:FREQ=WEEKLY;UNTIL={rrule_until.strftime(r'%Y%m%dT%H%M%S')}Z")

            for exdate in date.exclude_dates:
                vevent.append('EXDATE;TZID={}:{}'.format(tz_local.zone, tz_local.localize(datetime.combine(exdate, date.start_time)).strftime(r'%Y%m%dT%H%M%S')))

            vevent.append(f'SUMMARY:{self.name}')
            vevent.append(f'DESCRIPTION:{self.teacher}, {self.code}')

            vevent.append('END:VEVENT')
            ical.append('\n'.join(vevent))


        ical.append('END:VCALENDAR')
        return '\n'.join(ical)
