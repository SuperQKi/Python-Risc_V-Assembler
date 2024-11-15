
from assembly_parser import assemly_parser
from register_table import register_table
from instruction_table import instruction_table

file_in = open('riscv1.asm')
content = []
for line in file_in:
    line = line.strip()
    content.append(line)
parse_instructions = assemly_parser(register_table, instruction_table)
parse_instructions.build_label_table(content)
parse_instructions.first_pass(content)



