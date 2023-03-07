from pathlib import Path
import subprocess

name = "vast_out"
out_dir = Path(f"/rsrch4/home/mol_cgenesis/EMC_BIC_rsrch4/nkdang/Splicing_Projects/new/{name}")
out_dir.mkdir(parents=True, exist_ok=True)

log_dir = Path(
    f"/rsrch4/home/mol_cgenesis/EMC_BIC_rsrch4/nkdang/Splicing_Projects/new/log/{name}/align")
log_dir.mkdir(parents=True, exist_ok=True)

path_lsf = Path(
    f"/rsrch4/home/mol_cgenesis/EMC_BIC_rsrch4/nkdang/Splicing_Projects/new/lsf/{name}/align")
path_lsf.mkdir(parents=True, exist_ok=True)

for f1 in Path("/rsrch4/home/mol_cgenesis/EMC_BIC_rsrch4/nkdang/Splicing_Projects/new/data/data_remove_MT_rDNA").glob("*clean.1*"):
    filename = Path(f1.name.replace('_clean.1.fastq.gz',''))
    f2 = str(f1).replace("clean.1", "clean.2")
    if f1.name.startswith("2") or f1.name.startswith("3"):
        # continue
        command = f"#BSUB -W 24:00\n" \
            f"#BSUB -q medium\n" \
            f"#BSUB -n 12\n" \
            f"#BSUB -M 50\n" \
            f"#BSUB -R rusage[mem=50]\n" \
            "#BSUB –u nkdang@mdanderson.org\n" \
            f"#BSUB -J TRIM_{filename}\n" \
            f"#BSUB -o {log_dir.joinpath(filename.with_suffix('.log'))}\n" \
            f"#BSUB –cwd /rsrch4/home/mol_cgenesis/EMC_BIC_rsrch4/nkdang/Splicing_Projects\n" \
            f"module load bowtie/1.2.2\n" \
            f"./vast-tools/vast-tools align {f1} {f2} -sp mm10 -c 12 -n {filename} -o {out_dir.joinpath('mouse')}\n"
    else:
        continue
        command = f"#BSUB -W 24:00\n" \
            f"#BSUB -q medium\n" \
            f"#BSUB -n 12\n" \
            f"#BSUB -M 50\n" \
            f"#BSUB -R rusage[mem=50]\n" \
            "#BSUB –u nkdang@mdanderson.org\n" \
            f"#BSUB -J TRIM_{filename}\n" \
            f"#BSUB -o {log_dir.joinpath(filename.with_suffix('.log'))}\n" \
            f"#BSUB –cwd /rsrch4/home/mol_cgenesis/EMC_BIC_rsrch4/nkdang/Splicing_Projects\n" \
            f"module load bowtie/1.2.2\n" \
            f"./vast-tools/vast-tools align {f1} {f2} -sp hg38 -c 12 -n {filename} -o {out_dir.joinpath('human')}\n"
    with open(path_lsf.joinpath(f'{filename.stem}.lsf'), "w+") as out:
        out.writelines(command)

    command = f"bsub < {path_lsf.joinpath(f'{filename.stem}.lsf')}"
    # print(command)
    subprocess.Popen(command, shell=True)