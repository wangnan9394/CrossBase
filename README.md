# Populations_Linkage_groups_by_WGS

DATA ：2代
How to obtain vcfs：
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
# 3.排序
gatk MarkDuplicates --REMOVE_DUPLICATES=true -I ~/PATH/${line}.sort.bam -M ~/PATH/${line}.sort.markdup_metrics.txt -O ~/PATH/${line}.sort.removedup.bam
samtools index ~/PATH/${line}.sort.removedup.bam
echo "** ${line} sorted raw bam file done **"
done
```
