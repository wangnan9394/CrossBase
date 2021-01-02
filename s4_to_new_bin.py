import math
from collections import Counter
import argparse

parser = argparse.ArgumentParser(description = '该脚本用于第一步初步找重组位点', add_help = False, \
    usage = 'python3 s4_to_new_bin.py -i [input.txt] -o [output.txt] ')
required = parser.add_argument_group()
optional = parser.add_argument_group()
required.add_argument('-i', '--input', metavar = '[input.txt]', help = '输入 txt文件', required = True)
required.add_argument('-step_file', '--step_file', metavar = '[step.txt]', help = '输入第二步的 txt文件', required = True)
required.add_argument('-o', '--output', metavar = '[output.txt]', help = '输出的重组txt文件', required = True)
args = parser.parse_args()

loc_file=open(args.output,'w')

list=[]
with open(args.step_file,'r') as f:
    for i in f:
        i=i.replace('\n','').split()
        list.append(i[2])
#print(list)
ll=len(list)
#print(ll)

def transform(line):
    line = line.strip('\n').split('\t')
    chr = line[0]
    position = int(line[1])
    seq = line[4:-2]
    seq = ''.join(map(str,seq))
    return chr,position,seq



num=0
for i in range(ll-1):
  #  print('region',str(i))
    a= int(list[i])
    b= int(list[i+1])
   # print(a,b)
    list_count=[]
    with open(args.input,'r') as f:
        for i in f:
          #  print(i)
            chr,pos,seq=transform(i)
          #  print(pos)
            if pos >a and pos <b:
                list_count.append(seq)
    r = Counter(list_count).most_common(2)
    if r != [] and len(r)==2:
        #print(len(r))
        r0=(r[0])[0]
        s1=''
        for i in r0:
            s1+=i + '\t'
        loc_file.write(chr + '_'+'marker1'+'_'+str(a)+'_'+str(b)+'\t'+s1 + '\n')
        r1=(r[1])[0]
        s2=''
        for i in r1:
            s2+=i + '\t'
        loc_file.write(chr+ '_'+'marker2'+'_'+str(a)+'_'+str(b)+'\t'+s2 + '\n')
    if r ==[]:
        num+=1
print(num)

        # print(chr,position,seq)
