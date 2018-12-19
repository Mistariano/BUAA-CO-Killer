import random
from instruction import *


class Template(Instruction):
    def __init__(self, instr_instance_list: list = None, with_pc_comment=True, pc_start=0x3000):
        super().__init__(False)
        if instr_instance_list:
            self.instr_instance_list = [instr for instr in instr_instance_list]
        else:
            self.instr_instance_list = []
        pc_cnt = 0
        for instr in self.instr_instance_list:
            assert isinstance(instr, Instruction)
            pc_cnt += instr.get_pc_cnt()
        self.with_pc_comment = with_pc_comment
        self.pc_start = pc_start
        self._pc_cnt = pc_cnt

    def compile(self):
        if self.with_pc_comment:
            pc_start = self.pc_start
            instr_cnt = len(self.instr_instance_list)
            comments = [Comment(hex(pc_start + 4 * i)) for i in range(instr_cnt)]
            instr_list = [self.instr_instance_list[i // 2] if i % 2 else comments[i // 2] for i in range(2 * instr_cnt)]
        else:
            instr_list = self.instr_instance_list
        return '\n'.join([instr.compile() for instr in instr_list])

    def get_pc_cnt(self):
        return self._pc_cnt

    class PCCommentWrapper(Instruction):
        def __index__(self, instr: Instruction, pc_gen):
            super().__init__(check_name=False)
            self._comment = Comment(hex(pc_gen.__next__()))
            self._instr = instr

        def compile(self):
            return self._instr.compile() + '\n' + self._comment.compile()


class RandomKTemplate(Template):
    def __init__(self, instr_set: list, k=100, with_pc_comment=True, pc_start=0x3000):
        self.instr_set = instr_set
        self.k = k
        super().__init__(with_pc_comment=with_pc_comment, pc_start=pc_start)

    def compile(self):
        self.instr_instance_list = \
            [random.choice(self.instr_set)() for _ in range(self.k)]
        return super().compile()


class TailTemplate(Template):
    def __init__(self):
        label = Label('tail_loop')
        instr_list = [
            label,
            J(label)
        ]
        super().__init__(instr_list, False)
