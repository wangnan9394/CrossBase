#-*- coding:utf-8 -*-
import vcf
import argparse

parser = argparse.ArgumentParser(description = '该脚本用于找重组位点', add_help = False, \
    usage = '\npython s1_transform.py -i [input.vcf]  <optinal:  >')
required = parser.add_argument_group()
optional = parser.add_argument_group()
required.add_argument('-i', '--input', metavar = '[input.vcf]', help = '输入 vcf 文件', required = True)
#required.add_argument('-', '--kernel', metavar = '[kernel]', help = '卷积核长度', required = True)
required.add_argument('-o', '--output', metavar = '[output.txt]', help = '输出转化完成的txt文件', required = True)
#required.add_argument('-r', '--region', metavar = '[region]', help = '范围值 Mb', default='2',type=int)

args = parser.parse_args()

#txtfile=args.input[:-4] + '.txt'
file=open(args.output,'w')
vcf_file=vcf.Reader(filename=args.input)
#n=1
for record in vcf_file:
    v=''
    line=''
   # if record.POS >1000000*(n-1)*args.region and record.POS < 1000000*n*args.region:
    for i in record.samples:
        if i['GT'] =='0|0' or i['GT'] =='1|1':
            v= '0'
        elif i['GT'] =='0|1' or i['GT'] =='1|0':
            v= '1'
        else:
            v='0.5'
        line +=v + '\t'
    file.write(record.CHROM+'\t'+str(record.POS)+'\t'+record.REF+'\t'+line + '\n')

