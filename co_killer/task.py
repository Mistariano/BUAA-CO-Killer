from co_killer.compilable import *
import os


class Task:
    def __init__(self, output_dir, repeat_time=1, with_exc_handler=True, with_pc_comment=True, name=None):
        if not name:
            name = 'Task_' + str(id(self))
        self.name = name
        # print('Initializing Task', name, '...')
        self._repeat_time = repeat_time
        self._output_dir = output_dir
        self.templates = []
        self._text_pc_gen = get_pc_generator(0x3000) if with_pc_comment else None
        self._ktext_pc_gen = get_pc_generator(0x4180) if with_pc_comment else None

        self._with_pc_comment = with_pc_comment

        if with_exc_handler:
            self.add_template_class(ExcHandlerTemplate, True)

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

    def add_template_class(self, template_cls, use_ktext_pc_gen=False, args=None):
        assert issubclass(template_cls, Template)
        pc_gan = self._text_pc_gen if not use_ktext_pc_gen else self._ktext_pc_gen
        try:
            template_instance = template_cls(with_pc_comment=self._with_pc_comment, pc_gen=pc_gan, args=args)
        except TypeError as e:
            print('Current template class:', template_cls)
            raise e

        self.templates.append(template_instance)

    def add_compilable_sequence(self, cmp_seq: list, use_ktext_pc_gen=False):
        with_pc_comments = self._with_pc_comment
        pc_gen = self._with_pc_comment

        class _SeqWrapperTemplate(Template):
            def __init__(self):
                super().__init__(compilable_instances=cmp_seq, with_pc_comment=with_pc_comments, pc_gen=pc_gen)

        self.add_template_class(_SeqWrapperTemplate, use_ktext_pc_gen=use_ktext_pc_gen)

    def add_compilable(self, cmp: Compilable, use_ktext_pc_gen=False):
        self.add_compilable_sequence([cmp], use_ktext_pc_gen)
