# BUAA CO Killer

为北航六系神课计算机组成原理设计的CPU测试程序自动生成器

之后准备在这个项目的基础上进一步集成工具，得到完整的测试工具链

**如果在测试CPU时使用了该项目生成的测试数据，建议向助教主动说明**

开发中，**非常欢迎contribution**，包括但不限于issue、bug report

作者的课设当前进度：P7

环境依赖：
- Python 3.6


## 安装与运行

```bash
# Download
git clone https://github.com/Mistariano/BUAA-CO-Killer.git

# Install as a script 
# Stay tuned...

# Run with default settings
python main.py

# Show helps
python main.py -h

# Generate 100 asm files, with 1023 instructions in each of them
python main.py --n_case 100 --k_instr 1023

# Generate test cases for P6(on MIPS-C3)
python main.py --instr_set c3
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
13.	MULT*
14.	MULTU*
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
47.	MFHI*
48.	MFLO*
49.	MTHI*
50.	MTLO*

## 自定义代码模板

stay tuned

## 自动化测试：多进程、调度器及任务队列

stay tuned

## 软件许可协议

GNU GPL v3
