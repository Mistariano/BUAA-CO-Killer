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
