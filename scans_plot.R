#!/usr/bin/env Rscript

library(ggplot2)
args = commandArgs(trailingOnly=TRUE)
df <- read.table(file=args[1], sep='\t', header = TRUE)

pdf(args[2]) 
ggplot(df, aes(x=scanId, y=mean)) +geom_line(aes(y=N50), colour="grey50", linetype="dotted") +geom_line()
dev.off()