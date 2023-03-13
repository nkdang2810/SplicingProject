
#!/usr/bin/env Rscript
library(argparse)

parser <- ArgumentParser()
parser$add_argument("--foldChange", type="double", metavar="foldChange", default=0.0, help="FoldChange filter value [default \"%(default)s\"]")
parser$add_argument("--PCAScale", type="double", metavar="PCAScale", default=2, help="PCAScale value [default \"%(default)s\"]")
parser$add_argument("--pairwise", action='store_true', help="run pairwise comparison")
parser$add_argument("--input_data", help="Path to input data")
parser$add_argument("--input_metadata", help = "Path to input metadata")
parser$add_argument("--output", help = "Path to input data")

args <- parser$parse_args()
data_path = args$input_data
metadata_path = args$input_metadata
run_pairwise = args$pairwise
output_path = args$output
foldChange_cutoff = args$foldChange
PCAScale = args$PCAScale

dir.create(file.path(output_path), recursive = TRUE)

# import libraries
library(DESeq2)
library(ggplot2)
library(biomaRt)
library(ggpubr)
library(pheatmap)
library(gtools)

metaData <- read.table(metadata_path, header=TRUE, sep=",")

# read count file
countData <- read.table(file=data_path, head=T, sep=",", row.names=1, check.names=FALSE)
countData <- countData[,(names(countData) %in% metaData$id)]
dds <- DESeqDataSetFromMatrix(countData=round(countData),
                              colData=metaData,
                              design=~condition)
dds <- DESeq(dds)

# get_gene_name <- function(arg) {
#   unlist(strsplit(arg,"\\."))[1]
# }
# norm_counts <- counts(dds, normalized = T)
# norm_counts <- as.data.frame(norm_counts)
# norm_counts$Description <- rownames(norm_counts)
# norm_counts$Name <- unlist(lapply(rownames(norm_counts), get_gene_name))
# norm_counts <- norm_counts[, c(8,7,1,2,3,4,5,6)]
# write.table(norm_counts, "Tanner.gct", sep = "\t", quote = F, row.names = F)


# PCA diagram
rld <- rlog(dds)
par(pty="s")
png(file.path(output_path,"PCA.png"), width=5, height=5, units="in", res=300)
z <- plotPCA(rld, intgroup=c("condition"))
z + coord_fixed(ratio = PCAScale)
dev.off()
# normalized counts for all genes
write.table(counts(dds, norm=T), file = file.path(output_path,"count_norm_all.csv"), sep=",",  row.names=TRUE, col.names=NA, quote=FALSE)
dev.off()

# generate heatmap for DE genes and sig genes
res <- results(dds)
res_sig <- subset(res, padj < 0.05 & abs(log2FoldChange) > foldChange_cutoff)
select  <- rownames(res_sig)
df <- as.data.frame(colData(dds)[,c("condition","celltype")])
ntd <- normTransform(dds)
png(file.path(output_path,"heatmap.png"), width=10, height=12, units="in", res=300)
pheatmap(assay(ntd)[select, ], cluster_rows=T, show_rownames=F, cluster_cols=T, annotation_col=df, scale="row")
dev.off()
write.table(res_sig, file.path(output_path,paste0("heatmap_sig_", foldChange_cutoff, ".csv")), sep=",", row.names=TRUE, col.names=NA, quote=FALSE)

if (run_pairwise){
  my_matrix <- permutations(n=length(unique(metaData$condition)),r=2,v=unique(metaData$condition))
  for(row in 1:nrow(my_matrix)) {
      t1 <- my_matrix[row, 1]
      t2 <- my_matrix[row, 2]
      name <-  paste0(t1, "_", t2)
      output_path_sub <- file.path(output_path, name)
      dir.create(file.path(output_path_sub))
      
      
      res <- results(dds, contrast =c("condition", t1, t2))
      res_sig<- subset(res, padj < 0.05)
      
      # print MA plot
      png(file.path(output_path_sub,paste0(name, "_MA.png")), width=10, height=7, units="in", res=300)
      EV <- ggmaplot(res, main = name,
                    fdr=0.05, fc=1, size=0.6,
                    palette = c("#B31B12", "#1465AC", "darkgray"),
                    legend = "top", top=10,
                    font.label = c("bold", 6),
                    font.legend= "bold",
                    font.main=c("bold"),
                    ggtheme = ggplot2::theme_minimal())
      print(EV)
      dev.off()
      write.table(res_sig, file.path(output_path_sub,paste0(name,"_sig.csv")), sep=",", row.names = TRUE, col.names =NA, quote = FALSE)
      write.table(res, file.path(output_path_sub,paste0(name,"_all.csv")), sep=",", row.names = TRUE, col.names =NA, quote = FALSE)
      
      # generate heatmap for DE genes
      dds_pair <- dds[,dds$condition %in% c(t1,t2)]
      
      select <- rownames(res_sig)
      df <- as.data.frame(colData(dds_pair)[,c("condition","celltype")])
      ntd <- normTransform(dds_pair)
      
      png(file.path(output_path_sub,paste0(name,"_heatmap.png")), width=5, height=8, units="in", res=300)
      pheatmap(assay(ntd)[select, ], cluster_rows=T, show_rownames=F, cluster_cols=T, annotation_col=df, scale="row")
      dev.off()
  }
}