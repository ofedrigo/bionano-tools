#!/usr/bin/env Rscript

library(ggplot2)
args = commandArgs(trailingOnly=TRUE)
df <- read.table(file=args[1], sep='\t', header = TRUE)

pdf(args[2]) 
ggplot(data=df, aes(x=bin, y=val)) +geom_bar(stat="identity", fill="steelblue")+ theme_minimal()
  
dev.off()