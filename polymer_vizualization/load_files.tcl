# mol new new.psf type psf first 0 last -1 step 1 filebonds 1 autobonds 1 waitfor all
# mol addfile some.pdb type pdb first 0 last -1 step 1 filebonds 1 autobonds 1 waitfor all

color Display Background white
display render mode GLSL
color change rgb 0 0.7699999809265137 1.0 1.0


display eyesep       0.020000
display focallength  2.000000
display height       6.000000
display distance     -1.900000
display projection   Perspective
display nearclip set 0.001000
display farclip  set 10.000000
display depthcue   on
display cuestart   0.500000
display cueend     10.000000
display cuedensity 0.320000
display cuemode    Exp2


mol representation Bonds 0.1 50.0 
mol selection beta > 0.3
mol color ResID
material add copy Transparent
material change ambient Material122 0.0
material change diffuse Material122 1.0
material change specular Material122 0.16
material change shiness Material122 0.63
material change opacity Material122 0.45
material change outline Material122 4.0
material change outwidth Material122 1.0
mol material Material122

mol addrep 0
mol color Molecule
mol modselect 1 0 all
mol modstyle 1 0 Solvent 0.2 13.0 3.0
mod material 2 0 Transparent

menu render on