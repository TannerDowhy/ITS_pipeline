import argparse
from Bio.SeqIO.FastaIO import SimpleFastaParser
from Bio.Seq import Seq
import os


# Get number of lines must be either 2 or 4
# Generate the reverse compliments
# Take care of /1 and /F

def gen_permutations(fasta):
    adapters = []
    adapters_rc = []
    adapters_tmp = []
    with open(fasta) as f:
        for t in SimpleFastaParser(f):
            a = t[0].split('/')
            adapters_tmp.append([a[0], a[1], t[1]])
    f.close()

    for a in adapters_tmp:
        adapters_rc.append([a[0], a[1], a[2]])
        adapters_rc.append([a[0]+str("_rc"), a[1]+str('_rc'), str(Seq(a[2]).reverse_complement())])

    one = adapters_rc[0]
    one_rc = adapters_rc[1]
    two = adapters_rc[2]
    two_rc = adapters_rc[3]

    for a in range(4):
        if a == 0:
            adapters.append([one[0], one[2], " -g ", one[1]])
        elif a == 1:
            adapters.append([one_rc[0], one_rc[2], " -A ", one_rc[1]])
        elif a == 2:
            adapters.append([two[0], two[2], " -G ", two[1]])
        elif a == 3:
            adapters.append([two_rc[0], two_rc[2], " -a ", two_rc[1]])
        else:
            print("Something's gone horribly wrong. Have fun debugging.")
    return adapters


def run_cutadapt(adapters, file, base):
    f = file.split('/')
    f = f[-1]
    f = f.replace('.fastq.gz', '')
    p = f.replace('_R1', '_R2')

    os.system("~/.local/bin/cutadapt -m 100 -n 2 -q 20 --discard-untrimmed --pair-filter=both " + adapters[0][2] + ' ' + adapters[0][0] + "=" + adapters[0][1] + " " +
              adapters[3][2] + ' ' + adapters[3][0] + "=" + adapters[3][1] + " " + adapters[2][2] + ' ' + adapters[2][0] + "=" + adapters[2][1] + " " +
              adapters[1][2] + ' ' + adapters[1][0] + "=" + adapters[1][1] + " " + base + "/" + f + ".fastq.gz " + base + "/" + p + ".fastq.gz -o " +
              base + "/primer_removal/output/" + f + ".cutadapted.fastq.gz -p " + base + "/primer_removal/output/" + p + ".cutadapted.fastq.gz" + " > " + base + "/primer_removal/reports/" + f + ".report;")

def main():
    parser = argparse.ArgumentParser(description='Get the input file(s) and adapter file.')
    parser.add_argument('-a', type=argparse.FileType('r'), help='path to the adapter file')
    parser.add_argument('-b', help='base file path')
    parser.add_argument('-f', type=argparse.FileType('r'), nargs=argparse.REMAINDER, help='path to the forward read files directory')

    args = parser.parse_args()

    adapters = gen_permutations(args.a.name)

    for file in args.f:
        run_cutadapt(adapters, file.name, args.b)


if __name__ == "__main__":
    main()
