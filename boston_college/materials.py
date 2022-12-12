from typing import *
import json
from boston_college.utils import session, save_data

PROGRAMID = "2055"
STOREID = "46404"
TERMID = "100074138"

def create_payload(courses: List[str]):
  return {
    "courses": [
      {
        "departmentDisplayName": course[:4],
        "courseDisplayName": course[4:8],
        "sectionDisplayName": course[8:],
        "secondaryvalues": f"{course[:4]}/{course[4:8]}/{course[8:]}",
        "divisionDisplayName": "",
      }
      for course in courses
    ],
    "programId": PROGRAMID,
    "storeId": STOREID,
    "termId": TERMID
  }


def send_request(courses: List[str]):
  url = f"https://svc.bkstr.com/courseMaterial/results?storeId={STOREID}&langId=-1&catalogId=11077&requestType=DDCSBrowse"
  payload = create_payload(courses)
  response = session.post(url, json=payload, headers={
    "User-Agent": "Mozilla/5.0 (Linux; Android 12; Pixel 6 Build/SD1A.210817.023; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/94.0.4606.71 Mobile Safari/537.36"
  })
  if response.status_code != 200:
    print(response.content)
    raise Exception(f"Reponse returned {response.status_code}")
  return response.json()


def parse_material(material_data):
  print("\tMaterial:", material_data["title"])
  keys = [
    "title",
    "edition",
    "author",
    "publisher",
    "isbn",
    "image",
    "requirementType",
    "materialType",
  ]
  return {
    key: material_data[key] if key in material_data else None
    for key in keys
  }


def parse_course_data(course_data):
  course = course_data["course"]
  department = course_data["department"]
  section = course_data["section"]

  print(f"\nParsing course: {department}/{course}/{section}")
  try:
    materials_data = course_data["courseMaterialResultsList"]
    materials = list(map(parse_material, materials_data))
  except:
    materials = None

  return {
    "department": department,
    "course": course,
    "section": section,
    "course_full": f"{department}{course}{section}",
    "materials": materials
  }


def parse_response(data):
  course_data = data[0]["courseSectionDTO"]
  return [ parse_course_data(c) for c in course_data ]


def fetch_materials_for_courses(courses: List[str]):
  """Each course in list is of format AAAA123401 
  - AAAA = subject
  - 1234 = course id
  - 01 = section"""
  materials = []
  for i in range(0, len(courses), 30):
    print(f"Fetching materials for courses {i} - {min(len(courses), i+30)}...")
    response_data = send_request(courses[i:i+30])
    data = parse_response(response_data)
    materials += data
  return materials

if __name__ == "__main__":
  courses = [

  ]


  response_data = send_request(courses)
  data = parse_response(response_data)

  with open("books.json", 'w') as f:
    json.dump(data, f, indent=2)
