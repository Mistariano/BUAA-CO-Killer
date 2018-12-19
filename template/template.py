import random
from instruction import *


class Template(Compilable):
    def __init__(self, compilable_instances: list = None, with_pc_comment=True, pc_gen=None):
        if not compilable_instances:
            compilable_instances = []
        assert not with_pc_comment or pc_gen is not None
        self.compilable_instances = []
        wrapper_cls = self._PCCommentWrapper
        for cmp in compilable_instances:
            assert isinstance(cmp, Compilable)
            if isinstance(cmp, Instruction) and with_pc_comment:
                cmp = wrapper_cls(cmp, pc_gen)
            self.compilable_instances.append(cmp)

        self.with_pc_comment = with_pc_comment
        self.pc_gen = pc_gen

    def compile(self):
        cmp_list = self.compilable_instances
        return '\n'.join([cmp.compile() for cmp in cmp_list])

    def append(self, compilable: Compilable):
        if self.with_pc_comment and isinstance(compilable, Instruction):
            self.compilable_instances.append(self._PCCommentWrapper(compilable, self.pc_gen))
        else:
            self.compilable_instances.append(compilable)

    class _PCCommentWrapper(Compilable):
        def __init__(self, _instr: Instruction, pc_gen):
            self._comment = Comment(hex(next(pc_gen)))
            self._instr = _instr

        def compile(self):
            return self._comment.compile() + '\n' + self._instr.compile()

    @staticmethod
    def get_pc_generator(pc_start):
        def pc_gen(start):
            cur = start
            while True:
                yield cur
                cur += 4

        return pc_gen(pc_start)


class RandomKTemplate(Template):
    def __init__(self, compilable_set: list, k=100, with_pc_comment=True, pc_gen=None):
        self.compilable_set = compilable_set
        self.k = k
        compilable_instances = \
            [random.choice(self.compilable_set)() for _ in range(self.k)]
        super().__init__(compilable_instances=compilable_instances, with_pc_comment=with_pc_comment, pc_gen=pc_gen)


class TailTemplate(Template):
    def __init__(self, with_pc_comment=True, pc_gen=None):
        label = Label('tail_loop')
        instr_list = [
            label,
            J(label)
        ]
        super().__init__(instr_list, with_pc_comment=with_pc_comment, pc_gen=pc_gen)


class ExcHandlerTemplate(Template):
    class _MTC0SR(Instruction):
        def __init__(self):
            super().__init__(check_name=False)

        def compile(self):
            return 'mtc0 $0 $12'

    def __init__(self, with_pc_comment=True, pc_gen=None):
        mtc0_instr_list = [self._MTC0SR()]
        super().__init__(mtc0_instr_list, with_pc_comment=with_pc_comment, pc_gen=pc_gen)
        with open('resource/exc_handler.asm', 'r') as f:
            self._handler_asm = f.read()

    def compile(self):
        return self._handler_asm + '\n' + super().compile()
