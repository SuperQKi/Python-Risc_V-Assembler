
##############################
##############################
class assemly_parser:
    # word size
    word_size = 0
    # vị trí hiện tại trong bộ nhớ
    current_location = 0
    # danh sách label và địa chỉ nhớ của nó
    symbol_table = {}
    # list register
    register_table = {}
    # list floating ponit
    floatingPoint_table = {}
    # tập lệnh
    instruction_table = {}
    # output file truyền vào
    output_array = []
    #khởi tạo lớp
    def __init__(self, register_table, instruction_table, floatingPoint_table):
        self.register_table = register_table
        self.instruction_table = instruction_table
        self.floatingPoint_table = floatingPoint_table
        self.word_size = 4
        self.current_location = 64

    # danh sách label và địa chỉ nhớ của nó
    def build_label_table(self, lines):
        for line in lines:
            if ':' in line:
                label = line[0:line.find(':')]
                self.symbol_table[label] = self.current_location
            self.current_location += self.word_size

    def first_pass(self, lines):
        self.current_location = 64
        for line in lines:
            # xóa khoảng trắng thừa
            line = line.strip()
            # Làm sạch chuỗi ( cmt, whitespace, etc)
            if '#' in line:
                line = line[0:line.find('#')].strip()

            if len(line) == 0:
                continue

            # sử lý label
            if ':' in line:
                label = line[0:line.find(':')]
                line = line[line.find(':')+1:].strip()

            instruction = line[0: line.find(' ')]
            args = line[line.find(' ')+1:].replace(' ', '').split(',')

            #Phan tich lenh thanh ma may
            if instruction in self.instruction_table.keys():
                self.parse_instruction(instruction, args)
            # tăng địa chỉ để thực hiện câu lệnh tiếp theo
            self.current_location += self.word_size
        # in ra mã máy của tập lệnh
        self.print_marchien_code_map()
    def parse_instruction(self, instruction, raw_arg):
        # lấy core instruction format của lệnh
        field_machine_code = self.instruction_table[instruction]
        args = raw_arg[:]

        ######### Floating point ints ##############

        if 'f' in instruction:

            # lấy offset của lệnh
            if instruction == 'flw' or instruction == 'fld' or instruction == 'fsw' or instruction == 'fsd':
                offset = int(args[1][0:args[1].find('(')])
                args[1] = args[1][args[1].find('(') + 1: args[1].find(')')]
                # chuyển offset sang binary
                if offset < 0:
                    offset = bin((1 << 12) + offset)[2:]
                else:
                    offset = bin(offset)[2:].zfill(12)
                    # đổi giá trị thanh ghi sang mã máy
                    rd = bin(self.floatingPoint_table[args[0]])[2:].zfill(5)
                    rs1 = bin(self.register_table[args[1]])[2:].zfill(5)
                # phân tích các lệnh load và store
                if 's' in instruction:
                    field_machine_code[2] = rs1
                    field_machine_code[1] = rd
                    field_machine_code[0] = offset[0:7]
                    field_machine_code[4] = offset[7:]
                else:
                    field_machine_code[3] = rd
                    field_machine_code[1] = rs1
                    field_machine_code[0] = offset

            elif instruction == 'fcvt.s.w' or instruction == 'fcvt.s.wu' or instruction == 'fcvt.d.w' or instruction == 'fcvt.d.wu':
                # gán giá trị cho rs1
                field_machine_code[2] = bin(self.register_table[args[1]])[2:].zfill(5)
                # gán giá trị chp rd
                field_machine_code[4] = bin(self.floatingPoint_table[args[0]])[2:].zfill(5)

            elif instruction == 'fcvt.wu.s' or instruction == 'fcvt.w.s' or instruction == 'fcvt.wu.d' or instruction == 'fcvt.w.d': 
                # gán giá trị cho rs1
                field_machine_code[2] = bin(self.floatingPoint_table[args[1]])[2:].zfill(5)
                # gán giá trị chp rd
                field_machine_code[4] = bin(self.register_table[args[0]])[2:].zfill(5)

            elif instruction == 'fmv.s.x':
                # gán giá trị cho rs1
                field_machine_code[2] = bin(self.register_table[args[1]])[2:].zfill(5)
                # gán giá trị chp rd
                field_machine_code[4] = bin(self.floatingPoint_table[args[0]])[2:].zfill(5)
            
            elif instruction == 'fmv.x.s':
                # gán giá trị cho rs1
                field_machine_code[2] = bin(self.floatingPoint_table[args[1]])[2:].zfill(5)
                # gán giá trị chp rd
                field_machine_code[4] = bin(self.register_table[args[0]])[2:].zfill(5)
                
            elif instruction == 'feq.s' or instruction == 'fle.s' or instruction == 'flt.s':
                # gán giá trị cho rs2
                field_machine_code[1] = bin(self.floatingPoint_table[args[2]])[2:].zfill(5)
                # gán giá trị cho rs1
                field_machine_code[2] = bin(self.floatingPoint_table[args[1]])[2:].zfill(5)
                # gán giá trị chp rd
                field_machine_code[4] = bin(self.register_table[args[0]])[2:].zfill(5)

            elif instruction == 'feq.d' or instruction == 'fle.d' or instruction == 'flt.d':
                # gán giá trị cho rs2
                field_machine_code[1] = bin(self.floatingPoint_table[args[2]])[2:].zfill(5)
                # gán giá trị cho rs1
                field_machine_code[2] = bin(self.floatingPoint_table[args[1]])[2:].zfill(5)
                # gán giá trị chp rd
                field_machine_code[4] = bin(self.register_table[args[0]])[2:].zfill(5)

            elif instruction == 'fclass.s' or instruction == 'fclass.d':
                # gán giá trị cho rs1
                field_machine_code[2] = bin(self.floatingPoint_table[args[1]])[2:].zfill(5)
                # gán giá trị chp rd
                field_machine_code[4] = bin(self.register_table[args[0]])[2:].zfill(5)

            elif instruction == 'fmin.s' or instruction == 'fmax.s' or instruction == 'fmin.d' or instruction == 'fmax.d':
                # gán giá trị cho rs2
                field_machine_code[1] = bin(self.floatingPoint_table[args[2]])[2:].zfill(5)
                # gán giá trị cho rs1
                field_machine_code[2] = bin(self.floatingPoint_table[args[1]])[2:].zfill(5)
                # gán giá trị chp rd
                field_machine_code[4] = bin(self.floatingPoint_table[args[0]])[2:].zfill(5)

            elif instruction == 'fsgnj.s' or instruction == 'fsgnjn.s' or instruction == 'fsgnjx.s':
                # gán giá trị cho rs2
                field_machine_code[1] = bin(self.floatingPoint_table[args[2]])[2:].zfill(5)
                # gán giá trị cho rs1
                field_machine_code[2] = bin(self.floatingPoint_table[args[1]])[2:].zfill(5)
                # gán giá trị chp rd
                field_machine_code[4] = bin(self.floatingPoint_table[args[0]])[2:].zfill(5)

            elif instruction == 'fsgnj.d' or instruction == 'fsgnjn.d' or instruction == 'fsgnjx.d':
                # gán giá trị cho rs2
                field_machine_code[1] = bin(self.floatingPoint_table[args[2]])[2:].zfill(5)
                # gán giá trị cho rs1
                field_machine_code[2] = bin(self.floatingPoint_table[args[1]])[2:].zfill(5)
                # gán giá trị chp rd
                field_machine_code[4] = bin(self.floatingPoint_table[args[0]])[2:].zfill(5)

            elif instruction == 'fmadd.s' or instruction == 'fnmadd.s' or instruction == 'fmsub.s' or instruction == 'fnmsub.s':
                # gán giá trị cho rs3
                field_machine_code[0] = bin(self.floatingPoint_table[args[3]])[2:].zfill(5)
                # gán giá trị cho rs2
                field_machine_code[2] = bin(self.floatingPoint_table[args[2]])[2:].zfill(5)
                # gán giá trị cho rs1
                field_machine_code[3] = bin(self.floatingPoint_table[args[1]])[2:].zfill(5)
                # gán giá trị chp rd
                field_machine_code[5] = bin(self.floatingPoint_table[args[0]])[2:].zfill(5)

            elif instruction == 'fmadd.d' or instruction == 'fnmadd.d' or instruction == 'fmsub.d' or instruction == 'fnmsub.d':
                # gán giá trị cho rs3
                field_machine_code[0] = bin(self.floatingPoint_table[args[3]])[2:].zfill(5)
                # gán giá trị cho rs2
                field_machine_code[2] = bin(self.floatingPoint_table[args[2]])[2:].zfill(5)
                # gán giá trị cho rs1
                field_machine_code[3] = bin(self.floatingPoint_table[args[1]])[2:].zfill(5)
                # gán giá trị chp rd
                field_machine_code[5] = bin(self.floatingPoint_table[args[0]])[2:].zfill(5)

            elif instruction == 'fsqrt.s' or instruction == 'fsqrt.d':
                # gán giá trị cho rs1
                field_machine_code[2] = bin(self.floatingPoint_table[args[1]])[2:].zfill(5)
                # gán giá trị chp rd
                field_machine_code[4] = bin(self.floatingPoint_table[args[0]])[2:].zfill(5)

            elif instruction == 'fadd.s' or instruction == 'fsub.s' or instruction == 'fmul.s' or instruction == 'fdiv.s':
                # gán giá trị cho rs2
                field_machine_code[1] = bin(self.floatingPoint_table[args[2]])[2:].zfill(5)
                # gán giá trị cho rs1
                field_machine_code[2] = bin(self.floatingPoint_table[args[1]])[2:].zfill(5)
                # gán giá trị chp rd
                field_machine_code[4] = bin(self.floatingPoint_table[args[0]])[2:].zfill(5)

            elif instruction == 'fadd.d' or instruction == 'fsub.d' or instruction == 'fmul.d' or instruction == 'fdiv.d':
                # gán giá trị cho rs2
                field_machine_code[1] = bin(self.floatingPoint_table[args[2]])[2:].zfill(5)
                # gán giá trị cho rs1
                field_machine_code[2] = bin(self.floatingPoint_table[args[1]])[2:].zfill(5)
                # gán giá trị chp rd
                field_machine_code[4] = bin(self.floatingPoint_table[args[0]])[2:].zfill(5)


            # chuyển lệnh sang mã máy   
            machine_code = self.calculator_machine_code(field_machine_code)
            self.output_array.append(machine_code)

        # lấy offset của lệnh
        elif '(' in args[1]:
            offset = int(args[1][0:args[1].find('(')])
            args[1] = args[1][args[1].find('(') + 1: args[1].find(')')]
            # chuyển offset sang binary
            if offset < 0:
                offset = bin((1 << 12) + offset)[2:]
            else:
                offset = bin(offset)[2:].zfill(12)
            # đổi thanh ghi sang mã máy
            register_1 = bin(self.register_table[args[0]])[2:].zfill(5)
            register_2 = bin(self.register_table[args[1]])[2:].zfill(5)
            # phân tích các lệnh load và store
            if 's' in instruction:
                field_machine_code[2] = register_2
                field_machine_code[1] = register_1
                field_machine_code[0] = offset[0:7]
                field_machine_code[4] = offset[7:]
                machine_code = self.calculator_machine_code(field_machine_code)
                self.output_array.append(machine_code)
            else:
                field_machine_code[3] = register_1
                field_machine_code[1] = register_2
                field_machine_code[0] = offset
                # tính mã máy của lệnh
                machine_code = self.calculator_machine_code(field_machine_code)
                # đẩy mã máy vào danh sách mã máy của tập lệnh
                self.output_array.append(machine_code)

        # phân tích lệnh U-type và J-type
        elif args[1] not in self.register_table.keys():
            if 'j' in instruction:
                # phân tích imm nếu imm là một lable
                if args[1] in self.symbol_table.keys():
                    imm = self.symbol_table[args[1]] - self.current_location
                    if imm < 0:
                        imm = bin((1 << 21) + imm)[2:]
                    else:
                        imm = bin(imm)[2:].zfill(21)

                # gán imm vào core instruction format
                field_machine_code[0] = imm[0] + imm[10:20] + imm[9] + imm[1:9]
            else:
                # phân tích imm nếu imm là số hex
                if 'x' in args[1]:
                    imm = args[1][args[1].find('x') + 1:]
                    imm = bin(int(imm, 16))[2:].zfill(20)
                # phân tích imm nếu imm là số dec
                else:
                    if int(args[1]) < 0:
                        imm = bin((1 << 20) + int(args[1]))[2:].zfill(20)
                    else:
                        imm = bin(int(args[1]))[2:].zfill(20)
                # gán imm vào core instruction format
                field_machine_code[0] = imm
            # gán giá trị vào core instruction format còn lại
            field_machine_code[1] = bin(self.register_table[args[0]])[2:].zfill(5)
            # chuyển lệnh sang mã máy
            machine_code = self.calculator_machine_code(field_machine_code)
            self.output_array.append(machine_code)
        # phân tích B-type
        elif args[2] in self.symbol_table.keys():
            offset = self.symbol_table[args[2]] - self.current_location
            if offset < 0:
                offset = bin((1 << 13) + offset)[2:]
            else:
                offset = bin(offset)[2:].zfill(13)

            # chuyển thanh ghi sang số nhị phân
            register_1 = bin(self.register_table[args[0]])[2:].zfill(5)
            register_2 = bin(self.register_table[args[1]])[2:].zfill(5)
            # gán giá trị vào core instruction forma
            field_machine_code[0] = offset[0] + offset[2:8]
            field_machine_code[1] = register_2
            field_machine_code[2] = register_1
            field_machine_code[4] = offset[8:12] + offset[1]

            # tính mã máy của lệnh
            machine_code = self.calculator_machine_code(field_machine_code)
            # đẩy mã máy vào danh sách mã máy của tập lệnh
            self.output_array.append(machine_code)

        # R-type
        elif 'i' not in instruction:
            # gán giá trị vào core instruction format
            field_machine_code[1] = bin(self.register_table[args[2]])[2:].zfill(5)
            field_machine_code[2] = bin(self.register_table[args[1]])[2:].zfill(5)
            field_machine_code[4] = bin(self.register_table[args[0]])[2:].zfill(5)
            # tính mã máy của lệnh
            machine_code = self.calculator_machine_code(field_machine_code)
            self.output_array.append(machine_code)
        # I-type
        else:
            # trường hợp imm là số hex
            if 'x' in args[2]:
                imm = args[2][args[2].find('x') + 1:]
                imm = bin(int(imm, 16))[2:].zfill(12)
            # phân tích imm là decimal
            else:
                if int(args[2]) < 0:
                    imm = bin((1 << 12) + int(args[2]))[2:]
                else:
                    imm = bin(int(args[2]))[2:].zfill(12)
            # sử lí các lệnh có imm đặt biệt của i type.
            if instruction == 'slli' or instruction == 'srli' or instruction == 'srai':
                if instruction == 'srai':
                    imm = '0100000' + imm[7:]
                else:
                    imm = '0000000' + imm[7:]
            # gán giá trị vào core instruction format
            field_machine_code[0] = imm
            field_machine_code[1] = bin(self.register_table[args[1]])[2:].zfill(5)
            field_machine_code[3] = bin(self.register_table[args[0]])[2:].zfill(5)
            # đổi lệnh sang mã máy
            machine_code = self.calculator_machine_code(field_machine_code)
            self.output_array.append(machine_code)

    def calculator_machine_code(self, lst):
        machine_code = ''
        for i in lst:
            machine_code += i
        return machine_code

    def print_marchien_code_map(self):
        # in ra mã máy của tập lệnh
        file_out = open('D:\\python\\RiscV_Assembler\\Machine_code.txt', 'w')
        #file_out.write('Machine Code Map\n')
        for x in self.output_array:
            file_out.write(f'{x}\n')v
