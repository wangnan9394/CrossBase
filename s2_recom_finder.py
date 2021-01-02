#-*- coding:utf-8 -*-
import vcf 
import numpy as np
import argparse
import pandas as pd
import random

parser = argparse.ArgumentParser(description = '该脚本用于第一步初步找重组位点', add_help = False, \
    usage = 'python3 s2_recom_finder.py -i [input.txt] -o [output.txt] ')
required = parser.add_argument_group()
optional = parser.add_argument_group()
required.add_argument('-i', '--input', metavar = '[input.txt]', help = '输入 txt文件', required = True)
required.add_argument('-o', '--output', metavar = '[output.txt]', help = '输出的重组txt文件', required = True)
#required.add_argument('-', '--kernel', metavar = '[kernel]', help = '卷积核长度', required = True)
#required.add_argument('-r', '--region', metavar = '[region]', help = '范围值 Mb', default='2',type=int)

args = parser.parse_args()

filetxt=open(args.output,'w')

data=pd.read_csv(args.input,sep='\t',header=None)
#print(file)
col=[i for i in range(4,235)]
col=[1]+col
file=data[col]
#print(file)

kl=50
line1=np.random.randint(1,2,kl)
line2=np.random.randint(-1,0,kl)
line3=np.hstack((line1,line2))
kernel=line3
#kernel=np.array([[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]])
kernel=kernel.reshape(-1,1)
chrom=np.array(data[1])
#print(chrom)
#print(len(chrom))

#############100kb操作重组
for n in range(1,1000):
    lista=[]
    for i in range(len(chrom)-1):
        if chrom[i] >100000*(n-1) and chrom[i]<100000*n:##这个范围500k
            #print(i)
            lista.append(i)
    #print(lista)
    if not lista == []:
        file=data[col]
        file=file.loc[lista[0]:lista[-1]]
       # print(file)
        shu=random.randrange(4,235)
      #  print(shu)
        lie=file[shu]  ##4可变index,随机选两个
        lies=lie == 1   ####以0或者1作为suoyin
        filter=file.loc[lies]
        filter_chrom=np.array(filter[1])
       # print(filter_chrom)
        dict={}
        for ge in range(4,235):
            test=np.array(filter[ge]) ###测试其他单株
            length=len(test)
         #   print(length)
           # print(test)
      #      print(n)
            for i in range(length-kl*2):
                out=np.dot(test[0+i:kl*2+i],kernel)
                if abs(out[0])>15: 
                   # print(test[0+i:100+i])
                #    print(ge)
                   # print(filter_chrom[i])
                    dict[ge]=filter_chrom[i]
                 #   print(str(ge)+'\t'+str(filter_chrom[i]))
        for key,value in dict.items():
            key=str(key)
            value=str(value)
            filetxt.write(str(n)+'round100KB'+'\t'+key+'\t'+value+'\n')
            print(str(n)+'round100KB'+'\t'+key+'\t'+value)
