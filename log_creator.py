
import random 
import json
import time
import datetime

def get_students() -> list: 
    f = open("./students/students.json")
    return_list = []
    data = json.load(f)
    for student in data:
        return_list.append(student)
    return return_list

def create_password_fail(date, username, ip, f) -> None:
    taskid = random.randint(500, 3000)
    port = random.randint(50000, 70000)
    message = "{} solace sshd[{}]: Failed password for {} from {} port {} ssh2".format(date, taskid, username, ip, port)
    print(message)
    f.write(message + "\n")
    reset = "{} solace sshd[{}]: Connection reset by authenticating user {} {} port {}[preauth]".format(date, taskid, username, ip, port)
    print(reset)
    f.write(reset + "\n")
    auth_failure = "{} solace sshd[{}]: pam_unix(sshd:auth): authentication failure; logname = uid=0 euid=0 tty=ssh ruser= rhost={} user=root".format(date, taskid, ip)
    print(auth_failure)
    f.write(auth_failure + "\n")

def create_sucessful_login(date, username, ip, f) -> None:
    taskid = random.randint(500, 3000)
    port = random.randint(50000, 70000)
    sessionid = random.randint(1000, 3000)
    message = "{} solace sshd[{}]: Accepted password for {} from {} port {} ssh2".format(date, taskid, username, ip, port)
    print(message)
    f.write(message + "\n")
    session = "{} solace sshd[{}]: pam_unix(sshd:session): session opened for user {}(uid={}) by (uid={})".format(date, taskid, username, sessionid, sessionid)
    print(session)
    f.write(session + "\n")

def create_disconnect(date, username, ip, f) -> None:
    taskid = random.randint(500, 3000)
    port = random.randint(50000, 70000)
    sessionid = random.randint(1000, 3000)
    first_message = "{} solace sshd[{}]: Received disconnect from {} port {} disconnected by user".format(date, taskid, username, port)
    second_message = "{} solace sshd[{}]: Disconnected from user {} {} port {}".format(date, taskid, username, ip, port)
    third_message = "{} solace sshd[{}]: pam_unix(sshd:session): session closed for user {}".format(date, taskid, username)
    print(first_message)
    f.write(first_message + "\n")
    print(second_message)
    f.write(second_message + "\n")
    print(third_message)
    f.write(third_message + "\n")


def main() -> None:
    f = open("dummy_log.log", "w+")
    students_list = get_students()
    logged_students = []
    # n = 0
    while(True):
        current_student = students_list[random.randint(0, len(students_list) - 1)]
        student_id = current_student['username']
        student_ip = current_student['ip']
        current_date = datetime.datetime.now()
        date_format = current_date.strftime("%b %w %H:%M:%S")
        action = random.randint(1, 3)
        if action == 1 and student_id not in logged_students:
            create_password_fail(date_format, student_id, student_ip, f)
            print("This is password fail by {}".format(student_id))
        if action == 2 and student_id not in logged_students:
            logged_students.append(student_id)
            create_sucessful_login(date_format, student_id, student_ip, f)
            print("This is success login by {}".format(student_id))
        if action == 3 and student_id in logged_students:
            logged_students.remove(student_id)
            create_disconnect(date_format, student_id, student_ip, f)
            print("This is log out by {}".format(student_id))
        time.sleep(random.randint(1, 20))
        # n += 1
        
if __name__ == "__main__":
    main()

