###vcf_calling.CONFIG.sh
VERSION=0.10.0
GENOME_DIR=genome_dir
INPUT_DIR=input_dir
OUTPUT_DIR=output_dir
REFERENCE=reference
THREADS=threads
SAMPLE_LIST=sample.list

cat $SAMPLE_LIST|while read line
do
BAM=${line}.sort.removedup.bam
OUTPUT_VCF=${line}.vcf.gz
OUTPUT_GVCF=${line}.g.vcf.gz
docker run -v $INPUT_DIR:/input -v $OUTPUT_DIR:/output -v $GENOME_DIR:/genome google/deepvariant:${VERSION} /opt/deepvariant/bin/run_deepvariant --model_type=WGS --ref=/genome/reference --reads=/input/${BAM} --output_vcf=/output/${OUTPUT_VCF} --output_gvcf=/output/${OUTPUT_GVCF} --num_shards=threads
done