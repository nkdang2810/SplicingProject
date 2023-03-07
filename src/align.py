from pathlib import Path
import subprocess

# name = "data_remove_MT_rDNA" 
# name = "alignments_clean_TOPHAT" 
# name = "alignments_clean_HISAT" 
name = "alignments_clean_STAR" 
out_dir = Path(f"/rsrch4/home/mol_cgenesis/EMC_BIC_rsrch4/nkdang/Splicing_Projects/new/data/{name}")
out_dir.mkdir(parents=True, exist_ok=True)

log_dir = Path(
    f"/rsrch4/home/mol_cgenesis/EMC_BIC_rsrch4/nkdang/Splicing_Projects/new/log/{name}")
log_dir.mkdir(parents=True, exist_ok=True)

path_lsf = Path(
    f"/rsrch4/home/mol_cgenesis/EMC_BIC_rsrch4/nkdang/Splicing_Projects/new/lsf/{name}")
path_lsf.mkdir(parents=True, exist_ok=True)

# for f1 in Path("/rsrch4/home/mol_cgenesis/EMC_BIC_rsrch4/nkdang/Splicing_Projects/new/data/data_remove_adapter").glob("*_R1_*.fq.gz"):
#     filename = Path(f1.stem.replace('_R1_val_1.fq',''))
#     f2 = str(f1).replace("_R1_val_1", "_R2_val_2")
#     if f1.name.startswith("2") or f1.name.startswith("3"):
#         # continue
#         command = f"#BSUB -W 10:00\n" \
#             f"#BSUB -q medium\n" \
#             f"#BSUB -n 8\n" \
#             f"#BSUB -M 150\n" \
#             f"#BSUB -R rusage[mem=150]\n" \
#             "#BSUB –u nkdang@mdanderson.org\n" \
#             f"#BSUB -J TRIM_{f1.stem}\n" \
#             f"#BSUB -o {log_dir.joinpath(filename.with_suffix('.log'))}\n" \
#             f"#BSUB –cwd /rsrch4/home/mol_cgenesis/EMC_BIC_rsrch4/nkdang/Splicing_Projects\n" \
#             f"module load python/2.7.15-bio\n" \
#             f"module load bowtie2/2.4.1\n" \
#             f"bowtie2 -x ref/bt2_mouse_index/mouse_rDNA_MT -1 {f1} -2 {f2} -S {out_dir.joinpath(filename)}.sam -p 8 --un-conc-gz {out_dir.joinpath(filename)}_clean"
#             # f"bbmap.sh threads=8 in1={f1} in2={f2} out={out_dir.joinpath(filename)}.sam ref=/rsrch4/home/mol_cgenesis/EMC_BIC_rsrch4/nkdang/Splicing_Projects/ref/GRCm39.primary_assembly.genome.fa nodisk" \
#             # f"STAR --genomeDir /rsrch4/home/mol_cgenesis/EMC_BIC_rsrch4/nkdang/Splicing_Projects/ref/m39_index --runThreadN 8 --readFilesCommand zcat --readFilesIn {f1} {f2} --outFileNamePrefix {out_dir.joinpath(filename)} --outReadsUnmapped Fastx --outSAMtype BAM SortedByCoordinate --outSAMunmapped Within --outSAMattributes Standard" 

#         with open(path_lsf.joinpath(f'{filename.stem}.lsf'), "w+") as out:
#             out.writelines(command)

#         command = f"bsub < {path_lsf.joinpath(f'{filename.stem}.lsf')}"
#         # print(command)
#         subprocess.Popen(command, shell=True)
#     else:
#         # continue
#         command = f"#BSUB -W 10:00\n" \
#             f"#BSUB -q medium\n" \
#             f"#BSUB -n 8\n" \
#             f"#BSUB -M 150\n" \
#             f"#BSUB -R rusage[mem=150]\n" \
#             "#BSUB –u nkdang@mdanderson.org\n" \
#             f"#BSUB -J TRIM_{f1.stem}\n" \
#             f"#BSUB -o {log_dir.joinpath(filename.with_suffix('.log'))}\n" \
#             f"#BSUB –cwd /rsrch4/home/mol_cgenesis/EMC_BIC_rsrch4/nkdang/Splicing_Projects\n" \
#             f"module load python/2.7.15-bio\n" \
#             f"module load bowtie2/2.4.1\n" \
#             f"bowtie2 -x ref/bt2_human_index/human_rDNA_MT -1 {f1} -2 {f2} -S {out_dir.joinpath(filename)}.sam -p 8 --un-conc-gz {out_dir.joinpath(filename)}_clean"
#             # f"bbmap.sh threads=8 in1={f1} in2={f2} out={out_dir.joinpath(filename)}.sam ref=/rsrch4/home/mol_cgenesis/EMC_BIC_rsrch4/nkdang/Splicing_Projects/ref/GRCh38.primary_assembly.genome.fa nodisk" \
#             # f"STAR --genomeDir /rsrch4/home/mol_cgenesis/EMC_BIC_rsrch4/nkdang/Splicing_Projects/ref/hg38_index --runThreadN 8 --readFilesCommand zcat --readFilesIn {f1} {f2} --outFileNamePrefix {out_dir.joinpath(filename)} --outReadsUnmapped Fastx --outSAMtype BAM SortedByCoordinate --outSAMunmapped Within --outSAMattributes Standard" 

