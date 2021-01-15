##mapping.CONFIG.sh
GENOME_PATH=genome_path
THREADS=threads
SAMPLE_LIST=sample.list

cat $SAMPLE_LIST |while read line
do
FQ1=sample_dir/${line}*1*
FQ2=sample_dir/${line}*2*
bwa mem -t $THREADS -R "@RG\tID:$line\tLB:$line\tSM:$line\tPL:illumina" $GENOME_PATH $FQ1 $FQ2 | samtools sort -o 0.bam/${line}.sort.bam
echo "** ${line} BWA MEM done **"
# 3.ÅÅÐò
gatk MarkDuplicates --REMOVE_DUPLICATES=true -I 0.bam/${line}.sort.bam -M 1.sort.bam/${line}.sort.markdup_metrics.txt -O 1.sort.bam/${line}.sort.removedup.bam
samtools index 1.sort.bam/${line}.sort.removedup.bam
echo "** ${line} sorted raw bam file done **"
done
