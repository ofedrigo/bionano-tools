#!/usr/bin/env Rscript

library(ggplot2)
args = commandArgs(trailingOnly=TRUE)
df <- read.table(file=args[1], sep='\t', header = TRUE)

pdf(args[2]) 
ggplot(df, aes(x=scanId, y=yield))+geom_line()
dev.off()