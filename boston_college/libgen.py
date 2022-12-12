from bs4 import BeautifulSoup
from utils import session

def search_material(query: str):
  query = query.replace(' ', '+')
  url = f"https://libgen.rs/search.php?req={query}&open=0&res=100&view=simple&phrase=1&column=def"
  print("Url", url)
  response = session.get(url)
  print("Response", response.status_codes)

  # html = response.content
  # soup = BeautifulSoup(html, "html.parser")
  # results = soup.select("table.c > tr")[1:]
  # for result in results:
  #   print(result.text)

if __name__ == "__main__":
  search_material("Financial Accounting Libby")

