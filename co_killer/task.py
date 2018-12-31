# from .compilable import *

import os

from co_killer.builtin.templates import COP0InitTemplate
from .builtin import templates
from .compilable.compilable import Compilable
from .compilable.template import Template, TailTemplate


class Task:
    def __init__(self, name):
        if not name:
            name = 'Task_' + str(id(self))
        self.name = name

    def run(self):
        raise NotImplementedError()


class ASMGenerateTask(Task):
    def __init__(self, output_dir, repeat_time=1, builtin_exc_handler: str = None, with_pc_comment=True, name=None):
        super().__init__(name)
        self._repeat_time = repeat_time
        self._output_dir = output_dir
        self.templates = []
        self._text_pc_gen = self._get_pc_generator(0x3000) if with_pc_comment else None
        self._ktext_pc_gen = self._get_pc_generator(0x4180) if with_pc_comment else None

        self._with_pc_comment = with_pc_comment

        assert builtin_exc_handler in ['p7', 'p8'] or builtin_exc_handler is None
        if builtin_exc_handler is not None:
            self.add_template_class(templates.BuiltinExcHandlerTemplate, True, args={'handler': builtin_exc_handler})
            self.add_template_class(COP0InitTemplate)

        # print('Initialized Task', name, '...')

    def output_asm(self):
        tail = TailTemplate(with_pc_comment=self._with_pc_comment, pc_gen=self._text_pc_gen)
        templates = self.templates + [tail]
        for i in range(self._repeat_time):
            self._text_pc_gen.reset()
            self._ktext_pc_gen.reset()
            output_filename = '{}_repeat{}.asm'.format(self.name, str(i))
            output_path = os.path.join(self._output_dir, output_filename)
            if not os.path.exists(self._output_dir):
                os.mkdir(self._output_dir)
            with open(output_path, 'w') as f:
                asm = '\n\n'.join([temp.compile() for temp in templates])
                f.write(asm)

    def run(self):
        self.output_asm()

    def add_template_class(self, template_cls, use_ktext_pc_gen: bool = False, args: dict = None) -> None:
        """
        Add a template class into the task

        :param template_cls: the template class, NOT AN INSTANCE
        :param use_ktext_pc_gen: whether to use the ktext's pc counter instead of text
        :param args: arguments
        """
        assert issubclass(template_cls, Template)
        pc_gan = self._text_pc_gen if not use_ktext_pc_gen else self._ktext_pc_gen
        try:
            template_instance = template_cls(with_pc_comment=self._with_pc_comment, pc_gen=pc_gan, args=args)
        except TypeError as e:
            print('Current template class:', template_cls)
            raise e

        self.templates.append(template_instance)

    def add_handler_template_class(self, template_cls, args: dict = None) -> None:
        """
        Add a handler template class into the task
        :param template_cls: the template class, NOT AN INSTANCE
        :param args: arguments
        """
        self.add_template_class(template_cls=template_cls, use_ktext_pc_gen=True, args=args)

    def add_compilable_sequence(self, cmp_seq: list, use_ktext_pc_gen=False):
        with_pc_comments = self._with_pc_comment
        pc_gen = self._with_pc_comment

        class _SeqWrapperTemplate(Template):
            def __init__(self):
                super().__init__(compilable_instances=cmp_seq, with_pc_comment=with_pc_comments, pc_gen=pc_gen)

        self.add_template_class(_SeqWrapperTemplate, use_ktext_pc_gen=use_ktext_pc_gen)

    def add_compilable(self, cmp: Compilable, use_ktext_pc_gen=False):
        self.add_compilable_sequence([cmp], use_ktext_pc_gen)

    @staticmethod
    def _get_pc_generator(pc_start):
        def pc_gen(start):
            cur = start
            while True:
                yield cur
                cur += 4

        class RestartableGen:
            def __init__(self, start):
                self._pc_gen = pc_gen(start)
                self._pc_start = start

            def reset(self):
                self._pc_gen = pc_gen(self._pc_start)

            def __iter__(self):
                return self._pc_gen

            def __next__(self):
                return self._pc_gen.__next__()

        return RestartableGen(pc_start)
