import random
from .instruction import *
from .compilable import *
import os
from co_killer.global_configs import BASE_DIR
from .instr_set import *


class Template(Compilable):
    def __init__(self, compilable_instances: list = None, with_pc_comment=True, pc_gen=None, args: dict = None):
        assert not with_pc_comment or pc_gen is not None
        if not compilable_instances:
            compilable_instances = []
        self.compilable_instances = compilable_instances
        self.with_pc_comment = with_pc_comment
        self.pc_gen = pc_gen

        self.initial_compilable_instances(args)
        self._add_pc_comment_wrapper()

    def _add_pc_comment_wrapper(self):
        if not self.with_pc_comment:
            return
        cmp_list = self.compilable_instances
        wrapper_cls = self._PCCommentWrapper
        pc_gen = self.pc_gen
        self.compilable_instances = [wrapper_cls(cmp, pc_gen) if isinstance(cmp, Instruction) else cmp for cmp in
                                     cmp_list]

    def initial_compilable_instances(self, args: dict):
        pass

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

        class RestartableGen:
            def __init__(self, start):
                self._pc_gen = pc_gen(start)
                self._pc_start = start

            def reset(self):
                self._pc_gen = pc_gen(self._pc_start)

            def __iter__(self):
                return self._pc_gen

            def __next__(self):
                return self._pc_gen.__next__()

        return RestartableGen(pc_start)


class RandomKTemplate(Template):
    """
    Randomly choice args['k'] compilable objects from args['instr_set']
    """

    def __init__(self, compilable_instances=None, with_pc_comment=True, pc_gen=None, args=None):
        super().__init__(compilable_instances=compilable_instances, with_pc_comment=with_pc_comment, pc_gen=pc_gen,
                         args=args)
        self._compilable_set = args['instr_set']
        self._k = args['k']

    def compile(self):
        self.compilable_instances = [random.choice(self._compilable_set) for _ in range(self._k)]
        self._add_pc_comment_wrapper()
        return super().compile()


class TailTemplate(Template):
    def initial_compilable_instances(self, args: dict):
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
        exc_handler_path = os.path.join(BASE_DIR, 'resource/exc_handler.asm')
        with open(exc_handler_path, 'r') as f:
            self._handler_asm = f.read()

    def compile(self):
        return self._handler_asm


class COP0InitTemplate(Template):
    class _MTC0SR(Instruction):
        def __init__(self):
            super().__init__(check_name=False)

        def compile(self):
            return 'mtc0 $0 $12'

    def initial_compilable_instances(self, args: dict):
        instr_list = [
            self._MTC0SR()
        ]
        return instr_list


if __name__ == '__main__':
    print(ExcHandlerTemplate(with_pc_comment=False).compile())
