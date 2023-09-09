import datetime

import pandas as pd

students = ["John", "Jane", "Tom", "Alice"]  # 學生名單

def take_attendance():
    present_students = []  # 出席學生清單

    for student in students:
        attendance = input("請輸入{}是否出席（是/否）：".format(student))
        if attendance == "y":
            present_students.append(student)

    print("出席學生清單：")
    for student in present_students:
        print(student)

    return present_students

present_students = take_attendance()

dates = [datetime.date.today()]*len(present_students)

data = {'Dates': dates, 'Name':present_students}

df = pd.DataFrame(data)
print(df)