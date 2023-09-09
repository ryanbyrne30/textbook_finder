import boston_college as bc


if __name__ == "__main__":
  ### fetch and save all subjects
  # subjects = bc.fetch_subjects()
  # bc.utils.save_data(subjects, 'subjects.json')

  ### fetch all courses for year
  # courses = bc.fetch_courses_for_year()
  # unique_courses = bc.get_unique_courses(courses)
  # bc.utils.save_data(courses, 'all_courses.json')
  # bc.utils.save_data(unique_courses, 'unique_courses.json')

  ### get all courses for subject
  subject = "TMNT"
  unique_courses = bc.utils.read_data('unique_courses.json')
  courses = bc.get_courses_for_subject(subject, unique_courses)
  # bc.utils.save_data(courses, "courses_acct.json")

  ### get all materials for subject
  course_ids = [ c['course_id'] for c in courses ]
  materials = bc.fetch_materials_for_courses(course_ids)
  bc.utils.save_data(materials, f'materials_{subject}.json')
