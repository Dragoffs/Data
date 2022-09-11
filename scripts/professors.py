import json 
import random
import sys
from scriptlibs.data_commons import *

def make_email(fname, lname) -> str:
    return "{}.{}@rit.edu".format(fname, lname)

def create_professor(fname, lname, courses, email, password) -> dict: 
    professor = {
        "first_name": fname,
        "last_name": lname,
        "courses": courses,
        "email": email,
        "password": password,
        "pinned": []
    }
    return professor

def create_n_professors(n) -> None:
    return_professors = []
    courses = get_courses()
    first_names = get_first_names()
    last_names = get_last_names()
    for i in range(n):
        prof_f_name = first_names[random.randint(0, len(first_names) - 1)]
        prof_l_name = last_names[random.randint(0, len(last_names) - 1)]
        prof_course = courses[random.randint(0, len(courses) - 1)]
        prof_email = make_email(prof_f_name, prof_l_name)
        prof_password = "test"
        professor = create_professor(prof_f_name, prof_l_name, prof_course, prof_email, prof_password)
        return_professors.append(professor)
    with open("../professors/professors.json", "w") as outfile:
        json.dump(return_professors, outfile)

def main():
    args = sys.argv
    if (len(args) < 1 or len(args) > 2):
        print("Usage: python3 professors.py (# of professors to generate)")
        return 1
    if args[1].isnumeric():
        create_n_professors(int(args[1]))
        return 0
    else:
        print("(# of professors to generate) must be a number")
        return 1

if __name__ == "__main__":
    main()