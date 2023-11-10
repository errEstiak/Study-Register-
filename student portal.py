#########################################################################
# CT60A0203 Introduction to Programming - Online teaching
# Name:
# Student number:
# Email:
# Date:
# By submitting this work, I certify that
#
# • I discussed certain tasks with friends, but I personally wrote the code.
# • Although I used the internet to search for solutions (e.g., Stack Exchange,
#   GeeksforGeeks, and Programiz), I wrote the code independently.
# • I asked ChatGPT and used the answer as a reference, but I wrote the code by myself.
#
#########################################################################






import datetime
import random
import re


# i used file handling functions here
def read_file(filePath):
    with open(filePath, 'r') as file:
        return [line.strip() for line in file.readlines()]

def write_file(filePath, data, mode='a'):
    with open(filePath, mode) as file:
        file.write(data + '\n')

# generating & validating previous and current utilities
def validate_name(name):
    return bool(re.match(r'^[A-Z][a-z]*$', name))

def generate_email(firstName, lastName):
    return f"{firstName.lower()}.{lastName.lower()}@lut.fi"

def generate_unique_studentId():
    existing_ids = {line.split(',')[0] for line in read_file('students.txt')}
    while True:
        new_id = str(random.randint(10000, 99999))
        if new_id not in existing_ids:
            return new_id

def validate_date(dateStr):
    try:
        passedDate = datetime.datetime.strptime(dateStr, '%d/%m/%Y')
        if passedDate > datetime.datetime.now():
            print("Input date is later than today. Try again!")
            return False
        if (datetime.datetime.now() - passedDate).days > 30:
            print("Input date is older than 30 days. Contact 'opinto'.")
            return False
        return True
    except ValueError:
        print("Invalid date format. Use DD/MM/YYYY. Try again!")
        return False

def course_exists(courseId):
    courses = read_file('courses.txt')
    return any(course.split(',')[0] == courseId for course in courses)

def student_exists(studentId):
    students = read_file('students.txt')
    return any(student.split(',')[0] == studentId for student in students)

def get_student_info(studentId):
    students = read_file('students.txt')
    for student in students:
        id, firstName, lastName, year, major, email = student.split(',')
        if id == studentId:
            return {'firstName': firstName, 'lastName': lastName, 'year': year, 'major': major, 'email': email}

def get_passed_courses(studentId):
  passed = read_file('passed.txt')
  return [dict(zip(['courseId', 'studentId', 'date', 'grade'], line.split(','))) for line in passed if line.split(',')[1] == studentId]

def get_course_info(courseId):
    courses = read_file('courses.txt')
    for course in courses:
        id, name, credits, *teachers = course.split(',')
        if id == courseId:
            return {'name': name, 'credits': credits, 'teachers': teachers}

# Menu for our system
def display_menu():
    print("You may select one of the following:")
    print("1) Add student\n 2) Search student\n 3) Search course\n 4) Add course completion\n 5) Show student's record\n 0) Exit")
    return input("What is your selection? ")

# adding new student to our system
def addStudent():
    while True:
        firstName = input("Enter the first name of the student: ")
        lastName = input("Enter the last name of the student: ")
        if validate_name(firstName) and validate_name(lastName):
            break
        print("Names should contain only letters and start with capital letters.")

    email = generate_email(firstName, lastName)
    studentId = generate_unique_studentId()
    current_year = datetime.datetime.now().year
    major = input("Select student's major (CE, EE, ET, ME, SE): ")

    student_data = f"{studentId},{firstName},{lastName},{current_year},{major},{email}"
    write_file('students.txt', student_data)
    print("Student added successfully!")

# search previously registered student
def searchStudent():
    while True:
        search_term = input("Give at least 3 characters of the students first or last name: ")
        if len(search_term) >= 3:
            break
        print("The search term must contain at least three non-blank characters.")

    students = read_file('students.txt')
    for student in students:
        studentId, firstName, lastName, _, _, _ = student.split(',')
        if search_term.lower() in firstName.lower() or search_term.lower() in lastName.lower():
            print(f"ID: {studentId}, First name: {firstName}, Last name: {lastName}")

