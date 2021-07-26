from make_report import make_report

input_report_file = "report.txt"
input_photo_dir = r"C:\Users\Ben Windsor\Pictures\DrongO Event"

year = 2021
upload_dir_name = "20210512DrongOEvent"

report_title = "About a DrongO event"
username = "drongousername"
password = "drongopassword"

make_report(input_report_file, input_photo_dir, year, upload_dir_name, report_title, username, password)
