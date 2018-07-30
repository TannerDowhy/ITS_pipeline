library(dada2);
packageVersion("dada2")
# Merge multiple runs (if necessary)
args <- commandArgs(TRUE)
st <- readRDS(args[1])
# Remove chimeras
seqtab <- removeBimeraDenovo(st, method="consensus", multithread=TRUE)
# Assign taxonomy
tax <- assignTaxonomy(seqtab, "silva_nr_v128_train_set.fa.gz", multithread=TRUE)
# tax2 <- assignTaxonomy(seqtab, "../software/gg_13_8_otus/rep_set/99_otus.fasta.gz", multithread=TRUE)
#tax <- assignTaxonomy(seqtab, "sh.sh_general_release_dynamic_01.12.2017.fasta.gz", multithread=TRUE)
# Write to disk
write.csv(seqtab, args[2])
write.csv(tax, args[3])
saveRDS(seqtab, args[4])
saveRDS(tax, args[5])
#write.csv(tax2, args[6])
#saveRDS(tax2, args[7])
