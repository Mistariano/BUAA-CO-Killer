class Compilable:
    """
    可编译对象基类

    所有子类需要继承并实现其compile方法
    """

    def compile(self) -> str:
        """
        编译字符串并返回

        :return: 对象编译得到的字符串
        """
        raise NotImplementedError('Should implement compile() of a Compilable')


class Comment(Compilable):
    name = 'comment'

    def __init__(self, content):
        super().__init__()
        self.content = content

    def compile(self):
        return '# ' + self.content


class Label(Compilable):
    cnt = 0
    name = 'label'

    def __init__(self, prefix: str = None):
        super().__init__()
        if not prefix:
            prefix = ''
        elif prefix[-1] != '_':
            prefix += '_'
        self._label = prefix + str(Label.cnt)
        Label.cnt += 1

    def get_label(self):
        return self._label

    def compile(self):
        return self._label + ':'


class BlankLine(Compilable):
    name = 'blank_line'

    def compile(self) -> str:
        return '\n'
