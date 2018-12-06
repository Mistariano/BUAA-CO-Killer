from utils.placeholder import Placeholder


class Instruction:
    name = 'BASE_INSTRUMENT'

    def __init__(self):
        if self.__class__.__name__.lower() != self.name.lower():
            raise Warning('self.name != class_name:', self.name, self.__class__)

    def compile(self):
        raise NotImplementedError('Should implement Instruction!')

    def __str__(self):
        return self.compile()


class Comment(Instruction):
    name = 'comment'

    def __init__(self, content):
        super().__init__()
        self.content = content

    def compile(self):
        return '# ' + self.content


class Label(Instruction):
    cnt = 0
    name = 'label'

    def __init__(self, prefix: str = None):
        super().__init__()
        if not prefix:
            prefix = ''
        else:
            prefix += '_'
        self._label = prefix + str(Label.cnt)
        Label.cnt += 1

    def get_label(self):
        return self._label

    def compile(self):
        return self._label + ':'


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

    def __init__(self, rs=None, rt=None, offset=None, sl_safe_mode=True, use_smaller_mem=True):
        super().__init__()
        self.rs = Placeholder(rs)
        self.rt = Placeholder(rt)
        self.sl_safe_mode = sl_safe_mode
        if sl_safe_mode:
            assert self.align in [1, 2, 4]
            if self.align == 4:
                self.offset = Placeholder(offset, range=3 if use_smaller_mem else 14, radix='DEC')
            elif self.align == 2:
                self.offset = Placeholder(offset, range=4 if use_smaller_mem else 15, radix='DEC')
            else:
                self.offset = Placeholder(offset, range=5 if use_smaller_mem else 16, radix='DEC')
        else:
            self.offset = Placeholder(offset, range=16, radix='DEC')

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
            return '{} ${} {}({})'.format(self.name, rt, offset, rs)  # it's dangerous when rs is not 0.


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
