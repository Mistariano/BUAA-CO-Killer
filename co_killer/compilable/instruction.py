from .compilable import Compilable
from .compilable import Label
from ..util import Placeholder


class Instruction(Compilable):
    """
    指令基类，继承时需要指定子类的name属性
    """
    name = 'BASE_INSTRUMENT'

    def __init__(self, check_name=True):
        """
        构造函数

        :param check_name: 是否检查类名与name属性一致性，默认检查
        """

        if check_name and self.__class__.__name__.lower() != self.name.lower():
            raise Warning('self.name != class_name:', self.name, self.__class__)

    def compile(self):
        raise NotImplementedError('Should implement compile() of an Instruction!')


class RFormatInstr(Instruction):
    name = 'DEFAULT_R'

    def __init__(self, rd=None, rs=None, rt=None, is_random=False):
        super().__init__()
        self.rs = Placeholder(is_random, value=rs)
        self.rt = Placeholder(is_random, value=rt)
        self.rd = Placeholder(is_random, value=rd)

    def compile(self):
        rs = self.rs.compile()
        rt = self.rt.compile()
        rd = self.rd.compile()
        return '{} ${} ${} ${}'.format(self.name, rd, rs, rt)


class IFormatInstr(Instruction):
    name = 'DEFAULT_I'

    def __init__(self, rt=None, rs=None, imm=None, is_random=False):
        super().__init__()
        self.rs = Placeholder(is_random, value=rs)
        self.rt = Placeholder(is_random, value=rt)
        self.imm = Placeholder(is_random, value=imm, range=15, radix='DEC')

    def compile(self):
        rs = self.rs.compile()
        rt = self.rt.compile()
        imm = self.imm.compile()
        return '{} ${} ${} {}'.format(self.name, rt, rs, imm)


class IHexFormatInstr(IFormatInstr):
    name = 'DEFAULT_I'

    def __init__(self, rt=None, rs=None, imm=None, is_random=False):
        self.rs = Placeholder(is_random, rs)
        self.rt = Placeholder(is_random, rt)
        self.imm = Placeholder(is_random, value=imm, range=16, radix='HEX')
        super().__init__(rt=self.rt, rs=self.rs, imm=self.imm, is_random=False)


class IUFormatInstr(Instruction):
    name = 'DEFAULT_IU'

    def __init__(self, rt=None, rs=None, imm=None, is_random=False):
        super().__init__()
        self.rs = Placeholder(is_random, rs)
        self.rt = Placeholder(is_random, rt)
        self.imm = Placeholder(is_random, value=imm, range=15, radix='DEC')

    def compile(self):
        rs = self.rs.compile()
        rt = self.rt.compile()
        imm = self.imm.compile()
        imm = -imm - 1 if imm < 0 else imm
        return '{} ${} ${} {}'.format(self.name, rt, rs, imm)


class SLFormatInstr(Instruction):
    """
    Should implement this class with changing the value of align if you want to define lb, sb, lh, sh or something else.
    """
    name = 'DEFAULT_SL'
    align = None

    def __init__(self, rt=None, rs=None, offset=None, aligned_mode=False, safe_mode=False, use_smaller_mem=False,
                 check_name=True, is_random=False):
        super().__init__(check_name=check_name)
        self.rs = Placeholder(is_random, rs)
        self.rt = Placeholder(is_random, rt)
        self.sl_safe_mode = safe_mode
        if aligned_mode:
            assert self.align in [1, 2, 4]
            zeros = (self.align + 1) // 2 - self.align % 2  # 1:0, 2:1, 4:2
            self.offset = Placeholder(is_random, offset, range=5 - zeros if use_smaller_mem else 16 - zeros,
                                      radix='DEC')
        else:
            self.offset = Placeholder(is_random, offset, range=5 if use_smaller_mem else 16, radix='DEC')

    def compile(self):
        rs = self.rs.compile()
        rt = self.rt.compile()
        offset = self.offset.compile()
        if self.sl_safe_mode:
            if offset < 0:
                offset = -offset - 1
            offset *= self.align
            return '{} ${} {}($0)'.format(self.name, rt, offset)
        else:
            return '{} ${} {}(${})'.format(self.name, rt, offset, rs)  # it's dangerous when rs is not 0.


