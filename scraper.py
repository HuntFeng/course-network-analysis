from bs4 import BeautifulSoup
import requests
import json
import re

def make_subject_list(year: int) -> list:
    url = f"https://www.sfu.ca/students/calendar/{year}/spring/courses.html"
    page = requests.get(url)
    soup = BeautifulSoup(page.content)

    links = soup.findAll('a', attrs={'href': re.compile("courses/")})
    subjects = [] 
    for n, link in enumerate(links):
        subject_name = link.text.split("(")[0].strip()
        subject_label = link.text.split("(")[1].strip()[:-1]  # [:-1] is to remove )

        subject = {}
        subject["name"] = subject_name
        subject["label"] = subject_label.lower()
        subjects.append(subject)

    with open("subject_list.json", "w") as f:
        json.dump(subjects, f)
    return subjects

def make_course_list(subject_label: str):
    url = f"https://www.sfu.ca/students/calendar/2020/spring/courses/{subject_label}.html"
    page = requests.get(url)
    soup = BeautifulSoup(page.content)

    # scrape all course label and course title
    h3_tags = soup.findAll("h3")
    courses = []
    for h3 in h3_tags[2:]:
        fields = h3.text.split("-")
        label = fields[0].strip()
        name = fields[1].strip().split("\n")[0]

        if label.split(" ")[1][0] in '56789':
            # CMPT 5xx, CMPT 6xx  are graduate courses, we don't want them 
            break

        # description of the course
        p = h3.find_next_sibling()
        links = p.findAll("a") # find all courses in the description
        prereq_list = [link.text for link in links] 

        # determine if the course is a prerequisite
        desc = p.text.strip()
        desc_lower = desc.lower()
        start = desc_lower.find("prerequisite")
        if desc_lower.find("corequisite") != -1:
            end = desc_lower.find("corequisite")
        elif desc_lower.find("with credit for") != -1:
            end = desc_lower.find("with credit for")
        elif desc_lower.find("may not take") != -1:
            end = desc_lower.find("may not take")
        else:
            end = len(desc)

        prereq = []
        for raw_prereq in prereq_list:
            # prereq should be in between the words "Prereqsuisite" and "may not take"
            if start < desc.find(raw_prereq) < end:
                # if the prerequisite contains only course number, we add the subject label
                if re.search("^[0-9]", raw_prereq):
                    prerequisite = subject + " " + raw_prereq
                else:
                    prerequisite = raw_prereq
                    subject = raw_prereq.split(" ")[0]
                # prerequisite cannot be the course itself
                prereq.append(prerequisite)
            else:
                break

        course = {}
        course["label"] = label
        course["name"] = name
        prereq = list(set(prereq)) # remove all duplicated things
        if label in prereq:
            prereq.remove(label) # a course cannot be a prerequisite of itself
        course["prereq"] = prereq # remove all duplicated things
        courses.append(course)

    with open(f"courses/{subject_label}.json", "w") as f:
        json.dump(courses, f)

if __name__ == "__main__":
    year = 2020
    subjects = make_subject_list(year)
    for subject in subjects:
        subject_label = subject["label"]
        subject_name = subject["name"]
        print(subject_label)
        make_course_list(subject_label)

