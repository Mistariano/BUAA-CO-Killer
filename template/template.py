import random
from instruction import *


class Template(Compilable):
    def __init__(self, compilable_instances: list = None, with_pc_comment=True, pc_gen=None, args: dict = None):
        assert not with_pc_comment or pc_gen is not None
        compilable_instances = self.initial_compilable_instances(compilable_instances, args)
        self.compilable_instances = []
        wrapper_cls = self._PCCommentWrapper
        for cmp in compilable_instances:
            assert isinstance(cmp, Compilable)
            if isinstance(cmp, Instruction) and with_pc_comment:
                cmp = wrapper_cls(cmp, pc_gen)
            self.compilable_instances.append(cmp)

        self.with_pc_comment = with_pc_comment
        self.pc_gen = pc_gen

    def initial_compilable_instances(self, compilable_instances, args: dict) -> list:
        if not compilable_instances:
            compilable_instances = []
        return compilable_instances

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
    def initial_compilable_instances(self, compilable_instances, args):
        compilable_set = args['instr_set']
        k = args['k']
        compilable_instances = [random.choice(compilable_set)() for _ in range(k)]
        return compilable_instances


class TailTemplate(Template):
    def initial_compilable_instances(self, compilable_instances, args: dict):
        label = Label('tail_loop')
        instr_list = [
            label,
            J(label),
            NOP()
        ]
        return instr_list


class ExcHandlerTemplate(Template):

    def __init__(self, with_pc_comment=True, pc_gen=None, args=None):
        super().__init__(with_pc_comment=with_pc_comment, pc_gen=pc_gen, args=args)
        with open('resource/exc_handler.asm', 'r') as f:
            self._handler_asm = f.read()

    def compile(self):
        return self._handler_asm


class COP0InitTemplate(Template):
    class _MTC0SR(Instruction):
        def __init__(self):
            super().__init__(check_name=False)

        def compile(self):
            return 'mtc0 $0 $12'

    def initial_compilable_instances(self, compilable_instances, args: dict):
        instr_list = [
            self._MTC0SR()
        ]
        return instr_list
