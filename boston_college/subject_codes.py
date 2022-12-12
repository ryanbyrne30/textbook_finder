from bs4 import BeautifulSoup
import requests
import json 

session = requests.Session()
session.headers = {
  "User-Agent": "Mozilla/5.0 (Linux; Android 12; Pixel 6 Build/SD1A.210817.023; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/94.0.4606.71 Mobile Safari/537.36"
}

def parse_subjects_from_html(html):
  soup = BeautifulSoup(html, "html.parser")
  labels = soup.select("li#subject label")
  labels = labels[1:] # removing "All" from subjects
  data = {}
  for label in labels:
    key, val = label.text.split('-')
    key = key.strip()
    val = val.strip()
    data[key] = val
  return data


def fetch_subjects():
  url = "https://services.bc.edu/PublicCourseInfoSched/courseinfoschedResults!displayInput.action?authenticated=false&keyword=&presentTerm=2022FALL&registrationTerm=2023SPRG&termsString=2023SPRG%2C2022SUMM%2C2022FALL&selectedTerm=2023SPRG&selectedSort=&selectedSchool=6CSOM&selectedSubject=nullAll&selectedNumberRange=All&selectedLevel=&selectedMeetingDay=All&selectedMeetingTime=All&selectedCourseStatus=All&selectedCourseCredit=All&canvasSearchLink=&personResponse=jddFRnpc2ndcGlR5zrRWzc85sH&googleSiteKey=6LdV2EYUAAAAACy8ROcSlHHznHJ64bn87jvDqwaf"
  response = session.get(url)
  html = response.content
  return parse_subjects_from_html(html)


if __name__ == "__main__":
  subjects = fetch_subjects()
  print(f"Found {len(subjects)} subjects")

  with open('subjects.json', 'w') as f:
    json.dump(subjects, f, indent=2)