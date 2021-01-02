#-*- coding: UTF-8 -*-
import vcf
import argparse
import os

# Author: NAN WANG, wangnan9349@163.com

parser = argparse.ArgumentParser(description = '该脚本用于过滤vcf文件，输入vcf文件,输出aa×bb、lm×ll、nn×np和hk×hk四种标记', add_help = False, \
    usage = '\npython Filter_marker_2_four_type.py -i [input.vcf] -f [father_ID] -m [mother_ID]')
required = parser.add_argument_group()
optional = parser.add_argument_group()
required.add_argument('-i', '--input', metavar = '[input.vcf]', help = '输入 vcf 文件', required = True)
required.add_argument('-m', '--mother', metavar = '[mother_ID]', help = '母本ID名', required = True)
required.add_argument('-f', '--father', metavar = '[father_ID]', help = '父本ID名', required = True)
optional.add_argument('-h', '--help', action = 'help', help = '帮助信息')

args = parser.parse_args()


vcf_reader = vcf.Reader(open(args.input, 'r'))
out_aaXbb=(args.input)[:-4]+'_aaXbb.vcf'
out_lmXll=(args.input)[:-4]+'_lmXll.vcf'
out_nnXnp=(args.input)[:-4]+'_nnXnp.vcf'
out_hkXhk=(args.input)[:-4]+'_hkXhk.vcf'
vcf_writer_aaXbb = vcf.Writer(open(out_aaXbb, 'w'), vcf_reader)
vcf_writer_lmXll = vcf.Writer(open(out_lmXll, 'w'), vcf_reader)
vcf_writer_nnXnp = vcf.Writer(open(out_nnXnp, 'w'), vcf_reader)
vcf_writer_hkXhk = vcf.Writer(open(out_hkXhk, 'w'), vcf_reader)

for record in vcf_reader:
    a = record.genotype(args.mother)['GT']
    b = record.genotype(args.father)['GT']
    if (a == '0/0' or a == '1/1') and (a == '0/0' or b == '1/1'):
        vcf_writer_aaXbb.write_record(record)
    if a == '0/1' and (b == '0/0' or b == '1/1'):
        vcf_writer_lmXll.write_record(record)
    if (a == '0/0' or a == '1/1') and b == '0/1':
        vcf_writer_nnXnp.write_record(record)
    if a == '0/1' and b == '0/1':
        vcf_writer_hkXhk.write_record(record)
os.system('echo finished!')
