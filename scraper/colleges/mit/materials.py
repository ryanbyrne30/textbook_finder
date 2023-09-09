import urllib.parse
import requests
from bs4 import BeautifulSoup

BOOKSTORE_URL = "https://mitcoopbooks.bncollege.com/course-material-caching/course"
MIT_CAMPUS = 304
MIT_SECTION = 1
CURRENT_TERM = "23_F"


class Material:
    def __init__(
        self,
        title: str,
        author: str,
        edition: str,
        publisher: str,
        isbn: str,
    ) -> None:
        self.title = title
        self.author = author
        self.edition = edition
        self.publisher = publisher
        self.isbn = isbn

    def __str__(self) -> str:
        return f"Material('{self.title}', '{self.author}', '{self.edition}', '{self.isbn}')"


class MITMaterialsScraper:
    def __init__(self) -> None:
        pass

    def get_materials(self, department: str, course_id: str):
        params = {
            "campus": MIT_CAMPUS,
            "term": f"{MIT_CAMPUS}_{MIT_SECTION}_{CURRENT_TERM}",
            "course": f"{MIT_CAMPUS}_{MIT_SECTION}_{CURRENT_TERM}_{department}_.{course_id}_1",
            "section": MIT_SECTION,
            "oer": False,
        }
        url = BOOKSTORE_URL + urllib.parse.urlencode(params)
        html = self.get_material_html(url)
        return html
        soup = self.get_material_soup(soup)

    def get_material_html(self, url: str):
        response = requests.get(url)
        return response.content

    def get_material_soup(self, html: str):
        return BeautifulSoup(html, "html.parser")

    def get_materials_from_soup(self, soup: BeautifulSoup):
        material_blocks = soup.select(".bned-item-details-container")
        materials = []
        for block in material_blocks:
            title = block.select_one(".js-bned-item-name-text").text.strip()
            author = block.select_one(".author").text.strip()
            edition = (
                block.select_one('[data-code="courseMaterial.plp.edition"]')
                .parent.parent.select_one(".value")
                .text.strip()
            )
            publisher = (
                block.select_one("[data-code='courseMaterial.plp.publisher']")
                .parent.parent.select_one(".value")
                .text.strip()
            )
            isbn = (
                block.select_one("[data-code='courseMaterial.plp.isbn.thirteen']")
                .parent.parent.select_one(".value")
                .text.strip()
            )
            materials.append(Material(title, author, edition, publisher, isbn))
        return materials


if __name__ == "__main__":
    ms = MITMaterialsScraper()
    dep = 6
    cid = "100B"
    # html = ms.get_materials(dep, cid)

    with open("materials.html", "r") as f:
        html = f.read()

    soup = ms.get_material_soup(html)
    materials = ms.get_materials_from_soup(soup)

    for m in materials:
        print(m)
