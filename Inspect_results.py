# đọc file kết quả và file test
file_check = open('D:\\Tester\\test.txt', 'r')
content_file_check = [line.strip() for line in file_check]
file_result = open('D:\\python\\RiscV_Assembler\\Machine_code.txt', 'r')
content_file_result = [line.strip() for line in file_result]

# in dữ liệu hai file ra
print(content_file_check, '\n', content_file_result)

# hiện kết quả kiểm tra
if content_file_check == content_file_result:
    print('Similarly!')
else:
    print('Differently!')