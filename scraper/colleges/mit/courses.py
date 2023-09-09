import requests
from bs4 import BeautifulSoup


class Course:
    def __init__(self, name: str, department: str, course_id: str) -> None:
        self.name = name
        self.department = department
        self.course_id = course_id

    def __str__(self) -> str:
        return f"Course('{self.name}', '{self.department}.{self.course_id}')"


class MITCoursesScraper:
    def __init__(self, subject_url: str) -> None:
        self.url = subject_url

    def get_courses(self) -> [Course]:
        html = self.get_html()
        soup = self.get_soup(html)
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

    def get_html(self):
        response = requests.get(self.url)
        return response.content

    def get_soup(self, html: str):
        return BeautifulSoup(html, "html.parser")


if __name__ == "__main__":
    url = "http://student.mit.edu/catalog/m1a.html"
    cs = MITCoursesScraper(url)
    courses = cs.get_courses()

    for c in courses:
        print(c)
