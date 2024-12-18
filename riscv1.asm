addi t1, zero, 20
addi t2, zero, 200
addi t0, zero, 50

fcvt.s.w ft1, t1
fcvt.s.wu ft2, t2
fcvt.w.s t0, ft3
fcvt.wu.s t2, ft0
fcvt.d.w ft4, t1
fcvt.d.wu ft5, t2
fcvt.w.d t1, ft3
fcvt.wu.d t2, ft0

fmv.x.s t2, ft4
fmv.s.x ft4, t1

feq.s t2, ft1, ft2
flt.s t1, ft2, ft4
fle.s t3, ft3, ft4
fclass.s t3, ft1
feq.d t2, ft1, ft2
flt.d t1, ft2, ft4
fle.d t3, ft3, ft4
fclass.d t3, ft1

fmin.s ft6, ft1, ft2
fmax.s ft7, ft1, ft2
fmin.d ft8, ft1, ft2
fmax.d ft9, ft1, ft2

fsgnj.s ft1, ft2, ft3
fsgnjn.s ft3, ft4, ft5
fsgnjx.s ft4, ft5,ft6
fsgnj.d ft1, ft2, ft3
fsgnjn.d ft3, ft4, ft5
fsgnjx.d ft4, ft5,ft6

fmadd.s ft4, ft5,ft6, ft1
fnmadd.s ft4, ft5,ft6, ft1
fnmsub.s ft5, ft3,ft2, ft1
fmsub.s ft1, ft2,ft6, ft3
fmadd.d ft4, ft5,ft6, ft1
fnmadd.d ft4, ft5,ft6, ft1
fnmsub.d ft5, ft3,ft2, ft1
fmsub.d ft1, ft2,ft6, ft3

fsqrt.s ft1, ft5
fsqrt.d ft3, ft4

fadd.s ft1, ft3, ft4
fsub.s ft6, ft3, ft3
fmul.s ft2, ft4, ft1
fdiv.s ft1, ft3, ft5
fadd.d ft1, ft3, ft4
fsub.d ft6, ft3, ft3
fmul.d ft2, ft4, ft1
fdiv.d ft1, ft3, ft5

lui t1, 0x10010
fsw ft7, 8(t1)
fsd ft7, 12(t1)
flw ft1, 8(t1)
fld ft2, 12(t1) 
