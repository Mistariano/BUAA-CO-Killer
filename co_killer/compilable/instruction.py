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

    def __init__(self, rs=None, rt=None, rd=None):
        super().__init__()
        self.rs = Placeholder(rs)
        self.rt = Placeholder(rt)
        self.rd = Placeholder(rd)

    def compile(self):
        rs = self.rs.compile()
        rt = self.rt.compile()
        rd = self.rd.compile()
        return '{} ${} ${} ${}'.format(self.name, rd, rs, rt)


class IFormatInstr(Instruction):
    name = 'DEFAULT_I'

    def __init__(self, rs=None, rt=None, imm=None):
        super().__init__()
        self.rs = Placeholder(rs)
        self.rt = Placeholder(rt)
        self.imm = Placeholder(imm, range=15, radix='DEC')

    def compile(self):
        rs = self.rs.compile()
        rt = self.rt.compile()
        imm = self.imm.compile()
        return '{} ${} ${} {}'.format(self.name, rt, rs, imm)


class IHexFormatInstr(Instruction):
    name = 'DEFAULT_I'

    def __init__(self, rs=None, rt=None, imm=None):
        super().__init__()
        self.rs = Placeholder(rs)
        self.rt = Placeholder(rt)
        self.imm = Placeholder(imm, range=16, radix='HEX')

    def compile(self):
        rs = self.rs.compile()
        rt = self.rt.compile()
        imm = self.imm.compile()
        return '{} ${} ${} {}'.format(self.name, rt, rs, imm)


class IUFormatInstr(Instruction):
    name = 'DEFAULT_IU'

    def __init__(self, rs=None, rt=None, imm=None):
        super().__init__()
        self.rs = Placeholder(rs)
        self.rt = Placeholder(rt)
        self.imm = Placeholder(imm, range=15, radix='DEC')

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

    def __init__(self, rs=None, rt=None, offset=None, aligned_mode=True, safe_mode=True, use_smaller_mem=True,
                 check_name=True):
        super().__init__(check_name=check_name)
        self.rs = Placeholder(rs)
        self.rt = Placeholder(rt)
        self.sl_safe_mode = safe_mode
        if aligned_mode:
            assert self.align in [1, 2, 4]
            zeros = (self.align + 1) // 2 - self.align % 2  # 1:0, 2:1, 4:2
            self.offset = Placeholder(offset, range=5 - zeros if use_smaller_mem else 16 - zeros, radix='DEC')
        else:
            self.offset = Placeholder(offset, range=5 if use_smaller_mem else 16, radix='DEC')

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


class LUIFormatInstr(Instruction):
    name = 'DEFAULT_LUI'

    def __init__(self, rt=None, imm=None):
        super().__init__()
        self.rt = Placeholder(rt)
        self.imm = Placeholder(imm, range=16, radix='HEX')

    def compile(self):
        rt = self.rt.compile()
        imm = self.imm.compile()
        return '{} ${} {}'.format(self.name, rt, imm)


class MULTFormatInstr(Instruction):
    name = 'DEFAULT_MULT'

    def __init__(self, rs=None, rt=None):
        super().__init__()
        self.rs = Placeholder(rs)
        self.rt = Placeholder(rt)

    def compile(self):
        rs = self.rs.compile()
        rt = self.rt.compile()
        return '{} ${} ${}'.format(self.name, rs, rt)


class ShiftFormatInstr(Instruction):
    name = 'DEFAULT_SLL'

    def __init__(self, rt=None, rd=None, sa=None):
        super().__init__()
        self.rt = Placeholder(rt)
        self.rd = Placeholder(rd)
        self.sa = Placeholder(sa, range=5)

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


class LOHIFormatInstr(Instruction):
    name = 'DEFAULT_LOHI'

    def __init__(self, rt=None):
        super().__init__()
        self.rt = Placeholder(rt)

    def compile(self):
        return '{} ${}'.format(self.name, self.rt.compile())


class BEQFormatInstr(Instruction):
    name = 'DEFAULT_BEQ'

    def __init__(self, rs: int, rt: int, label: Label):
        super().__init__()
        self.rs = rs
        self.rt = rt
        self.label = label

    def compile(self):
        return '{} ${} ${} {}'.format(self.name, self.rs, self.rt, self.label.get_label())


class BZeroFormatInstr(Instruction):
    name = 'DEFAULT_BZero'

    def __init__(self, rs: int, label: Label):
        super().__init__()
        self.rs = rs
        self.label = label

    def compile(self):
        return '{} ${} {}'.format(self.name, self.rs, self.label.get_label())
