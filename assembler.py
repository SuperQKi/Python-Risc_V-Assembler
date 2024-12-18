
from assembly_parser import assemly_parser
from register_table import register_table
from instruction_table import instruction_table
from floatingPoint_table import floatingPoint_table

try:
    print('Program running...')
    # mở file chưa lệnh cần phân tích
    file_in = open('D:\\Tester\\riscv1.asm', 'r')
    # chuyển dữ liệu trong file sang list
    content = [line.strip() for line in file_in]
    # chuyển lệnh sang mã máy
    parse_instructions = assemly_parser(register_table, instruction_table, floatingPoint_table)
    parse_instructions.build_label_table(content)
    parse_instructions.first_pass(content)

    print('Program finished!')

except Exception as e:
    print(f'Program failed: {e}')



