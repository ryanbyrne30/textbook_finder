import requests
from bs4 import BeautifulSoup


class Subject:
    def __init__(self, name: str, url: str) -> None:
        self.name = name
        self.url = url

    def __str__(self) -> str:
        return f"Subject('{self.name}', '{self.url}')"


class MITSubjectsScraper:
    def __init__(self) -> None:
        self.url_base = "http://student.mit.edu/catalog"
        self.url = f"{self.url_base}/index.cgi"

    def get_html(self):
        response = requests.get(self.url)
        return response.content

    def get_soup(self, html: str):
        return BeautifulSoup(html, "html.parser")

    def get_subjects(self, soup: BeautifulSoup) -> [Subject]:
        tags = soup.select("li a")
        subjects = []
        for tag in tags:
            url = self.url_base + "/" + tag.attrs["href"]
            name = tag.text.strip()
            subjects.append(Subject(name, url))
        return subjects


if __name__ == "__main__":
    mit_subjects = MITSubjectsScraper()
    html = mit_subjects.get_html()
    soup = mit_subjects.get_soup(html)
    subjects = mit_subjects.get_subjects(soup)
    for s in subjects:
        print(s)
