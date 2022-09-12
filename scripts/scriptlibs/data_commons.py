#############################
#     Helper functions      #
#############################
import json

def get_students() -> list: 
    f = open("./students/students.json")
    return_list = []
    data = json.load(f)
    for student in data:
        return_list.append(student)
    return return_list

def get_first_names() -> list:
    return_list = []
    f = open("./data/firstnames.csv")
    for line in f:
        values = line.split(",")
        return_list.append(values[1].replace("\"", ""))
    return return_list[1:]

def get_last_names() -> list:
    return_list = []
    f = open("./data/lastnames.csv")
    for line in f: 
        values = line.split(",")
        return_list.append(values[0].lower().capitalize())
    return return_list[1:]

def get_courses() -> list:
    return_list = []
    with open("../classes/classes.json") as json_file:
        data = json.load(json_file)
        for i in range(len(data)):
            return_list.append(data[i]["class_code"])
    return return_list
