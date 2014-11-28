import argparse



parser = argparse.ArgumentParser(description='Create melt def.chain')
parser.add_argument('integer',metavar='N',type=str,nargs='+',help='some')
# parser.add_argument('integers', metavar='N', type=int, nargs='+',
                   # help='an integer for the accumulator')

args = parser.parse_args()
print(args.accumulate(args.integers))