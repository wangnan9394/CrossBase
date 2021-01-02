# Populations_Linkage_groups_by_WGS

DATA ：2代
##How to obtain vcfs：
### One step:
make a list.txt including NAME (NAME_1_clean.fq.gz,NAME_2_clean.fq.gz),one line one NAME.
YOU HAVE TO MAKE A CORRECT PATH
```shell
# bwa mem
reference=~/genome.fa
cat list.txt|while read line
do
bwa mem -t 20 -R "@RG\tID:$line\tLB:$line\tSM:$line\tPL:illumina" $reference ~/PATH/${line}_1_clean.fq.gz ~/PATH/${line}_2_clean.fq.gz | samtools sort -o ~/PATH/${line}.sort.bam
echo "** ${line} BWA MEM done **"
# remove duplicates, sort and index
gatk MarkDuplicates --REMOVE_DUPLICATES=true -I ~/PATH/${line}.sort.bam -M ~/PATH/${line}.sort.markdup_metrics.txt -O ~/PATH/${line}.sort.removedup.bam
samtools index ~/PATH/${line}.sort.removedup.bam
echo "** ${line} sorted raw bam file done **"
done
```
### Two step(IN GPU)
IF YOU NEED TO CONFIGURE A GPU,in root!!!
```
### check the system
cat /etc/os-release 
```
```
### pre-DNS
cat /etc/resolv.conf
```
```
### make a rpm
rpm -Uvh http://www.elrepo.org/elrepo-release-7.0-3.el7.elrepo.noarch.rpm
```
```
### Shield system tape drive
vi /lib/modprobe.d/dist-blacklist.conf
### delete
#blacklist nvidiafb
### add
blacklist nouveau  
options nouveau modeset=0 
```

