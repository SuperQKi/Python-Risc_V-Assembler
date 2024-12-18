
from assembly_parser import assemly_parser
from register_table import register_table
from instruction_table import instruction_table
from floatingPoint_table import floatingPoint_table

# mở file chưa lệnh cần phân tích
file_in = open('D:\\Tester\\riscv1.asm', 'r')
content = []
# chuyển dữ liệu trong file sang list
for line in file_in:
    line = line.strip()
    content.append(line)
# chuyển lệnh sang mã máy
parse_instructions = assemly_parser(register_table, instruction_table, floatingPoint_table)
parse_instructions.build_label_table(content)
parse_instructions.first_pass(content)



