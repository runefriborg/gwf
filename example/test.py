
# This is an example workflow for read mapping using bwa and samtools.

from gwf import *

target('IndexGenome',
       input='ponAbe2.fa.gz', 
       output=['ponabe2-bwaidx.amb', 'ponabe2-bwaidx.ann', 'ponabe2-bwaidx.pac']) << '''
       
bwa index -p ponabe2-bwaidx -a bwtsw ponAbe2.fa.gz

'''

target('MapReads', 
       input=['Masala_R1.fastq.gz', 'Masala_R2.fastq.gz', 
              'ponabe2-bwaidx.amb', 'ponabe2-bwaidx.ann', 'ponabe2-bwaidx.pac'],
       output='Masala.unsorted.bam', 
       pbs=['-l nodes=1:ppn=16', '-l walltime=1:0:0']) << '''
       
bwa mem -t 16 ponabe2-bwaidx Masala_R1.fastq.gz Masala_R2.fastq.gz | \
    samtools view -Shb - > Masala.unsorted.bam
    
'''

target('SortBAM', input='Masala.unsorted.bam', output='Masala.sorted.rmdup.bam', pbs='-l walltime=1:0:0') << '''
samtools sort -o Masala.unsorted.bam /scratch/$PBS_JOBID/Masala | \
	 samtools rmdup -s - Masala.sorted.rmdup.bam
'''