#         with open(path_lsf.joinpath(f'{filename.stem}.lsf'), "w+") as out:
#             out.writelines(command)

#         command = f"bsub < {path_lsf.joinpath(f'{filename.stem}.lsf')}"
#         # print(command)
#         subprocess.Popen(command, shell=True)


for f1 in Path("/rsrch4/home/mol_cgenesis/EMC_BIC_rsrch4/nkdang/Splicing_Projects/new/data/data_remove_MT_rDNA").glob("*clean.1*"):
    filename = Path(f1.name.replace('_clean.1.fastq.gz',''))
    f2 = str(f1).replace("clean.1", "clean.2")
    if f1.name.startswith("2") or f1.name.startswith("3"):
        # continue
        command = f"#BSUB -W 24:00\n" \
            f"#BSUB -q medium\n" \
            f"#BSUB -n 12\n" \
            f"#BSUB -M 128\n" \
            f"#BSUB -R rusage[mem=128]\n" \
            "#BSUB –u nkdang@mdanderson.org\n" \
            f"#BSUB -J TRIM_{filename}\n" \
            f"#BSUB -o {log_dir.joinpath(filename.with_suffix('.log'))}\n" \
            f"#BSUB –cwd /rsrch4/home/mol_cgenesis/EMC_BIC_rsrch4/nkdang/Splicing_Projects\n" \
            f"STAR --genomeDir /rsrch4/home/mol_cgenesis/EMC_BIC_rsrch4/nkdang/Splicing_Projects/ref/m39_index --runThreadN 12 --readFilesCommand zcat --readFilesIn {f1} {f2} --outFileNamePrefix {out_dir.joinpath(filename)} --outReadsUnmapped Fastx --outSAMtype BAM SortedByCoordinate --outSAMunmapped Within --outSAMattributes Standard" 
            
            # f"module load hisat2/2.1.0\n" \
            # f"hisat2 -x ref/hisat2_mouse_index.idx -1 {f1} -2 {f2} -S {out_dir.joinpath(filename)}.sam\n" \
            
            # f"module load tophat/2.1.1\n" \
            # f"module load bowtie2/2.3.4.2\n" \
            # f"module load python/2.7.15-bio\n" \
            # f"tophat2 -G ref/gencode.vM31.primary_assembly.annotation.gtf -o {out_dir.joinpath(filename)} -p 12 ref/bt2_mouse_genome_index/mouse_genome {f1} {f2}" \


        with open(path_lsf.joinpath(f'{filename.stem}.lsf'), "w+") as out:
            out.writelines(command)

        command = f"bsub < {path_lsf.joinpath(f'{filename.stem}.lsf')}"
        # print(command)
        subprocess.Popen(command, shell=True)
    else:
        # continue
        command = f"#BSUB -W 24:00\n" \
            f"#BSUB -q medium\n" \
            f"#BSUB -n 12\n" \
            f"#BSUB -M 128\n" \
            f"#BSUB -R rusage[mem=128]\n" \
            "#BSUB –u nkdang@mdanderson.org\n" \
            f"#BSUB -J TRIM_{filename}\n" \
            f"#BSUB -o {log_dir.joinpath(filename.with_suffix('.log'))}\n" \
            f"#BSUB –cwd /rsrch4/home/mol_cgenesis/EMC_BIC_rsrch4/nkdang/Splicing_Projects\n" \
            f"STAR --genomeDir /rsrch4/home/mol_cgenesis/EMC_BIC_rsrch4/nkdang/Splicing_Projects/ref/hg38_index --runThreadN 12 --readFilesCommand zcat --readFilesIn {f1} {f2} --outFileNamePrefix {out_dir.joinpath(filename)} --outReadsUnmapped Fastx --outSAMtype BAM SortedByCoordinate --outSAMunmapped Within --outSAMattributes Standard" 
            # f"module load hisat2/2.1.0\n" \
            # f"hisat2 -x ref/hisat2_human_index.idx -1 {f1} -2 {f2} -S {out_dir.joinpath(filename)}.sam\n" \

            # f"module load tophat/2.1.1\n" \
            # f"module load bowtie2/2.3.4.2\n" \
            # f"module load python/2.7.15-bio\n" \
            # f"tophat2 -G ref/gencode.v42.primary_assembly.annotation.gtf -o {out_dir.joinpath(filename)} -p 12 ref/bt2_human_genome_index/human_genome {f1} {f2}" \
            

        with open(path_lsf.joinpath(f'{filename.stem}.lsf'), "w+") as out:
            out.writelines(command)

        command = f"bsub < {path_lsf.joinpath(f'{filename.stem}.lsf')}"
        # print(command)
        subprocess.Popen(command, shell=True)