from setuptools import setup

setup(
    name='co_killer',
    version='0.3',
    packages=['co_killer', 'co_killer.util', 'co_killer.compilable'],
    url='https://github.com/Mistariano/BUAA-CO-Killer',
    license='GPL-3.0',
    author='Alex He',
    author_email='hdl730@163.com',
    description='',
    data_files=[('co_killer/resource', ['co_killer/resource/exc_handler.asm'])]
)
