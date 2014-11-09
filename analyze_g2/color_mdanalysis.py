import MDAnalysis
from MDAnalysis import *
import numpy as np
# u = Universe("polymer.psf", "trajectory_newparam.xtc")
u = Universe("poly_without_long.psf", "trajectory_shortchain.xtc")
C = '1'

t_types = {
'phi': (C,C,C,C),
}

u.trajectory[1500]
dihedrals = dict((name, u.atoms.selectBonds(torsion)) for name,torsion in t_types.items())

# just look at phi to keep the example simple
phis = dihedrals['phi']

print list(phis)   # show the phi dihedrals

# short cut to all angles (use periodic boundary conditions 
#in case you didn't center or if your polymer crosses 
# boundaries)
# phis_degrees = np.rad2deg(phis.torsions())
phis_rad = phis.torsions(pbc=True)

#---

# You now have a list of all dihedrals in phis_degrees (in degrees).

# > and changing the charge of the particles according to the dihedral angle of the atoms involved?
CA_atoms = phis.atom3
CA_atoms.set_bfactor(phis_rad)
CA_atoms.set_name("my")
#----

CA_atoms.write("polymer_shortchain_liq.pdb")

# Then write out your file. (By the way, I would use set_bfactor() and write data into the temperatureFactor in a PDB file.)

# Hope that does want you want it to do.

# Oliver7