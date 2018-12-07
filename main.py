from template.template import RandomKTemplate
from instruction.instr_set import MIPS_LITE_WITHOUT_JUMP, MIPS_C3_WITHOUT_JUMP
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-k', '--k_instr', dest='k', type=int, metavar='k', default=1023,
                    help="generate k random instructions.")
parser.add_argument('-n', '--n_case', dest='n', type=int, metavar='n', default=1,
                    help="the number of generated test cases.")
parser.add_argument('-is', '--instr_set', dest='instr_set', type=str, metavar='set_name', default='lite',
                    choices=['c3', 'lite'],
                    help="the instruction set on which the test cases will be generated. Should be 'c3' or 'lite'.")
parser.add_argument('-t', '--template', dest='template', type=str, metavar='template_name', default='random_k',
                    help="the template to compile, default to 'random_k'")

args = parser.parse_args()

if __name__ == '__main__':
    for i in range(args.n):
        instr_list = MIPS_LITE_WITHOUT_JUMP if args.instr_set == 'lite' else MIPS_C3_WITHOUT_JUMP
        if args.template == 'random_k':
            asm = RandomKTemplate(MIPS_LITE_WITHOUT_JUMP, k=1023).compile()
        else:
            raise Exception('Template not found: no template named "{}"'.format(args.template))
        print(asm)
        if not os.path.exists('output'):
            os.mkdir('output')
        with open('output/rand{}.asm'.format(i), 'w') as f:
            f.write(asm)