class SafeSLFormatInstr(SLFormatInstr):
    def __init__(self, rt=None, rs=None, offset=None, aligned_mode=True, safe_mode=True, use_smaller_mem=True,
                 check_name=False, is_random=False):
        super().__init__(
            rt=rt,
            rs=rs,
            offset=offset,
            aligned_mode=aligned_mode,
            safe_mode=safe_mode,
            use_smaller_mem=use_smaller_mem,
            check_name=check_name,
            is_random=is_random
        )

    @classmethod
    def get_safe_sl_class(cls, sl_cls):
        align = sl_cls.align
        name = sl_cls.name

        class SafeSLInstrClass(SafeSLFormatInstr):
            pass

        SafeSLInstrClass.align = align
        SafeSLInstrClass.name = name
        return SafeSLInstrClass


class LUIFormatInstr(Instruction):
    name = 'DEFAULT_LUI'

    def __init__(self, rt=None, imm=None, is_random=False):
        super().__init__()
        self.rt = Placeholder(is_random, rt)
        self.imm = Placeholder(is_random, imm, range=16, radix='HEX')

    def compile(self):
        rt = self.rt.compile()
        imm = self.imm.compile()
        return '{} ${} {}'.format(self.name, rt, imm)


class MULTFormatInstr(Instruction):
    name = 'DEFAULT_MULT'

    def __init__(self, rs=None, rt=None, is_random=False):
        super().__init__()
        self.rs = Placeholder(is_random, rs)
        self.rt = Placeholder(is_random, rt)

    def compile(self):
        rs = self.rs.compile()
        rt = self.rt.compile()
        return '{} ${} ${}'.format(self.name, rs, rt)


class ShiftFormatInstr(Instruction):
    name = 'DEFAULT_SLL'

    def __init__(self, rd=None, rt=None, sa=None, is_random=False):
        super().__init__()
        self.rt = Placeholder(is_random, rt)
        self.rd = Placeholder(is_random, rd)
        self.sa = Placeholder(is_random, sa, range=5)

    def compile(self):
        rt = self.rt.compile()
        rd = self.rd.compile()
        sa = self.sa.compile()
        if sa < 0:
            sa = -sa - 1
        return '{} ${} ${} {}'.format(self.name, rd, rt, sa)


class JFormatInstr(Instruction):
    name = 'DEFAULT_J'

    def __init__(self, label: Label):
        super().__init__()
        self.label = label

    def compile(self):
        return '{} {}'.format(self.name, self.label.get_label())


class JRFormatInstr(Instruction):
    name = 'DEFAULT_JR'

    def __init__(self, rs):
        super().__init__()
        self.rs = Placeholder(False, rs)

    def compile(self):
        return '{} ${}'.format(self.name, self.rs.compile())


class LOHIFormatInstr(Instruction):
    name = 'DEFAULT_LOHI'

    def __init__(self, rt=None, is_random=False):
        super().__init__()
        self.rt = Placeholder(is_random, rt)

    def compile(self):
        return '{} ${}'.format(self.name, self.rt.compile())


class BEQFormatInstr(Instruction):
    name = 'DEFAULT_BEQ'

    def __init__(self, rs: int, rt: int, label: Label):
        super().__init__()
        self.rs = Placeholder(False, rs)
        self.rt = Placeholder(False, rt)
        self.label = label

    def compile(self):
        return '{} ${} ${} {}'.format(self.name, self.rs.compile(), self.rt.compile(), self.label.get_label())


class BZeroFormatInstr(Instruction):
    name = 'DEFAULT_B_ZERO'

    def __init__(self, rs: int, label: Label):
        super().__init__()
        self.rs = Placeholder(False, rs)
        self.label = label

    def compile(self):
        return '{} ${} {}'.format(self.name, self.rs.compile(), self.label.get_label())


class CPFormatInstr(Instruction):
    name = 'DEFALUT_CP'

    def __init__(self, rt, rd):
        super().__init__()
        self.rt = Placeholder(False, rt)
        self.rd = Placeholder(False, rd)

    def compile(self):
        return '{} ${} ${}'.format(self.name, self.rt.compile(), self.rd.compile())
