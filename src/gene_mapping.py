import sys
from pathlib import Path
import json
import pandas as pd
from gtfparse import read_gtf
import requests
from p_tqdm import p_umap
from tqdm import tqdm

def main():
    if len(sys.argv) < 3:
        raise Exception("Missing input. First argument is the gtf. Next argument(s) are the csv files.")
    gtf_path = Path(sys.argv[1])
    files_path = sys.argv[2:]
    files_path = [Path(i) for i in files_path]

    print(f"\n\nGTF file is {gtf_path}")
    print(f"{len(files_path)} input file(s) are:")
    [print(i) for i in files_path]
    print("\n")

    # Load mapper_genename
    """
    Mapping from gene ID to gene name from GTF file
    """
    mapper_genename_path = Path(gtf_path.parent.joinpath(gtf_path.stem+"_mapper_genename.json"))
    if not mapper_genename_path.is_file():
        print("Mapper genename doesn't exist. Build gene_id VS gene_name mapper ...")
        gtf = read_gtf(gtf_path)

        mapper_genename = dict(zip(gtf['gene_id'],gtf["gene_name"]))
        with open(mapper_genename_path, 'w') as json_file:
            json_file.write(json.dumps(mapper_genename))
    else:
        print("Mapper genename exist. Load mapper") 
        with open(mapper_genename_path, "r") as f:
            mapper_genename = json.load(f)

    # Load mapper_description
    """
    Mapping from gene name to description from NCBI api
    """
    def api_caller(x):
        response = requests.get(f"https://clinicaltables.nlm.nih.gov/api/ncbi_genes/v3/search?terms={x}")
        try: 
            des = response.json()[3][0][4]
        except:
            des = ""
            
        return pd.DataFrame({"gene":x, "description":des}, index=[x])

    mapper_description_path = Path(gtf_path.parent.joinpath(gtf_path.stem+"_mapper_description.json"))
    if not mapper_description_path.is_file():
        print("Mapper description doesn't exist. Build gene_name VS description mapper ...")
        df_list = p_umap(api_caller, mapper_genename.values())
        df_combined = pd.concat(df_list, ignore_index=True)

        mapper_description = dict(zip(df_combined['gene'],df_combined['description']))
        with open(mapper_description_path, 'w') as json_file:
            json_file.write(json.dumps(mapper_description))
    else:
        print("Mapper description exist. Load mapper") 
        with open(mapper_description_path, "r") as f:
            mapper_description = json.load(f)


    # Mapping
    for f in tqdm(files_path, total=len(files_path)):
        df = pd.read_csv(f, index_col=0)
        df['gene'] = df.apply(lambda row: mapper_genename[row.name], axis=1)
        df['description'] = df.apply(lambda row: mapper_description[row['gene']], axis=1)
        df.to_csv(f.parent.joinpath(f.stem+"_annotated.csv"))

if __name__ == "__main__":
    main()