import json
import pymongo
import random
import time
import datetime

client = pymongo.MongoClient("mongodb+srv://username:sl2password@dblogs.haqtcfn.mongodb.net/?retryWrites=true&w=majority")
db = client['SL2']

def get_students() -> list: 
    f = open("../students/students.json")
    return_list = []
    data = json.load(f)
    for student in data:
        return_list.append(student)
    return return_list

def insert_students():
    student_list = get_students()
    collection = db['Students']
    for student in student_list:
        print("inserted {}".format(student))
        collection.insert_one(student)

def insert_log(user, date, result):
    result_object = { "datetime": date, "result": result}
    collection = db['Students']
    collection.update_one({'username': user}, {'$push': {'logs': result_object} })
    print('{} was {} {}'.format(user, result ,date))

def main():
    collection = db['Students']
    students_list = list(collection.find({}))
    #Students that are currently logged in.
    logged_students = []
    #Student_id that are permanent failure go in here
    error_students = ["lxm5229", "pxp4868", "mxm1276", "exp7267", "rxh6668"]
    while(True):
        current_date = datetime.datetime.now()
        random_student = students_list[random.randint(0, len(students_list) - 1)]
        student_id = random_student['username']
        #Chooses the action that will be taken
        action = random.randint(1, 3)
        if student_id in error_students:
            insert_log(student_id, current_date, "Failure")
        else:
            if action == 1 and student_id not in logged_students:
                insert_log(student_id, current_date, "Failure")
                print("This is password fail by {}".format(student_id))
            if action == 2 and student_id not in logged_students:
                logged_students.append(student_id)
                insert_log(student_id, current_date, "Success")
                print("This is success login by {}".format(student_id))
            if action == 3 and student_id in logged_students:
                logged_students.remove(student_id)
                insert_log(student_id, current_date, "Disconnect")
                print("This is log out by {}".format(student_id))
        #Creates an interval of random time
        time.sleep(random.randint(50, 100))


if __name__ == "__main__":
    main()