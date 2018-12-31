from setuptools import setup

setup(
    name='co_killer',
    version='0.5',
    packages=['co_killer', 'co_killer.util', 'co_killer.compilable', 'co_killer.builtin'],
    url='https://github.com/Mistariano/BUAA-CO-Killer',
    license='GPL-3.0',
    author='Alex He',
    author_email='hdl730@163.com',
    description='',
    data_files=[
        ('co_killer/resource', ['co_killer/resource/exc_handler.asm', 'co_killer/resource/exc_handler_p8.asm'])],
    entry_points={
        'console_scripts': [
            'coklr = co_killer.script:main',
        ]
    }
)
