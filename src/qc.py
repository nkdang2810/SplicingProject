from pathlib import Path
import subprocess

name = "data_remove_MT_rDNA"
out_dir = Path(f"/rsrch4/home/mol_cgenesis/EMC_BIC_rsrch4/nkdang/Splicing_Projects/new/qc/{name}")
out_dir.mkdir(parents=True, exist_ok=True)

log_dir = Path(
    f"/rsrch4/home/mol_cgenesis/EMC_BIC_rsrch4/nkdang/Splicing_Projects/new/log/qc/{name}")
log_dir.mkdir(parents=True, exist_ok=True)

path_lsf = Path(
    f"/rsrch4/home/mol_cgenesis/EMC_BIC_rsrch4/nkdang/Splicing_Projects/new/lsf/qc/{name}")
path_lsf.mkdir(parents=True, exist_ok=True)

# for f in Path("/rsrch4/home/mol_cgenesis/EMC_BIC_rsrch4/nkdang/Splicing_Projects/data2/data_raw2").glob("*.fastq.gz"):
for f in Path("/rsrch4/home/mol_cgenesis/EMC_BIC_rsrch4/nkdang/Splicing_Projects/new/data/data_remove_MT_rDNA").glob("*.fastq.gz"):
    # new_file =  f"/rsrch4/home/mol_cgenesis/EMC_BIC_rsrch4/nkdang/Splicing_Projects/qc_remove_MT_rDNA/{f.stem}"
    # subprocess.Popen(f"gzip -d {f} > {new_file}", shell=True)

    # subprocess.Popen(f"fastqc {new_file}", shell=True)
    filename = Path(Path(f.stem).stem)
    command = f"#BSUB -W 6:00\n" \
        f"#BSUB -q medium\n" \
        f"#BSUB -n 8\n" \
        f"#BSUB -M 100\n" \
        f"#BSUB -R rusage[mem=100]\n" \
        "#BSUB –u nkdang@mdanderson.org\n" \
        f"#BSUB -J QC_{filename}\n" \
        f"#BSUB -o {log_dir.joinpath(filename.with_suffix('.log').name)}\n" \
        f"#BSUB –cwd /rsrch4/home/mol_cgenesis/EMC_BIC_rsrch4/nkdang/Splicing_Projects\n" \
        f"fastqc {f} -t 8 -o {out_dir}\n" \

    with open(path_lsf.joinpath(f'{filename}.lsf'), "w+") as out:
        out.writelines(command)

    command = f"bsub < {path_lsf.joinpath(f'{filename}.lsf')}"
    # print(command)
    subprocess.Popen(command, shell=True)