from template.template import RandomKTemplate
from instrument.instr_set import MIPS_LITE_WITHOUT_JUMP, MIPS_C3_WITHOUT_JUMP
import os

if __name__ == '__main__':
    # asm = RandomKTemplate(MIPS_LITE_WITHOUT_JUMP, k=1000).compile()
    for i in range(30):
        asm = RandomKTemplate(MIPS_C3_WITHOUT_JUMP, k=1023).compile()
        print(asm)
        if not os.path.exists('output'):
            os.mkdir('output')
        with open('output/rand{}.asm'.format(i), 'w') as f:
            f.write(asm)
