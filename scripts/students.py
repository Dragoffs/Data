import sys
import json
import random
from scriptlibs.data_commons import *

def make_uid() -> int:
    return random.randint(10000000, 99999999)

def make_email(fname, lname) -> str:
    return "{}x{}{}@rit.edu".format(fname[0].lower(), lname[0].lower(), str(random.randint(1000, 9999)))

def create_student(uid, username,fname, lname, courses, email) -> dict: 
    student = {
        "uid": uid,
        "username": username,
        "first_name": fname,
        "last_name": lname,
        "courses": courses,
        "email": email,
    }
    return student

def create_n_students(n) -> None:
    return_students = []
    courses = get_courses()
    first_names = get_first_names()
    last_names = get_last_names()
    for i in range(n):
        uid = make_uid()
        f_name = first_names[random.randint(0, len(first_names) - 1)]
        l_name = last_names[random.randint(0, len(last_names) - 1)]
        course = courses[random.randint(0, len(courses) - 1)]
        email = make_email(f_name, l_name)
        username = email.split("@")[0]
        student = create_student(uid, username, f_name, l_name, course, email)
        return_students.append(student)
    with open("../students/students.json", "w") as outfile:
        json.dump(return_students, outfile)

def main():
    args = sys.argv
    if (len(args) < 2 or len(args) > 2):
        print("Usage: python3 students.py (# of students to generate)")
        return 1
    if args[1].isnumeric():
        create_n_students(int(args[1]))
        return 0
    else:
        print("(# of students to generate must be a number)")
        return 1

if __name__ == "__main__":
    main()