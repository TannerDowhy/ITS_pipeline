# This is the Sample inference script

library(dada2);
packageVersion("dada2")
args <- commandArgs(TRUE)
# Path setup
path <- args[1]
filt_path <- file.path(path, "filtered")
merged_files <- list.files(path, pattern=".fastq")
filterAndTrim(file.path(path, merged_files), file.path(filt_path, merged_files), rm.phix=FALSE, truncLen=183,  multithread=TRUE)

filts <- list.files(filt_path, pattern=".fastq", full.names=TRUE)
sample.names <- sapply(strsplit(basename(filts), ".extended"), `[`, 1)
names(filts) <- sample.names

# Learn the errors
set.seed(100)
err_merged <- learnErrors(filts, nreads=1000000, MAX_CONSIST=100, multithread=TRUE, randomize=TRUE)

png(args[3])
plotErrors(err_merged, nominalQ=TRUE)
dev.off()

dds <- vector("list", length(sample.names))
names(dds) <- sample.names

for(sam in sample.names) {
    cat("Processing:", sam, "\n")
    derep <- derepFastq(filts[[sam]])
    dds[[sam]] <- dada(derep, err=err_merged, multithread=TRUE)
}
# Construct sequence table and write to disk
seqtab <- makeSequenceTable(dds)

write.csv(seqtab, file=args[4])
saveRDS(seqtab, args[5])
