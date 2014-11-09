# $Id: bucky.vmd,v 1.1 2004/05/14 18:30:42 akohlmey Exp $
set viewplist {}
# Display settings
display projection   Orthographic
display nearclip set 0.000000
display depthcue   off
# mol delete top
# mol load pdb polymer.pdb
# mol addfile {trajectory_shortchain.xtc} type xtc waitfor all
# pbc unwrap
# mol new {bucky.xyz} type xyz waitfor all 
# mol addfile {bucky.dcd} type dcd waitfor all

# mol new {polymer.psf} type psf waitfor all
# mol addfile {trajectory_newparam.xtc} type xtc waitfor all

# set numframes [molinfo top get numframes]
# set numatoms [molinfo top get numatoms]

# set na [expr $numatoms - 2]
set sel [atomselect top "all"]
# set selb [atomselect top "index > 1 and index < $na"]
# set seldebug [atomselect top "index > 0 and index < 10"]

# puts "num atoms = $numatoms"

animate goto 0
mol delrep 0 top
# mol representation VDW 0.350000 30.000000
mol representation Lines 1.5
mol color User
mol selection {all}
mol material Opaque
mol addrep top
mol colupdate 0 top 1
mol scaleminmax top 0 auto
 #0.0 1.0
# mol representation DynamicBonds 1.400000 0.600000 19.000000
# mol color ColorID 1
# mol addrep top
# mol rename top {Bucky Billard}

puts "here1 "

# set dlist ""
set cl 20 
set nmol 110
puts "here2 "

# for {set iframe 0} {$iframe < 2500} {incr iframe 100} {
	set iframe 0
	remove_long_bonds 5

	$sel frame $iframe
	set dlist ""
	for {set imol 0} {$imol < $nmol} {incr imol} {

		# dlist append "cos"  # appending for the first atom c1
		lappend dlist "1.5"
		# puts "imol = $imol"
		for {set i 0} {$i < $cl - 3} {incr i} {
			set j [expr $imol*$cl + $i]
			set c1 [expr $j]
			set c2 [expr $j+1]
			set c3 [expr $j+2]
			set c4 [expr $j+3]
			set ang [measure dihed [list $c1 $c2 $c3 $c4] frame $iframe]
			set cosine [expr abs($ang) / 180.]
			# puts "i am here"
			# set cosine [expr cos(3.1459 * $ang / 180.0)*cos(3.1459 * $ang / 180.0) ]

			# cos = measure dihedral $c1 $c2 $c3 $c4
			# dlist append "cos" 	# appendng for the second atom c2
			lappend dlist $cosine


		}	
		puts "imol = $imol, cosine  = $cosine"

		# dlist append "something" #appending for the atom $c3
		# dlist append "something" #appending for the atom $c4
		lappend dlist "1.5"
		lappend dlist "1.5"

	}

	$sel set user $dlist
	$sel writepdb cryst_$i.pdb
	
# }




# animate style rock
# animate speed 0.8
# animate forward