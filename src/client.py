import json
import logging
import requests as re

sem = ['fa', 'sp', 'su', 'ja']

class Schedge(object):
    
    def __init__(self, sem, year):
        self.prefix = "https://schedge.a1liu.com"
        self.sem = sem
        self.year = year
    
    def get_courses(self, school, subject, full=False):
        url = f"{self.prefix}/{self.year}/{self.sem}/{school}/{subject}?full={full}"
        try:
            resp = re.get(url)
            return resp.json()
        except Exception as e:
            print(e)
    
    def get_section(self, registration_number, full=False):
        url = f"{self.prefix}/{self.year}/{self.sem}/{registration_number}?full={full}"
        try:
            resp = re.get(url)
            return resp.json()
        except Exception as e:
            print(e)

    def get_non_online(self):
        url = f"{self.prefix}/{self.year}/{self.sem}/notOnline"
        try:
            resp = re.get(url)
            return resp.json()
        except Exception as e:
            print(e)

    def check_schedule(self, *argv):
        schedule =  ""
        for arg in argv:
            schedule += f'{arg},'
        url = f"{self.prefix}/{self.year}/{self.sem}/generateSchedule?registrationNumbers={schedule}"
        try:
            resp = re.get(url)
            return resp.json()
        except Exception as e:
            print(e)
    
    # def search_course(self, query, 
    # school="", subject="", title_weight=2, description_weight=1, notes_weight=0,
    # prereqs_weight=0, full=False, limit=10):
    #     url = """{prefix}/{year}/{sem}/search?\
    #     query={query}&subject={subject}&school={school}&titleWeight={title_weight}
    #     &descriptionWeight={description_weight}
    #     &notesWeight={notes_weight}&prereqsWeight={prereqs_weight}
    #     &full={full}&limit={limit}"""\
    #     .format(prefix=self.prefix, 
    #     year=self.year, sem=self.sem,
    #     query=query, subject=subject,
    #     school=school, title_weight=title_weight,
    #     description_weight=description_weight,
    #     notes_weight=notes_weight, prereqs_weight=prereqs_weight,
    #     full=full, limit=limit)
    #     print(url)
    #     try:
    #         resp = re.get(url)
    #         return resp.json()
    #     except Exception as e:
    #         print(e)
        


