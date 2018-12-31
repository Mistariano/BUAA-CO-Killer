import os

from co_killer.compilable.template import Template
from co_killer.global_configs import BASE_DIR
from .instructions import *


class BranchDelaySlotExcTemplate(Template):
    def get_initial_compilable_instances(self):
        label = Label('branch_delay_slot_exc_test_end')
        seq = [
            LUI(10, '0x7fff'),
            ORI(10, 10, '0xffff'),
            BEQ(0, 0, label),
            ADDI(10, 10, 1),  # Overflow here
            label,
        ]
        return seq


class BuiltinExcHandlerTemplate(Template):

    def __init__(self, with_pc_comment=False, pc_gen=None, args: dict = None):
        super().__init__(with_pc_comment=with_pc_comment, pc_gen=pc_gen, args=args)
        handler = args['handler']
        handler_path = 'resource/exc_handler_p8.asm' if handler == 'p8' else 'resource/exc_handler.asm'
        handler_path = os.path.join(BASE_DIR, handler_path)
        with open(handler_path, 'r') as f:
            self._handler_asm = f.read()

    def compile(self):
        return self._handler_asm


class COP0InitTemplate(Template):
    class _MTC0SR(Instruction):
        def __init__(self):
            super().__init__(check_name=False)

        def compile(self):
            return 'mtc0 $0 $12'

    def get_initial_compilable_instances(self):
        instr_list = [
            self._MTC0SR()
        ]
        return instr_list
