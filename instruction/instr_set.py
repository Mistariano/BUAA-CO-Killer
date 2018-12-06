from instruction.instruction import *


class NOP(Instruction):
    name = 'nop'

    def compile(self):
        return 'nop'


# 1
class LB(SLFormatInstr):
    align = 1
    name = 'lb'


# 2
class LBU(SLFormatInstr):
    align = 1
    name = 'lbu'


# 3
class LH(SLFormatInstr):
    align = 2
    name = 'lh'


# 4
class LHU(SLFormatInstr):
    align = 2
    name = 'lhu'


# 5
class LW(SLFormatInstr):
    align = 4
    name = 'lw'


# 6
class SB(SLFormatInstr):
    align = 1
    name = 'sb'


# 7
class SH(SLFormatInstr):
    align = 2
    name = 'sh'


# 8
class SW(SLFormatInstr):
    align = 4
    name = 'sw'


# 9
class ADD(RFormatInstr):
    name = 'add'


# 10
class ADDU(RFormatInstr):
    name = 'addu'


# 11
class SUB(RFormatInstr):
    name = 'sub'


# 12
class SUBU(RFormatInstr):
    name = 'subu'


# 13
class MULT(MULTFormatInstr):
    name = 'mult'


# 14
class MULTV(MULTFormatInstr):
    name = 'multv'


# 15
class DIV(MULTFormatInstr):
    name = 'div'


# 16
class DIVU(MULTFormatInstr):
    name = 'divu'


# 17
class SLL(ShiftFormatInstr):
    name = 'sll'


# 18
class SRL(ShiftFormatInstr):
    name = 'srl'


# 19
class SRA(ShiftFormatInstr):
    name = 'sra'


# 20
class SLLV(RFormatInstr):
    name = 'sllv'


# 21
class SRLV(RFormatInstr):
    name = 'srlv'


# 22
class SRAV(RFormatInstr):
    name = 'srav'


# 23
class AND(RFormatInstr):
    name = 'and'


# 24
class OR(RFormatInstr):
    name = 'or'


# 25
class XOR(RFormatInstr):
    name = 'xor'


# 26
class NOR(RFormatInstr):
    name = 'nor'


# 27
class ADDI(IFormatInstr):
    name = 'addi'


# 28
class ADDIU(IUFormatInstr):
    name = 'addiu'


# 29
class ANDI(IHexFormatInstr):
    name = 'andi'


# 30
class ORI(IHexFormatInstr):
    name = 'ori'


# 31
class XORI(IHexFormatInstr):
    name = 'xori'


# 32
class LUI(LUIFormatInstr):
    name = 'lui'


# 33
class SLTI(IFormatInstr):
    name = 'slti'


# 34
class SLTIU(IUFormatInstr):
    name = 'sltiu'


# 35
class SLT(RFormatInstr):
    name = 'slt'


# 36
class SLTU(RFormatInstr):
    name = 'sltu'


# 37...

# 47


MIPS_LITE_WITHOUT_JUMP = [NOP, ADDU, SUBU, ORI, LW, SW]

MIPS_C3_WITHOUT_JUMP = [
    LB, LBU, LH, LHU, LW,  # 1-5
    SB, SH, SW,  # 6-8
    # ADD, SUB # 9, 11
    ADDU, SUBU,  # 10, 12
    SLL, SRL, SRA, SLLV, SRLV, SRAV,  # 17-22
    AND, OR, XOR, NOR,  # 23-26
    # ADDI, 27
    ADDIU, ANDI, ORI, XORI, LUI,  # 28-32
    SLTI, SLTIU, SLT, SLTU
]

if __name__ == '__main__':
    for instr in MIPS_LITE_WITHOUT_JUMP:
        print(instr())
