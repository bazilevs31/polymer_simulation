#!/usr/bin/env python
import os
import read_parameters


# def main():
print "I am doing reading paramters"
args = read_parameters.read_pbs()
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
        f.write('mv log.*   ./figures/\n')
        f.write('mv *.chain ./figures/\n')
        f.write('AnalyzeLog.py')
    elif args.run==True:
        f.write('mpirun lmp_openmpi -in in.lammps > log.lammps\n')
        f.write('rm tmp.*\n')
        f.write('rm *.pbs.*\n')
        f.write('mv *.data ./figures/\n')
        f.write('mv log.*   ./figures/\n')
    elif args.analyze==True:
        f.write('cp ./figures/polymer_0.8.data ./figures/lammps.data \n')
        f.write('AnalyzeTrueg2.py simple -f %s \n' % pbsname)
    else:
        raise ValueError('no input name specified')

        
# if __name__ == '__main__':
#   main()