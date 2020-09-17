import json
import logging
import requests as re
from src.SchedgeException import SchedgeException

logger = logging.getLogger(__name__)

sem = ["fa", "sp", "su", "ja"]


class Schedge(object):
    def __init__(self, sem, year):
        self.prefix = "https://schedge.a1liu.com"
        self.sem = sem
        self.year = year
        self.session = re.Session()

    def get_courses(self, school, subject, full=False):
        url = f"{self.prefix}/{self.year}/{self.sem}/{school}/{subject}?full={full}"
        resp = re.get(url)
        try:
            resp.raise_for_status()
        except re.exceptions.HTTPError as e:
            msg = ""
            if resp.status_code == 400:
                msg = resp.json()["message"]
            else:
                msg = e.message()
            logger.error("Error: {}".format(msg))
            raise SchedgeException(resp.status_code, -1, msg)
        return resp.json()

    def get_section(self, registration_number, full=False):
        url = f"{self.prefix}/{self.year}/{self.sem}/{registration_number}?full={full}"
        resp = re.get(url)
        try:
            resp.raise_for_status()
        except re.exceptions.HTTPError as e:
            msg = ""
            if resp.status_code == 404:
                msg = "Section not found for {}".format(registration_number)
            else:
                msg = e.message()
            logger.error(msg)
            raise SchedgeException(resp.status_code, -1, msg)
        return resp.json()

    def get_non_online(self):
        url = f"{self.prefix}/{self.year}/{self.sem}/notOnline"
        try:
            resp = re.get(url)
            return resp.json()
        except re.exceptions.HTTPError as e:
            msg = e.message()
            logger.error(msg)
            raise SchedgeException(resp.status_code, -1, msg)

    def check_schedule(self, *argv):
        schedule = ""
        for arg in argv:
            schedule += f"{arg},"
        url = f"{self.prefix}/{self.year}/{self.sem}/generateSchedule?registrationNumbers={schedule}"
        resp = re.get(url)
        try:
            resp.raise_for_status()
        except re.exceptions.HTTPError as e:
            msg = ""
            if resp.status_code == 400:
                msg = "Invalid input string for {}".format(resp.json()["message"])
            else:
                msg = e.message()
            logger.error(msg)
            raise SchedgeException(resp.status_code, -1, msg)
        return resp.json()

    def search_course(
        self,
        query,
        school="",
        subject="",
        title_weight=2,
        description_weight=1,
        notes_weight=0,
        prereqs_weight=0,
        full=False,
        limit=50,
    ):
        url = "{prefix}/{year}/{sem}/search?query={query}&titleWeight={title_weight}&descriptionWeight={description_weight}&prereqs_weight={prereqs_weight}&full={full}&limit={limit}".format(
            prefix=self.prefix,
            year=self.year,
            sem=self.sem,
            query=query,
            title_weight=title_weight,
            description_weight=description_weight,
            notes_weight=notes_weight,
            prereqs_weight=prereqs_weight,
            full=full,
            limit=limit,
        )
        if school != "":
            url = f"{url}&school={school}"
        if subject != "":
            subject = f"{url}&subject={subject}"
        resp = re.get(url)
        try:
            resp.raise_for_status()
        except re.exceptions.HTTPError as e:
            msg = ""
            if resp.status_code == 400:
                msg = "Invalid input string for {}".format(resp.json()["message"])
            else:
                msg = e.message()
            logger.error(msg)
            raise SchedgeException(resp.status_code, -1, msg)
        return resp.json()
