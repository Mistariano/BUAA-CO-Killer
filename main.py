from template import *
from instruction import MIPS_LITE_WITHOUT_JUMP, MIPS_C3_SUBSET, MIPS_C4_SUBSET
from task import Task
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-k', '--k_instr', dest='k', type=int, metavar='k', default=1000,
                    help="generate k random instructions.")
parser.add_argument('-n', '--n_case', dest='n', type=int, metavar='n', default=10,
                    help="the number of generated test cases.")
parser.add_argument('-is', '--instr_set', dest='instr_set', type=str, metavar='set_name', default='c4',
                    choices=['c3', 'c4', 'lite'],
                    help="the instruction set on which the test cases will be generated."
                         "Should be 'c3', 'c4' or 'lite'.")
parser.add_argument('-t', '--template', dest='template', type=str, metavar='template_name', default='random_k',
                    help="the template to compile, default to 'random_k'")

args = parser.parse_args()

if __name__ == '__main__':
    instr_list = MIPS_LITE_WITHOUT_JUMP if args.instr_set == 'lite' \
        else MIPS_C3_SUBSET if args.instr_set == 'c3' \
        else MIPS_C4_SUBSET
    with open('resource/exc_handler.asm', 'r') as f:
        exc_handler = f.read()
    for i in range(args.n):
        task = Task(with_exc_handler=(args.instr_set == 'c4'))
        if args.template == 'random_k':
            random_k_args = {'k': args.k, 'instr_set': instr_list}
            task.add_template_class(RandomKTemplate, args=random_k_args)
        else:
            raise Exception('Template not found: no template named "{}"'.format(args.template))
        asm = task.compile()
        # print(asm)
        if not os.path.exists('output'):
            os.mkdir('output')
        with open('output/rand{}.asm'.format(i), 'w') as f:
            f.write(asm)
