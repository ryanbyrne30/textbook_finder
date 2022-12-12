import requests
import json

session = requests.Session()
session.headers = {
  "User-Agent": "Mozilla/5.0 (Linux; Android 12; Pixel 6 Build/SD1A.210817.023; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/94.0.4606.71 Mobile Safari/537.36"
}


department_codes = {
  "finance": "MFIN",
  "accounting": "ACCT",
  "computer_science": "CSCI"
}


def fetch_courses_for_year():
  base_url = "https://bcweb.bc.edu/aem/"
  targets = ["coursessprg.json", "coursessumm.json", "coursesfall.json"]
  courses = []
  for target in targets:
    response = session.get(base_url+target)
    courses += response.json()['payload']
  return courses

def get_unique_courses(courses):
  unique_courses = {}
  for course in courses:
    key = course["dept_code"] + course["crs_number"]
    if not key in unique_courses:
      unique_courses[key] = course 
  return list(unique_courses.values())


def get_courses_for_subject(subject_code:str, courses):
  return list(filter(lambda c: c['dept_code'] == subject_code, courses))




if __name__ == "__main__":
  # courses = fetch_courses_for_year()
  # with open("all_courses.json", 'w') as f:
  #   json.dump(courses, f, indent=2)
  # print(f"{len(courses)} offered this year.")

  with open('all_courses.json', 'r') as f:
    courses = json.load(f)

  unique_courses = get_unique_courses(courses)
  print(f"{len(unique_courses)} unique courses offered this year.")