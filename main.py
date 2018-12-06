from template.template import RandomKTemplate
from instruction.instr_set import MIPS_LITE_WITHOUT_JUMP, MIPS_C3_WITHOUT_JUMP
import os

if __name__ == '__main__':
    for i in range(100):
        # P5
        # asm = RandomKTemplate(MIPS_LITE_WITHOUT_JUMP, k=1023).compile()
        # P6
        asm = RandomKTemplate(MIPS_C3_WITHOUT_JUMP, k=1023).compile()
        print(asm)
        if not os.path.exists('output'):
            os.mkdir('output')
        with open('output/rand{}.asm'.format(i), 'w') as f:
            f.write(asm)
