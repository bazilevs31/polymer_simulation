#!/usr/bin/env python
import argparse
from argparse import ArgumentDefaultsHelpFormatter
import os
def read_params():

	parser = argparse.ArgumentParser(description=__doc__,
                            formatter_class=argparse.ArgumentDefaultsHelpFormatter)

	# group = parser.add_mutually_exclusive_group(help='What do you want to do create melt or run sim')
	group = parser.add_mutually_exclusive_group()
	group.add_argument('--create', action='store_true',help='Create and equilibrate the run')
	group.add_argument('--run', action='store_true', help='Run the simulation')
	group.add_argument('--analyze', action='store_true', help='Analyze the alignment using AnalyzeTrueg2.py')
	
	parser.add_argument("-p", 
					"--procs",
                    dest="procs", 
                    default=12, 
                    type=int, 
                    help="Number of processors")
	parser.add_argument("-n", 
					"--nodes",
                    dest="nodes", 
                    default=5, 
                    type=int, 
                    help="Number of nodes")	
	parser.add_argument("-m", 
					"--memmory",
                    dest="memmory", 
                    default=600, 
                    type=int, 
                    help="Memmory to use")
	parser.add_argument("-wm", 
					"--wallminutes",
                    dest="wallminutes", 
                    default=0, 
                    type=int, 
                    help="Walltime minutes")
	parser.add_argument("-wh", 
					"--wallhours",
                    dest="wallhours", 
                    default=8, 
                    type=int, 
                    help="Number of nodes")
	parser.add_argument("-name", 
					"--pbsname",
                    dest="pbsname", 
                    default='poly', 
                    type=str, 
                    help="Name of pbs file")

	args = parser.parse_args()
	return args


# def main():
print "I am doing reading paramters"
args = read_params()
print args
procs,nodes,memmory,wallhours,wallminutes,pbsname = args.procs,args.nodes,args.memmory,args.wallhours,args.wallminutes,args.pbsname
curdir = os.getcwd()

assert wallminutes<=60 , " wallminutes should be less than 60"

if args.run==True:
	filename="pbs_%s_run.pbs" % pbsname
elif args.create==True:
	filename="pbs_%s_create.pbs" % pbsname
elif args.analyze==True:
	filename="pbs_%s_analyze.pbs" % pbsname
else:
	raise ValueError('no input name specified')


with open(curdir+"/"+filename, 'w') as f:
	f.write('#!/bin/bash\n\n')
	f.write('#PBS -S /bin/bash\n')
	f.write('#PBS -l pmem=%dmb\n' % memmory )
	f.write('#PBS -l nodes=%d:ppn=%d\n' %(nodes,procs))
	f.write('#PBS -l walltime=%d:%d:00\n' %(wallhours,wallminutes))
	f.write('#PBS -m bea\n')
	f.write('#PBS -M vasiliy.triandafilidi@gmail.com\n\n')
	f.write('cd $PBS_O_WORKDIR\n\n')

	if args.create==True:
		f.write('mkdir figures')
		f.write('mpirun lmp_openmpi -in in.kremer > log.kremer\n')
		f.write('bash create_addangle.sh\n')
		f.write('mv *.dcd ./figures/\n')
		f.write('mpirun lmp_openmpi -in in.nve > log.nve\n')
		f.write('mpirun lmp_openmpi -in in.npt > log.npt\n')
		
		f.write('rm tmp.*\n')
		f.write('rm *.pbs.*\n')
		f.write('mv *.data ./figures/\n')
		f.write('mv log.*	./figures/\n')
		f.write('mv *.chain ./figures/\n')

	elif args.run==True:
		f.write('mpirun lmp_openmpi -in in.lammps > log.lammps\n')
		f.write('rm tmp.*\n')
		f.write('rm *.pbs.*\n')
		f.write('mv *.data ./figures/\n')
		f.write('mv log.*	./figures/\n')
	elif args.analyze==True:
		f.write('cp ./figures/polymer_0.8.data ./figures/lammps.data \n')
		f.write('AnalyzeTrueg2.py simple -f %s \n' % pbsname)
	else:
		raise ValueError('no input name specified')

		
# if __name__ == '__main__':
# 	main()