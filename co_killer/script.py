import argparse

from co_killer import tester
from co_killer.builtin.instruction_set import InstructionSetMgr
from co_killer.builtin.templates import BranchDelaySlotExcTemplate
from co_killer.compilable import *
from co_killer.task import ASMGenerateTask

parser = argparse.ArgumentParser()
parser.add_argument('-k', '--k_instr', dest='k', type=int, metavar='k', default=1000,
                    help="generate k random instructions.")
parser.add_argument('-n', '--n_case', dest='n', type=int, metavar='n', default=10,
                    help="the number of generated test cases.")
parser.add_argument('-is', '--instr_set', dest='instr_set', type=str, metavar='set_name', default='c5',
                    choices=['c3', 'c4', 'c5', 'lite'],
                    help="the instruction set on which the test cases will be generated."
                         "Should be 'c3', 'c4', 'c5', or 'lite'.")
parser.add_argument('-t', '--template', dest='template', type=str, metavar='template_name', default='random_k',
                    help="the template to compile, default to 'random_k'")
parser.add_argument(dest='output_dir', type=str, metavar='output_dir')

args = parser.parse_args()


def main():
    instr_list = InstructionSetMgr.get_instr_set_by_name(args.instr_set)
    exc_handler = {'c4': 'p7', 'c5': 'p8'}[args.instr_set] if args.instr_set in ['c4', 'c5'] else None
    task = ASMGenerateTask(repeat_time=args.n, output_dir=args.output_dir, builtin_exc_handler=exc_handler, name='rand')
    if args.template == 'random_k':
        random_k_args = {'k': args.k, 'instr_set': instr_list}
        task.add_template_class(RandomKTemplate, args=random_k_args)
        if args.instr_set == 'c5':
            task.add_template_class(BranchDelaySlotExcTemplate)
    else:
        raise Exception('Template not found: no template named "{}"'.format(args.template))
    tester.add(task)
    tester.run()


if __name__ == '__main__':
    main()