# Search added course in the txt file
def searchCourse():
    while True:
        search_term = input("Give at least 3 characters of the name of the course or the teacher: ")
        if len(search_term) >= 3:
            break
        print("The search term must contain at least three non-blank characters.")

    courses = read_file('courses.txt')
    for course in courses:
        course_data = course.split(',')
        courseId, courseName, _, *teachers = course_data
        if search_term.lower() in courseName.lower() or any(search_term.lower() in teacher.lower() for teacher in teachers):
            print(f"ID: {courseId}, Name: {courseName}, Teacher(s): {', '.join(teachers)}")

# add completed course 
def addCourseCompletion():
    courseId = input("Give the course ID: ")
    studentId = input("Give the student ID: ")

    if not course_exists(courseId) or not student_exists(studentId):
        print("Invalid course ID or student ID.")
        return

    grade = input("Give the grade: ")
    if not grade.isdigit() or not 1 <= int(grade) <= 5:
        print("Grade is not a correct grade.")
        return

    passedDate = input("Enter a date (DD/MM/YYYY): ")
    if not validate_date(passedDate):
        return

    update_course_completion(courseId, studentId, grade, passedDate)

def update_course_completion(courseId, studentId, grade, dateStr):
    passed_courses = read_file('passed.txt')
    new_record = f"{courseId},{studentId},{dateStr},{grade}"
    updated = False

    for i, record in enumerate(passed_courses):
        if record.startswith(f"{courseId},{studentId},"):
            existing_grade = record.split(',')[3]
            if int(grade) > int(existing_grade):
                passed_courses[i] = new_record
                updated = True
            else:
                print("Student has passed this course earlier with a higher or equal grade.")
            break

    if not updated:
        passed_courses.append(new_record)

    write_file('passed.txt', '\n'.join(passed_courses), mode='w')
    print("Record added!" if not updated else "Record updated!")

# display student record
def showStudentRecord():
  studentId = input("Enter the student ID: ")
  student_info = get_student_info(studentId)

  if student_info:
      print(f"Student ID: {studentId}")
      print(f"Name: {student_info['lastName']}, {student_info['firstName']}")
      print(f"Starting year: {student_info['year']}")
      print(f"Major: {student_info['major']}")
      print(f"Email: {student_info['email']}")

      passed_courses = get_passed_courses(studentId)
      if passed_courses:
          print("Passed courses:")
          total_credits, total_grade = 0, 0
          for course in passed_courses:
              course_info = get_course_info(course['courseId'])
              if course_info:  # Check if course info is not None
                  print(f"Course ID: {course['courseId']}, Name: {course_info['name']}, Credits: {course_info['credits']}")
                  print(f"Date: {course['date']}, Teacher(s): {', '.join(course_info['teachers'])}, grade: {course['grade']}")
                  total_credits += int(course_info['credits'])
                  total_grade += int(course['grade'])
              else:
                  print(f"Course ID: {course['courseId']} is not found")
          if total_grade:
              average_grade = total_grade / len(passed_courses)
              print(f"Total credits: {total_credits}, average grade: {average_grade:.1f}")
      else:
          print("No passed courses for this student.")
  else:
      print("Invalid student ID or student information not found.")




# Main Program Loop
def main():
    while True:
        choice = display_menu()
        if choice == '0': 
            break
        elif choice == '1': 
            addStudent()
        elif choice == '2':
            searchStudent()
        elif choice == '3':
            searchCourse()
        elif choice == '4':
            addCourseCompletion()
        elif choice == '5':
            showStudentRecord()
        else:
            print("Invalid selection. Please choose a number between 0-5.")

#line if __name__ == "__main__" checks if the script is being run as the main program. If it is, the condition is True, and the code inside the if block is executed.
if __name__ == "__main__":
    main()
