from collections.abc import Iterable
import requests
from bs4 import BeautifulSoup
import json
from time import sleep
from random import randrange


class Course:
    def __init__(self, name: str, department: str, course_id: str) -> None:
        self.name = name
        self.department = department
        self.course_id = course_id

    def to_dict(self):
        return {"name": self.name, "department": self.department, "cid": self.course_id}

    def __str__(self) -> str:
        return f"Course('{self.name}', '{self.department}.{self.course_id}')"


class MITCoursesScraper:
    def __init__(self, subject_url: str) -> None:
        self.url = subject_url
        subject = subject_url.split("/")[-1]
        self.url_base = subject_url[: -len(subject) - 1]

    def get_courses(self) -> [Course]:
        html = self.get_html()
        soup = self.get_soup(html)
        page_urls = self.get_pagination_links(soup)
        courses = self.get_page_courses(soup)

        print("Finished scraping first page", self.url)
        print(f"{len(page_urls)} more to go")
        for page_url in page_urls:
            sleep_time = randrange(10, 50) / 10
            print(f"Sleeping {round(sleep_time, 1)} seconds")
            sleep(sleep_time)
            print("Scraping", page_url)
            page_html = self.get_html(page_url)
            page_soup = self.get_soup(page_html)
            courses += self.get_page_courses(page_soup)
        return courses

    def get_pagination_links(self, soup: BeautifulSoup):
        page_link_tags = soup.select("table > tr > td > table > tr b a")
        return [self.url_base + "/" + p.attrs["href"] for p in page_link_tags]

    def get_page_courses(self, soup: BeautifulSoup):
        tags = soup.select("h3")
        courses = []
        for tag in tags:
            words = tag.text.strip().split(" ")
            course_id = words[0]
            dep = course_id.split(".")[0]
            cid = course_id.split(".")[1].replace("[J]", "")
            title = " ".join(words[1:])
            courses.append(Course(title, dep, cid))
        return courses

    def get_html(self, url=None):
        response = requests.get(url if url is not None else self.url)
        return response.content

    def get_soup(self, html: str):
        return BeautifulSoup(html, "html.parser")


if __name__ == "__main__":
    url = "http://student.mit.edu/catalog/m6e.html"
    cs = MITCoursesScraper(url)
    courses = cs.get_courses()
    courses = sorted(courses, key=lambda c: c.course_id)

    with open("courses.json", "w") as f:
        json.dump([c.to_dict() for c in courses], f, indent=2)

    print(len(courses), "courses found")
