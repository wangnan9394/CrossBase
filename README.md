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
### Two step(IN GPU/CPU)
container：
docker pull google/deepvariant:rc1.0.0-gpu(GPU)
docker pull google/deepvariant:rc1.0.0(CPU)
### generate the vcfs
```
docker run --gpus all -v $INPUT:/input -v $OUTPUT:/output google/deepvariant:rc1.0.0-gpu /opt/deepvariant/bin/run_deepvariant --model_type=WGS --ref=$GENOME --reads=$BAM --output_vcf=$NAME.vcf.gz --output_gvcf=$NAME.g.vcf.gz --num_shards=24
```
### merge vcfs in glnexus
```
docker run \
   -v "$input":"/data" \
   quay.io/mlin/glnexus:v1.2.6 \
   /usr/local/bin/glnexus_cli \
   --config DeepVariantWGS \
 ~all .g.vcf.gz files \
 | bcftools view - | bgzip -c > ${output}/deepvariant.cohort.vcf.gz
```
##
# Three step
obtain different markers
*like:aaXbb,nnXnp,lmXll,hkXhk*





#### CONFIGURE A DOCKER-GPU
IF YOU NEED TO CONFIGURE A GPU,in root!!!

### check the system
```
cat /etc/os-release 
```
### pre-DNS
```
cat /etc/resolv.conf
```
### make a rpm
```
rpm -Uvh http://www.elrepo.org/elrepo-release-7.0-3.el7.elrepo.noarch.rpm
```
### Shield system tape drive
```
vi /lib/modprobe.d/dist-blacklist.conf
### delete
#blacklist nvidiafb
### add
blacklist nouveau  
options nouveau modeset=0 
```
### check
```
cat /lib/modprobe.d/dist-blacklist.conf
```
### rebuild initramfs image
```
mv /boot/initramfs-$(uname -r).img /boot/initramfs-$(uname -r).img.bak  
dracut /boot/initramfs-$(uname -r).img $(uname -r) 
```
### restart system
```
reboot
```
### check 
```
lsmod | grep nouveau 
```
### install gpu-driver
```
yum -y install kmod-nvidia
```
### restart system
```
reboot
```
### check gpu-driver
```
nvidia-smi 
```
### install docker
```
curl -fsSL https://get.docker.com | bash -s docker --mirror Aliyun
```
### install NVIDIA Container Toolkit
```
distribution=$(. /etc/os-release;echo $ID$VERSION_ID) 
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.repo | sudo tee /etc/yum.repos.d/nvidia-docker.repo 
yum install -y nvidia-container-toolkit 
systemctl restart docker
```
####Test nvidia-smi with the latest official CUDA image
```
docker run --gpus all nvidia/cuda:10.0-base nvidia-smi
```
#Start a GPU enabled container on two GPUs
```
docker run --gpus 2 nvidia/cuda:10.0-base nvidia-smi
```
#Starting a GPU enabled container on specific GPUs
```
docker run --gpus '"device=1,2"' nvidia/cuda:10.0-base nvidia-smi
docker run --gpus '"device=UUID-ABCDEF,1"' nvidia/cuda:10.0-base nvidia-smi
```
#Specifying a capability (graphics, compute, ...) for my container
#Note this is rarely if ever used this way
```
docker run --gpus all,capabilities=utility nvidia/cuda:10.0-base nvidia-smi
```
