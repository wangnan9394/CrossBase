#-*- coding: UTF-8 -*-

import vcf
import argparse
from scipy import stats

# Author: NAN WANG, wangnan9349@163.com

parser = argparse.ArgumentParser(description = '该脚本用于过滤lmXll和nnXnp标记的vcf文件和偏分离标记，输入vcf文件，和过滤参数，需要载入PyVCF和argparse包，使用pip进行安装,输出过滤后的vcf文件和可以进行图谱构建的txt文档', add_help = False, \
    usage = '\nFilter_pop_lmXll_nnXnp_vcf_to_txt.py -i [input.vcf] -f [father_ID] -m [mother_ID] <optinal: -DP:覆盖深度 -GQ:质量值 -freq:频率 -p:p值 >')
required = parser.add_argument_group()
optional = parser.add_argument_group()
required.add_argument('-i', '--input', metavar = '[input.vcf]', help = '输入 vcf 文件', required = True)
required.add_argument('-f', '--father', metavar = '[father_ID]', help = '父本ID名', required = True)
required.add_argument('-m', '--mother', metavar = '[mother_ID]', help = '母本ID名', required = True)
required.add_argument('-p', '--p_value', metavar = '[p_value]', help = 'p_vaule值，约大约准确，范围0.001~0.00001，默认为0.001', default='0.001',type=float)
required.add_argument('-DP', '--read_depth', metavar = '[int]', help = '父母本覆盖深度,默认为10', default='10',type=int)
required.add_argument('-GQ', '--genotype_quality', metavar = '[int]', help = '父母本基因型质量值,默认为20', default='20',type=int)
required.add_argument('-freq', '--frequency', metavar = '[0<float<1]', help = '子代群体检测完整度,默认为0.6', default='0.6',type=float)
optional.add_argument('-h', '--help', action = 'help', help = '帮助信息')

args = parser.parse_args()

def read_file(name):
    name=name
    vcf_file=vcf.Reader(open(name, 'r'))
    return vcf_file

def value(type,value,freq,record):
    a = record.genotype(args.father)[type]
    b = record.genotype(args.mother)[type]
    if not a is None and not b is None and a > value and b > value:###筛选条件
        return record

def filter(record,gq_value,dp_value,freq,GQ='GQ',DP='DP'):
    record=value(GQ,gq_value,freq,record)
    if not record is None:
        record=value(DP,dp_value,freq,record)
        if not record is None:
            h_type=0
            b_type=0
            individual_allel=0
            num=0
            for i in record.samples:
                if i['GT'] == './.':
                    num+=1
                if i['GT'] =='0/0' or i['GT'] =='1/1':
                    b_type+=1
                if i['GT'] =='0/1':
                    h_type+=1
            individual_allel = b_type + h_type -2
            obs = [b_type,h_type]
            exp = [0.5*individual_allel,0.5*individual_allel]        
            chi_value=stats.chisquare(obs, f_exp = exp)
           # print(obs)
           # print(exp)
           # print(chi_value)
            rate = 1- float(num / len(record.samples))
           # print(1-rate)
            if chi_value[1] > args.p_value and rate > freq:  
               # print(record)
                #  print(record.genotype('PN')['GQ'])
                #  print(record.genotype('DB')['GQ'])
                #  print(record.genotype('PN')['DP'])
                #  print(record.genotype('DB')['DP'])
                vcf_writer_filter.write_record(record)###写入文件 
                chrom = str(record.CHROM)
                pos = str(record.POS)
                line = chrom + '-' + pos + '\t'
                for i in record.samples:
                    if i['GT'] == '0/0':
                        v = 'a' 
                    elif i['GT'] == '0/1':
                        v = 'h' 
                    elif i['GT'] == '1/1':
                        v = 'b' 
                    elif i['GT'] == './.':
                        v = '-' 
                    line += v + '\t'
                line += '\n'
                return line

filter_name=(args.input)[:-4]+ "_"+ str(args.read_depth)+"_"+ str(args.genotype_quality)+"_"+ str(args.frequency) + "_chisq_"+str(args.p_value)
filter_name_txt=filter_name+ ".txt"
filter_name_vcf=filter_name+ ".vcf"
file_txt=open(filter_name_txt,mode='w')
vcf_reader = read_file(args.input)
vcf_writer_filter = vcf.Writer(open(filter_name_vcf, 'w'), vcf_reader)
for record in vcf_reader:
    line=filter(record,gq_value=args.genotype_quality,dp_value=args.read_depth,GQ='GQ',DP='DP',freq=args.frequency)
    if not line is None:
        file_txt.write(line)


