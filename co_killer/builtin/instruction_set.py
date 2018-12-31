from .instructions import *


class InstructionSetMgr:
    _XALU_INSTRUCTIONS = [
        MULT, MULTU,  # 13,14
        MFHI, MFLO, MTHI, MTLO,  # 47-50
    ]

    _50_INSTRUCTIONS_WITHOUT_XALU = [
                                        # LB, LBU, LH, LHU, LW,  # 1-5
                                        # SB, SH, SW,  # 6-8
        # ADD, SUB # 9, 11
        ADDU, SUBU,  # 10, 12
        # MULT, MULTU, DIV, DIVU,  # 13,14,15,16
        SLL, SRL, SRA, SLLV, SRLV, SRAV,  # 17-22
        AND, OR, XOR, NOR,  # 23-26
        # ADDI, 27
        ADDIU, ANDI, ORI, XORI, LUI,  # 28-32
        SLTI, SLTIU, SLT, SLTU,  # 33-36
                                    ] + safe_sl_classes

    _EXCEPTION_INSTRUCTIONS = [
        ADD, SUB,  # 9, 11
        ADDI,  # 27
        SHNotAligned, SWNotAligned,
        LHNotAligned, LWNotAligned,
        # BranchDelaySlotExcTemplate,
    ]

    _MIPS_LITE_SUBSET = [NOP, ADDU, SUBU, ORI, LW, SW]

    _MIPS_C3_SUBSET = _50_INSTRUCTIONS_WITHOUT_XALU + _XALU_INSTRUCTIONS

    _MIPS_C4_SUBSET = _MIPS_C3_SUBSET + _EXCEPTION_INSTRUCTIONS

    _MIPS_C5_SUBSET = _50_INSTRUCTIONS_WITHOUT_XALU + _EXCEPTION_INSTRUCTIONS

    @classmethod
    def _get_loaded_instr_set(cls, instr_set):
        return [_instr() for _instr in instr_set]

    @classmethod
    def get_lite(cls):
        return cls._MIPS_LITE_SUBSET

    @classmethod
    def get_c3(cls):
        return cls._MIPS_C3_SUBSET

    @classmethod
    def get_c4(cls):
        return cls._MIPS_C4_SUBSET

    @classmethod
    def get_c5(cls):
        return cls._MIPS_C5_SUBSET

    @classmethod
    def get_instr_set_by_name(cls, instr_set_name):
        if instr_set_name == 'lite':
            return cls.get_lite()
        elif instr_set_name == 'c3':
            return cls.get_c3()
        elif instr_set_name == 'c4':
            return cls.get_c4()
        elif instr_set_name == 'c5':
            return cls.get_c5()
