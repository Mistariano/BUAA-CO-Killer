from template import *
from instruction import Compilable


class Task(Compilable):
    def __init__(self, with_exc_handler=True, with_pc_comment=True, name=None):
        if not name:
            name = 'Task_' + str(id(self))
        # print('Initializing Task', name, '...')
        self.templates = []
        self._text_pc_gen = get_pc_generator(0x3000) if with_pc_comment else None
        self._ktext_pc_gen = get_pc_generator(0x4180) if with_pc_comment else None

        self._with_pc_comment = with_pc_comment

        if with_exc_handler:
            self.add_template_class(ExcHandlerTemplate, True)

            self.add_template_class(COP0InitTemplate)

        # print('Initialized Task', name, '...')

    def compile(self):
        tail = TailTemplate(with_pc_comment=self._with_pc_comment, pc_gen=self._text_pc_gen)
        return '\n\n'.join([temp.compile() for temp in self.templates + [tail]])

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
