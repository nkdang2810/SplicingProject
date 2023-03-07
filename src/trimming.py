from pathlib import Path
import subprocess

out_dir = Path("/rsrch4/home/mol_cgenesis/EMC_BIC_rsrch4/nkdang/Splicing_Projects/new/data/data_remove_adapter")
out_dir.mkdir(parents=True, exist_ok=True)

qc_out_dir = Path("/rsrch4/home/mol_cgenesis/EMC_BIC_rsrch4/nkdang/Splicing_Projects/new/qc/qc_remove_adapter")
qc_out_dir.mkdir(parents=True, exist_ok=True)

log_dir = Path(
    "/rsrch4/home/mol_cgenesis/EMC_BIC_rsrch4/nkdang/Splicing_Projects/new/log/galore")
log_dir.mkdir(parents=True, exist_ok=True)

path_lsf = Path(
    "/rsrch4/home/mol_cgenesis/EMC_BIC_rsrch4/nkdang/Splicing_Projects/new/lsf/galore")
path_lsf.mkdir(parents=True, exist_ok=True)

for f1 in Path("/rsrch4/home/mol_cgenesis/EMC_BIC_rsrch4/nkdang/Splicing_Projects/data2/data_raw2").glob("*_R1.fastq.gz"):
    filename = Path(f1.stem.replace('_R1.fastq',''))
    f2 = str(f1).replace("_R1.fastq.gz", "_R2.fastq.gz")
    command = f"#BSUB -W 6:00\n" \
        f"#BSUB -q medium\n" \
        f"#BSUB -n 8\n" \
        f"#BSUB -M 50\n" \
        f"#BSUB -R rusage[mem=50]\n" \
        "#BSUB –u nkdang@mdanderson.org\n" \
        f"#BSUB -J TRIM_{f1.stem}\n" \
        f"#BSUB -o {log_dir.joinpath(filename.with_suffix('.log'))}\n" \
        f"#BSUB –cwd /rsrch4/home/mol_cgenesis/EMC_BIC_rsrch4/nkdang/Splicing_Projects\n" \
        f"trim_galore --core 8 -o {out_dir} --paired {f1} {f2} --fastqc_args '-t 8 -o {qc_out_dir}'\n" \

    with open(path_lsf.joinpath(f'{filename.stem}.lsf'), "w+") as out:
        out.writelines(command)

    command = f"bsub < {path_lsf.joinpath(f'{filename.stem}.lsf')}"
    # print(command)
    subprocess.Popen(command, shell=True)