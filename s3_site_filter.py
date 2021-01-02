#-*- coding:utf-8 -*-
from itertools import groupby
import argparse

parser = argparse.ArgumentParser(description = '该脚本用于第二步过滤重组位点', add_help = False, \
    usage = 'python3 s3_site_filter.py -i [input.txt] -o [output.txt] ')
required = parser.add_argument_group()
optional = parser.add_argument_group()
required.add_argument('-i', '--input', metavar = '[input.txt]', help = '输入第一步 txt文件', required = True)
required.add_argument('-o', '--output', metavar = '[output.txt]', help = '输出的第二步过滤完成的txt文件', required = True)

args = parser.parse_args()


writer_out=open(args.output,'w')
with open(args.input,'r') as f:
    num=0
    for line in f:
        num+=1
   # print(num)
with open(args.input,'r') as f:
    lst=[]
    for line in f:
        line =line.replace('\n','').split('\t')
        position=int(line[2])
        lst.append(position)



##########以10kb为边界检测线
filter=[]
for k,g in groupby(sorted(lst),key=lambda x: x//10000):
    count=len(list(g))
    if count > 10:
        print("restart!python to fix out.file")
    if count>10 :
        line1=str(k*10000)+'\t'+str((k+1)*10000-1)+'\t'+str(count)
        print(line1)
        a=k*10000
        b=(k+1)*10000
        with open(args.input,'r') as f:
            for line in f:
                line =line.replace('\n','').split('\t')
                position=int(line[2])
              #  print(a,b)
                if position > a and position < b:
                    filter.append(position)
filter=sorted(list(set(filter)))
#
#print(filter)
with open(args.input,'r') as f:
    for line in f:
        line =line.replace('\n','').split('\t')
        position=int(line[2])
        if not position in filter:  
           # print(line)
            writer_out.write(line[0]+'\t'+line[1]+'\t'+line[2]+'\n')
