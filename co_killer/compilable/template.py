import random

import co_killer.builtin.instructions as builtin
from . import Instruction, Compilable, Comment, Label


class Template(Compilable):
    def __init__(self, compilable_instances: list = None, with_pc_comment=False, pc_gen=None, args: dict = None):
        assert not with_pc_comment or pc_gen is not None
        if not compilable_instances:
            compilable_instances = []
        self._compilable_instances = compilable_instances
        self._with_pc_comment = with_pc_comment
        self._pc_gen = pc_gen

        self._compilable_instances = self.get_initial_compilable_instances()
        assert self._compilable_instances is not None
        self._add_pc_comment_wrapper()

    def _add_pc_comment_wrapper(self):
        if not self._with_pc_comment:
            return
        cmp_list = []
        wrapper_cls = self._PCCommentWrapper
        pc_gen = self._pc_gen
        with_pc_comment = self._with_pc_comment
        for cmp in self._compilable_instances:
            if isinstance(cmp, Instruction):
                cmp_list.append(wrapper_cls(cmp, pc_gen))
            elif isinstance(cmp, Template):
                cmp.reset_pc_gen(with_pc_comment, pc_gen)
                cmp._add_pc_comment_wrapper()
                cmp_list.append(cmp)
            else:
                cmp_list.append(cmp)
        self._compilable_instances = cmp_list

    def get_initial_compilable_instances(self):
        return self._compilable_instances

    def compile(self):
        cmp_list = self._compilable_instances
        return '\n'.join([cmp.compile() for cmp in cmp_list])

    def reset_pc_gen(self, with_pc_comment, pc_gen):
        self._with_pc_comment = with_pc_comment
        self._pc_gen = pc_gen

    @NotImplementedError
    def append(self, compilable: Compilable):
        pass

    class _PCCommentWrapper(Compilable):
        def __init__(self, instr: Instruction, pc_gen):
            self._pc_gen = pc_gen
            self._instr = instr

        def compile(self):
            return Comment(hex(next(self._pc_gen))).compile() + '\n' + self._instr.compile()


class RandomKTemplate(Template):
    """
    Randomly choice args['k'] compilable objects from args['instr_set']
    """

    def __init__(self, compilable_instances=None, with_pc_comment=False, pc_gen=None, args=None):
        super().__init__(compilable_instances=compilable_instances, with_pc_comment=with_pc_comment, pc_gen=pc_gen,
                         args=args)
        self._compilable_set = args['instr_set']
        self._k = args['k']

    def compile(self):
        self._compilable_instances = [random.choice(self._compilable_set)() for _ in range(self._k)]
        self._add_pc_comment_wrapper()
        return super().compile()


class TailTemplate(Template):
    def get_initial_compilable_instances(self):
        label = Label('tail_loop')
        instr_list = [
            label,
            builtin.J(label),
            builtin.NOP()
        ]
        return instr_list


class ExcHandlerTemplate(Template):
    def __init__(self, compilable_instances: list = None, with_pc_comment=False, pc_gen=None, args: dict = None):
        """
        the exception handler template

        :param compilable_instances: compilable instances
        :param with_pc_comment: whether to add the comment
        :param pc_gen: the generator
        :param args: args['exc_entry'] is needed. default to 0x4180
        """
        super().__init__(compilable_instances, with_pc_comment, pc_gen, args)
        if args is not None and 'exc_entry' in args.keys():
            exc_entry = args['exc_entry']
            assert isinstance(exc_entry, int) or isinstance(exc_entry, str)
            if isinstance(exc_entry, int):
                exc_entry = str(hex(exc_entry))
            else:
                if exc_entry[:2] != '0x':
                    exc_entry = '0x' + exc_entry
            self.exc_entry = exc_entry
        else:
            self.exc_entry = '0x4180'

    def get_initial_compilable_instances(self):
        raise NotImplementedError

    def compile(self):
        return '\n'.join(['.ktext ' + self.exc_entry, super().compile(), '.text:'])


if __name__ == '__main__':
    pass
