import random
from instrument.instrument import *


class Template:
    def __init__(self, instr_instance_list=None, with_pc_comment=True, pc_start=0x3000):
        if instr_instance_list:
            self.instr_instance_list = [instr for instr in instr_instance_list]
        else:
            self.instr_instance_list = []
        self.with_pc_comment = with_pc_comment
        self.pc_start = pc_start

    def compile(self):
        if self.with_pc_comment:
            pc_start = self.pc_start
            instr_cnt = len(self.instr_instance_list)
            comments = [Comment(hex(pc_start + 4 * i)) for i in range(instr_cnt)]
            instr_list = [self.instr_instance_list[i // 2] if i % 2 else comments[i // 2] for i in range(2 * instr_cnt)]
        else:
            instr_list = self.instr_instance_list
        return '\n'.join([instr.compile() for instr in instr_list])


class RandomKTemplate(Template):
    def __init__(self, instr_set: list, k=100, with_pc_comment=True, pc_start=0x3000):
        self.instr_set = instr_set
        self.k = k
        super().__init__(with_pc_comment=with_pc_comment, pc_start=pc_start)

    def compile(self):
        self.instr_instance_list = \
            [random.choice(self.instr_set)() for _ in range(self.k)]
        return super().compile()
