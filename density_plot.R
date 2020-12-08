#!/usr/bin/env Rscript

library(ggplot2)
args = commandArgs(trailingOnly=TRUE)
df <- read.table(file=args[1], sep='\t', header = TRUE)
col_x=args[3]
col_y=args[4]
pdf(args[2])
ggplot(df, aes_string(col_x,col_y)) + geom_hex(bins = 100) +scale_fill_continuous(type = "viridis") +theme_bw()
dev.off()