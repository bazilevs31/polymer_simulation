#!/usr/local/bin/vmd
# VMD script written by save_state $Revision: 1.44 $
# VMD version: 1.9.1
mol new new.psf type psf first 0 last -1 step 1 filebonds 1 autobonds 1 waitfor all
mol addfile some.pdb type pdb first 0 last -1 step 1 filebonds 1 autobonds 1 waitfor all


set viewplist {}
set fixedlist {}

material add copy Transparent
material rename Material22 Polybonds

  material change ambient Transparent 0.000000
  material change diffuse Transparent 0.650000
  material change specular Transparent 0.500000
  material change shininess Transparent 0.534020
  material change opacity Transparent 0.300000
  material change outline Transparent 0.000000
  material change outlinewidth Transparent 0.000000
  material change transmode Transparent 0.000000
  material change ambient Polybonds 0.000000
  material change diffuse Polybonds 1.000000
  material change specular Polybonds 0.250000
  material change shininess Polybonds 0.630000
  material change opacity Polybonds 0.310000
  material change outline Polybonds 4.000000
  material change outlinewidth Polybonds 1.000000
  material change transmode Polybonds 0.000000

# Display settings
display eyesep       0.065000
display focallength  2.000000
display height       6.000000
display distance     -2.000000
display projection   Perspective
display nearclip set 0.001000
display farclip  set 10.000000
display depthcue   on
display cuestart   0.500000
display cueend     10.000000
display cuedensity 0.320000
display cuemode    Exp2
display rendermode GLSL
color Display Background white
color Molecule 0 blue

mol representation Solvent 0.200000 13.000000 3.000000
mol color Molecule
color Molecule 0 blue
color change rgb 0 0.700000 1.000000 1.000000

mol selection {all}
mol material Transparent
mol addrep top
mol selupdate 0 top 0
mol colupdate 0 top 0
mol scaleminmax top 0 0.000000 0.000000
mol smoothrep top 0 0
# mol drawframes top 0 {now}
# mol clipplane center 0 0 top {0.0 0.0 0.0}
# mol clipplane color  0 0 top {0.5 0.5 0.5 }
# mol clipplane normal 0 0 top {0.0 0.0 1.0}
# mol clipplane status 0 0 top {0}
# mol clipplane center 1 0 top {0.0 0.0 0.0}
# mol clipplane color  1 0 top {0.5 0.5 0.5 }
# mol clipplane normal 1 0 top {0.0 0.0 1.0}
# mol clipplane status 1 0 top {0}
# mol clipplane center 2 0 top {0.0 0.0 0.0}
# mol clipplane color  2 0 top {0.5 0.5 0.5 }
# mol clipplane normal 2 0 top {0.0 0.0 1.0}
# mol clipplane status 2 0 top {0}
# mol clipplane center 3 0 top {0.0 0.0 0.0}
# mol clipplane color  3 0 top {0.5 0.5 0.5 }
# mol clipplane normal 3 0 top {0.0 0.0 1.0}
# mol clipplane status 3 0 top {0}
# mol clipplane center 4 0 top {0.0 0.0 0.0}
# mol clipplane color  4 0 top {0.5 0.5 0.5 }
# mol clipplane normal 4 0 top {0.0 0.0 1.0}
# mol clipplane status 4 0 top {0}
# mol clipplane center 5 0 top {0.0 0.0 0.0}
# mol clipplane color  5 0 top {0.5 0.5 0.5 }
# mol clipplane normal 5 0 top {0.0 0.0 1.0}
# mol clipplane status 5 0 top {0}

mol representation Bonds 0.100000 50.000000
mol color ResID
mol selection {beta > 0.3}
mol material Polybonds
mol addrep top
mol selupdate 1 top 0
mol colupdate 1 top 0
mol scaleminmax top 1 0.000000 0.000000
mol smoothrep top 1 0
# mol drawframes top 1 {now}
# mol clipplane center 0 1 top {0.0 0.0 0.0}
# mol clipplane color  0 1 top {0.5 0.5 0.5 }
# mol clipplane normal 0 1 top {0.0 0.0 1.0}
# mol clipplane status 0 1 top {0}
# mol clipplane center 1 1 top {0.0 0.0 0.0}
# mol clipplane color  1 1 top {0.5 0.5 0.5 }
# mol clipplane normal 1 1 top {0.0 0.0 1.0}
# mol clipplane status 1 1 top {0}
# mol clipplane center 2 1 top {0.0 0.0 0.0}
# mol clipplane color  2 1 top {0.5 0.5 0.5 }
# mol clipplane normal 2 1 top {0.0 0.0 1.0}
# mol clipplane status 2 1 top {0}
# mol clipplane center 3 1 top {0.0 0.0 0.0}
# mol clipplane color  3 1 top {0.5 0.5 0.5 }
# mol clipplane normal 3 1 top {0.0 0.0 1.0}
# mol clipplane status 3 1 top {0}
# mol clipplane center 4 1 top {0.0 0.0 0.0}
# mol clipplane color  4 1 top {0.5 0.5 0.5 }
# mol clipplane normal 4 1 top {0.0 0.0 1.0}
# mol clipplane status 4 1 top {0}
# mol clipplane center 5 1 top {0.0 0.0 0.0}
# mol clipplane color  5 1 top {0.5 0.5 0.5 }
# mol clipplane normal 5 1 top {0.0 0.0 1.0}
# mol clipplane status 5 1 top {0}

mol delrep 0 0

set viewpoints([molinfo top]) {{{1 0 0 -8.78482} {0 1 0 -8.66811} {0 0 1 -8.7387} {0 0 0 1}} {{-0.729819 0.00241407 -0.683636 0} {-0.0540828 0.996655 0.0612555 0} {0.681497 0.0816785 -0.727247 0} {0 0 0 1}} {{0.0497116 0 0 0} {0 0.0497116 0 0} {0 0 0.0497116 0} {0 0 0 1}} {{1 0 0 0} {0 1 0 0} {0 0 1 0} {0 0 0 1}}}
lappend viewplist [molinfo top]
set topmol [molinfo top]
# done with molecule 0
mol top $topmol
unset topmol

