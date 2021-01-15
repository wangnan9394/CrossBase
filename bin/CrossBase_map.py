#！/usr/bin/python3
import os
import argparse

parser = argparse.ArgumentParser(description = 'For mapping and calling variants', add_help = False, \
    usage = '\npython CrossBase.py -g -map -call -sample_dir -sample_list -t 20')

required = parser.add_argument_group()
optional = parser.add_argument_group()
required.add_argument('-g', '--genome_path', metavar = '[input.vcf]', help = 'merge vcf', required = True)
required.add_argument('-map', '--map_config', metavar = '[mother_ID]', help = 'male name', required = True)
required.add_argument('-call', '--call_config', metavar = '[father_ID]', help = 'female name', required = True)
required.add_argument('-sample_dir', '--sample_dir', metavar = '[sample_dir]', help = 'sample_dir', required = True)
required.add_argument('-sample_list', '--sample_list', metavar = '[sample_list]', help = 'sample_list', required = True)
required.add_argument('-t', '--threads', metavar = '[threads]', help = 'threads', required = True,default=20)
optional.add_argument('-h', '--help', action = 'help', help = 'help information')

args = parser.parse_args()

def prepare_software(name):
    CMD0='echo "checking {}"'.format(name)
    os.system(CMD0)
    CMD1='which {} 2>run.log'.format(name)
    os.system(CMD1)
    var=os.popen('cat run.log|wc -l').read()
    if int(var)>0:
        CMD3='echo "please install {}"'.format(name)
        os.system(CMD3)
        os._exit()
    if var=='':
        CMD4='check {} done!'.format(name)
        os.system(CMD4)

def pre_deepvariant():
    CMD1='docker pull google/deepvariant:rc1.0.0'
    CMD2='docker pull quay.io/mlin/glnexus:v1.2.6'
    os.system(CMD1)
    os.system(CMD2)

def build_index(genome_path):
    if genome_path[:-2]=='fa':
        dict_name=genome_path[:-2]+'dict'
    if genome_path[:-5]=='fasta':
        dict_name=genome_path[:-5]+'dict'
    CMD1='samtools faidx {}'.format(genome_path)
    CMD2='bwa index {}'.format(genome_path)
    CMD3='gatk CreateSequenceDictionary -R {} -O {}'.format(genome_path,dict_name)

##sample_list,one line one sample
def pre_mapping_shell(config_file,genome_path,sample_dir,sample_list,threads):
    CMD1='rm -rf pre_mapping.sh'
    CMD2='mkdir 0.bam'
    CMD3='mkdir 1.sort.bam'
    os.system(CMD1)
    os.system(CMD2)
    os.system(CMD3)
    config1 = open(config_file,"r")
    content = config1.read()
    config1.close()
    t1 = content.replace("genome_path",genome_path)
    t2 = t1.replace("threads",threads)
    t3 = t2.replace("sample_dir",sample_dir)
    t4 = t3
    t5 = t4.replace("sample.list",sample_list)
    with open("mywork.mapping.config.sh","w") as f2:
        f2.write(t5)
    CMD5='bash mywork.mapping.config.sh'
    os.system(CMD5)

###call_SNP_merge
def call_variant(config_file,genome_path,sample_list,threads,input_dir='1.sort.bam',output_dir='2.vcf'):
    CMD1='mkdir 2.vcf'
    os.system(CMD1)
    config1 = open(config_file,"r")
    content = config1.read()
    config1.close()
    reference=genome_path.split('/')[-1]
    genome_dir=genome_path[:-len(reference)]
    t1 = content.replace("genome_dir",genome_dir)
    t2 = t1.replace("input_dir",input_dir)
    t3 = t2.replace("output_dir",output_dir)
    t4 = t3.replace("reference",reference)
    t5 = t4.replace("threads",threads)
    t6 = t5.replace("sample.list",sample_list)
    with open("mywork.calling.config.sh","w") as f2:
        f2.write(t6)
    CMD2='bash mywork.mapping.config.sh'
    os.system(CMD2)
    CMD3='mkdir 3.merge_vcf'
    os.system(CMD3)
    with open("merge.sh","w") as f:
        l1='docker run -v '+output_dir+':/work quay.io/mlin/glnexus:v1.2.6 /usr/local/bin/glnexus_cli --config DeepVariantWGS \\'+'\n'
        f.write(l1)
        s=''
        with open(sample_list,'r') as f2:
            for line in f2:
                line='/work/'+line+'.g.vcf.gz\ '
                s+=line
        f.write(s)
        l2='| bcftools view - | bgzip -c > 3.merge_vcf/deepvariant.cohort.vcf.gz'
        f.write(l2)
    CMD5='bash merge.sh'
    os.system(CMD5)

prepare_software('samtools')
prepare_software('bwa')
prepare_software('gatk')
pre_deepvariant()
build_index(args.genome_path)
pre_mapping_shell(args.map_config,args.genome_path,args.sample_dir,args.sample_list,args.threads)
call_variant(args.call_config,args.genome_path,args.sample_list,args.threads,input_dir='1.sort.bam',output_dir='2.vcf')
