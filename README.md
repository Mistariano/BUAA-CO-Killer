# BUAA CO Killer

> **作者已停止维护，该仓库仅供参考**

> **如果在测试CPU时使用了该项目生成的测试数据，建议向助教主动说明**


为北航六系计算机组成原理课设编写的CPU测试程序自动生成器


作者的课设进度：P8通过

环境依赖：
- Python 3.5/3.6/3.7


## 安装与运行

注意版本已更新，与先前版本启动方式不同

目前已知问题：
- 在Py3.5的安装路径中如果含有中文等特殊字符会安装失败，如果遇到这个问题直接运行`coklr`脚本即可。其他版本的Python很可能也存在这个问题

```bash
# Download
git clone https://github.com/Mistariano/BUAA-CO-Killer.git
cd BUAA-CO-Killer

# Install
python setup.py install

# Check installation & show helps
coklr -h
```

```bash

# Run with default settings
coklr <output_dir>

# Generate 100 asm files, with 1023 instructions in each of them
coklr <output_dir> --n_case 100 --k_instr 1023

# Generate test cases for P5(on MIPS-LITE)
coklr <output_dir> --instr_set lite

# Generate test cases for P6(on MIPS-C3)
coklr <output_dir> --instr_set c3
```

## 支持指令

加*表示未完成

1.	LB
2.	LBU
3.	LH
4.	LHU
5.	LW
6.	SB
7.	SH
8.	SW
9.	ADD
10.	ADDU
11.	SUB
12.	SUBU
13.	MULT
14.	MULTU
15.	DIV
16.	DIVU
17.	SLL
18.	SRL
19.	SRA
20.	SLLV
21.	SRLV
22.	SRAV
23.	AND
24.	OR
25.	XOR
26.	NOR
27.	ADDI
28.	ADDIU
29.	ANDI
30.	ORI
31.	XORI
32.	LUI
33.	SLTI
34.	SLTIU
35.	SLT
36.	SLTU
37.	BEQ
38.	BNE
39.	BLEZ
40.	BGTZ
41.	BLTZ
42.	BGEZ
43.	J
44.	JAL
45.	JR
46.	JALR
47.	MFHI
48.	MFLO
49.	MTHI
50.	MTLO
51. MFC0
52. MTC0
53. ERET

## 编写自己的测试脚本

1. 自定义模板：继承Template并重载`get_initial_compilable_instances`
2. 自定义Task：
    1. `from co_killer.task import Task`
    2. 实例化一个`Task`，并使用`add_template_class`将模板类挂载入Task
3. 运行：调用`Task`对象的`run`方法

示例：自定义模板并定义自己的`Task`

```python
from co_killer.task import ASMGenerateTask
from co_killer.compilable import ExcHandlerTemplate, Template
from co_killer.builtin.instructions import *


class MyExcHandlerTemplate(ExcHandlerTemplate):
    def get_initial_compilable_instances(self):
        instr_seq = [
            # add your instructions here
            ADDI(rs=0, rt=0, imm=0),
            NOP(),
        ]
        return instr_seq


class MyASMTextTemplate(Template):
    def get_initial_compilable_instances(self):
        instr_seq = [
            # add your instructions here
            ORI(),
            ORI(),
            ORI(),
            ORI(),
        ]
        return instr_seq


def get_task():
    task = ASMGenerateTask(output_dir='output',
                repeat_time=5,
                builtin_exc_handler=None,
                name='my_task'
                )

    task.add_handler_template_class(template_cls=MyExcHandlerTemplate)
    task.add_template_class(template_cls=MyASMTextTemplate)
    return task


def main():
    task = get_task()
    task.run()


if __name__ == '__main__':
    main()

```

注意，当不给`ORI`或其他内建指令指定参数时，将会使用安全的随机值

上述代码生成5个测试文件，其中一个内容如下：
```
.ktext 0x4180:
# 0x4180
addi $22 $16 -5569
# 0x4184
nop
.text:

# 0x3000
ori $19 $16 0xd311
# 0x3004
ori $26 $5 0x245d
# 0x3008
ori $24 $19 0x6b15
# 0x300c
ori $4 $7 0x52bf

tail_loop_0:
# 0x3010
j tail_loop_0
# 0x3014
nop
```


## 自动化测试：多进程、调度器及任务队列

stay tuned

## Contribution

已停止维护

## 软件许可协议

GNU GPL v3
