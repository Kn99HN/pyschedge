import json
import logging
import requests as re
from pyschedge.SchedgeException import SchedgeException

logger = logging.getLogger(__name__)

valid_sem = ["fa", "sp", "su", "ja"]
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.5",
}


class Schedge(object):
    def __init__(self, sem, year):
        """
        Create a Schedge API client

        Args:
            sem (str):
            semester code, can only be 'fa','sp','ja','su'
            year (int): the year requested for data

        Raises:
            SchedgeException:
            an exception indicating
            error with message
        """
        if sem not in sem:
            raise SchedgeException(-1, -1, "", reason="Invalid Semester Code")
        self._prefix = "https://schedge.a1liu.com"
        self.sem = sem
        self.year = year
        self._session = re.Session()

    def _internal_call(self, method, url):
        """
        Creating a session.
        https://requests.readthedocs.io/en/master/user/advanced/

        Args:
            method (str): type of request
            url (str): URL for making the request

        Raises:
            SchedgeException:
            an exception indicating
            error with message

        Returns:
            list[str]: Arrays of JSON from the request
        """
        logger.debug("Sending %s to %s with Headers: %s", method, url, headers)
        try:
            resp = self._session.request(method, url, headers=headers)
            resp.raise_for_status()
            results = resp.json()
        except re.exceptions.HTTPError as e:
            msg = ""
            if resp.status_code == 400:
                msg = resp.json()["message"]
            else:
                msg = e.message()
            logger.error(
                "HTTP Error for %s to %s returned %s due to %s",
                method,
                url,
                resp.status_code,
                msg,
            )
            raise SchedgeException(resp.status_code, -1, msg)
        except Exception as e:
            logger.error("Error returned due to %s", e.message())
            raise SchedgeException(-1, -1, e.message())
        return results

    def get_courses(self, school, subject, full=False):
        url = f"{self._prefix}/{self.year}/{self.sem}/{school}/{subject}?full={full}"
        return self._internal_call("GET", url)

    def get_section(self, registration_number, full=False):
        url = f"{self._prefix}/{self.year}/{self.sem}/{registration_number}?full={full}"
        return self._internal_call("GET", url)

    def get_non_online(self):
        url = f"{self._prefix}/{self.year}/{self.sem}/notOnline"
        return self._internal_call("GET", url)

    def check_schedule(self, *argv):
        schedule = ""
        for arg in argv:
            schedule += f"{arg},"
        url = f"{self.prefix}/{self.year}/{self.sem}/generateSchedule?registrationNumbers={schedule}"
        return self._internal_call("GET", url)

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
        url = """
            {prefix}/{year}/{sem}/search?query={query}&
            titleWeight={title_weight}&
            descriptionWeight={description_weight}&
            prereqs_weight={prereqs_weight}&
            full={full}
            &limit={limit}""".format(
            prefix=self._prefix,
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
        return self._internal_call("GET", url)
