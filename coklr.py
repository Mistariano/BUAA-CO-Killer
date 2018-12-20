from co_killer.compilable import *
from co_killer.task import Task
from co_killer import tester

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
parser.add_argument(dest='output_dir', type=str, metavar='output_dir')

args = parser.parse_args()

if __name__ == '__main__':
    instr_list = MIPS_LITE_WITHOUT_JUMP if args.instr_set == 'lite' \
        else MIPS_C3_SUBSET if args.instr_set == 'c3' \
        else MIPS_C4_SUBSET
    task = Task(repeat_time=args.n, output_dir=args.output_dir, with_exc_handler=(args.instr_set == 'c4'), name='rand')
    if args.template == 'random_k':
        random_k_args = {'k': args.k, 'instr_set': instr_list}
        task.add_template_class(RandomKTemplate, args=random_k_args)
    else:
        raise Exception('Template not found: no template named "{}"'.format(args.template))
    # task.run()
    tester.add(task)
    tester.run()
