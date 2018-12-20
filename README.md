# BUAA CO Killer

为北航六系神课计算机组成原理设计的CPU测试程序自动生成器

之后准备在这个项目的基础上进一步集成工具，得到完整的测试工具链

**如果在测试CPU时使用了该项目生成的测试数据，建议向助教主动说明**

开发中，**非常欢迎contribution**，包括但不限于issue、bug report

作者的课设当前进度：P7

环境依赖：
- Python 3.5 3.6 3.7


## 安装与运行

注意版本已更新，与先前版本启动方式不同

目前已知问题：
- 在Py3.5的安装路径中如果含有中文等特殊字符会安装失败，如果遇到这个问题直接运行`coklr.py`脚本即可。其他版本的Python很可能也存在这个问题

```bash
# Download
git clone https://github.com/Mistariano/BUAA-CO-Killer.git
cd BUAA-CO-Killer

# Install
python setup.py install

# Check installation & show helps
coklr.py -h
```

```bash

# Run with default settings
coklr.py <output_dir>

# Generate 100 asm files, with 1023 instructions in each of them
coklr.py <output_dir> --n_case 100 --k_instr 1023

# Generate test cases for P5(on MIPS-LITE)
coklr.py <output_dir> --instr_set lite

# Generate test cases for P6(on MIPS-C3)
coklr.py <output_dir> --instr_set c3
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
15.	DIV*
16.	DIVU*
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
37.	BEQ*
38.	BNE*
39.	BLEZ*
40.	BGTZ*
41.	BLTZ*
42.	BGEZ*
43.	J*
44.	JAL*
45.	JR*
46.	JALR*
47.	MFHI
48.	MFLO
49.	MTHI
50.	MTLO

## 编写自己的测试脚本

1. 自定义模板：继承Template并重载`initial_compilable_instances`
2. 自定义Task：
    1. `from co_killer.task import Task`
    2. 实例化一个`Task`，并使用`add_template_class`将模板类挂载入Task
3. 运行：调用task对象的`run`方法

示例：随机生成100*1000条P7测试指令
```python
from co_killer.task import Task
from co_killer.compilable import RandomKTemplate, instr_set


if __name__ == '__main__':
    task = Task(output_dir='./out', repeat_time=100, name='rand')
    task.add_template_class(template_cls=RandomKTemplate,  args={'k': 1000, 'instr_set': instr_set.MIPS_C4_SUBSET})
    task.run()
```




## 自动化测试：多进程、调度器及任务队列

stay tuned

## Contribution

我需要一波文档、注释、Bug Report

随便开issue就好，怎么PR都行

## 软件许可协议

GNU GPL v3
