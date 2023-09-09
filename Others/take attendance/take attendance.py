# import datetime
# import time
#
# import pandas as pd
#
# students = ["John", "Jane", "Tom", "Alice"]  # 學生名單
#
# def take_attendance():
#     present_students = []  # 出席學生清單
#     print('================================================')
#     print('If student shows up, enter y, otherwise enter n')
#     print('================================================')
#
#     for student in students:
#         attendance = input("請輸入{}是否出席（是/否）：".format(student))
#         if attendance == "y":
#             present_students.append(student)
#
#     print("出席學生清單：")
#     for student in present_students:
#         print(student)
#
#
#
#     return present_students
#
# present_students = take_attendance()
#
# dates = [datetime.date.today()]*len(present_students)
#
# data = {'Dates': dates, 'Name':present_students}
#
# df = pd.DataFrame(data)
# csv_name = df.to_csv(f'{datetime.date.today()} Attendance.CSV')
#
# print(df)
# print(f'CSV file has been created: {csv_name}')
# print(f'The system will automatically close in 10 sec')
# time.sleep(10)

# demo for multiple sheets in Excel
# import pandas as pd
#
# # Create some example dataframes
# df1 = pd.DataFrame({'A': ['A0', 'A1', 'A2', 'A3'],
#                     'B': ['B0', 'B1', 'B2', 'B3'],
#                     'C': ['C0', 'C1', 'C2', 'C3'],
#                     'D': ['D0', 'D1', 'D2', 'D3']},
#                    index=[0, 1, 2, 3])
#
# df2 = pd.DataFrame({'A': ['A4', 'A5', 'A6', 'A7'],
#                     'B': ['B4', 'B5', 'B6', 'B7'],
#                     'C': ['C4', 'C5', 'C6', 'C7'],
#                     'D': ['D4', 'D5', 'D6', 'D7']},
#                    index=[4, 5, 6, 7])
#
# # Create a Pandas Excel writer using XlsxWriter as the engine.
# with pd.ExcelWriter('pandas_multiple.xlsx', engine='xlsxwriter') as writer:
#     # Write each dataframe to a different worksheet.
#     df1.to_excel(writer, sheet_name='Sheet1')
#     df2.to_excel(writer, sheet_name='Sheet2')

