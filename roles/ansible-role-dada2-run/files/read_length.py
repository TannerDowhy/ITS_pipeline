import csv
import re
import argparse


def read_length(file):
    prev = '100.000%'
    counter = 0
    with open(file, 'r') as tsvin:
        tsvin = csv.reader(tsvin, delimiter='\t')
        for row in tsvin:
            if counter < 10:
                counter+=1
            elif counter >= 10:
                r = str(row).split()

                m = re.match('^\'97\.*', prev)
                m_t = re.match('^\'98\.*', prev)
                n = re.match('^\'97\.*', r[4])
                if (m != None or m_t != None) and n == None:
                    prev_len=prev_len.replace('\',', '')
                    print(prev_len.replace('[\'', ''))

                # if re.search('\A97*', r[4]):
                #     print(r[0])
                prev_len = r[0]
                prev = r[4]

def main():
    parser = argparse.ArgumentParser(description='Get the path to the input file.')
    parser.add_argument('-f', type=argparse.FileType('r'), help='path to the hist file')

    args = parser.parse_args()

    file = args.f.name
    read_length(file)


if __name__ == "__main__":
    main()
