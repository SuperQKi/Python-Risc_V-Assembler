add t1, t2, t5
lbu t1, -100(t2)
lhu t1, 40(t2)
srai t1, t2, 3
srai t1, t2, 4
sltiu t1, t2, 0x7
sltu t1, t2, t3
addi t1, zero, 7
addi t2, zero, -7
lw t1, 40(t2)
jal t1, loop
lui t1, -12
bne t1, t2, loop
and t2, t0, t1     # t2 = t0 AND t1
or t3, t0, t1      # t3 = t0 OR t1
xor t4, t0, t1     # t4 = t0 XOR t1
loop:
