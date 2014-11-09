# $Id: bucky.vmd,v 1.1 2004/05/14 18:30:42 akohlmey Exp $
set viewplist {}
# Display settings
display projection   Orthographic
display nearclip set 0.000000
display depthcue   off

# mol new {bucky.xyz} type xyz waitfor all 
# mol addfile {bucky.dcd} type dcd waitfor all

mol new {polymer.psf} type psf waitfor all
mol addfile {trajectory_newparam.xtc} type xtc waitfor all

animate goto 0
mol delrep 0 top
mol representation VDW 0.350000 30.000000
mol color User
mol selection {all}
mol material Opaque
mol addrep top
mol colupdate 0 top 1
mol scaleminmax top 0 3.38 3.69
mol representation DynamicBonds 1.600000 0.200000 19.000000
mol color ColorID 6
mol addrep top
mol rename top {Bucky Billard}

set n 403
set natoms 501
set left [atomselect top all]

set zaxis {0.13781049  0.93179896  0.33579603}
# set len 

for {set i 0} {$i < $n} {incr i} {
    $left frame $i
    set dlist ""
    lappend dlist 0.724144
    puts "this is the frame = $i"
     for {set j 1} {$j <= $natoms} {incr j} {
    	set e1 [expr $j-1]
    	set e2 [expr $j]
    	# puts "I am here1"
 
		set a1 [atomselect top "index $e1" frame $i]
		# puts "a1 = $a1"
		set a2 [atomselect top "index $e2" frame $i]
		set q1 [lindex [$a1 get { x y z } ] 0]
		set q2 [lindex [$a2 get { x y z } ] 0]
    	# puts "I am here2"

		set hd [vecsub $q1 $q2]
		# puts $hd
    	# puts "I am here3"
    	set lenbond  [veclength $hd]

		set cosine [expr [vecdot $hd $zaxis] / ( [veclength $hd] * [veclength $zaxis])]
		# set param [ expr -log($cosine*$cosine)]
		set param [expr 1.5*$cosine*$cosine - 0.5 ]
		# puts $cosine
        # puts "i am here 3"
        lappend dlist $cosine
    	# puts "I am here1"

    	# angle $q1 $q2 $q3 
    	$a1 delete
    	$a2 delete 
    	# $a3 delete

    }
    # puts $dlist 
    # lappend dlist 0.7241445078825316

	if {$i == 200} {
			puts $dlist
		}


    $left set user $dlist
}

  #  for {set j 1} {$j < 10} {incr j} {
  #   	set e1 [expr $j-1]
  #   	set e2 [expr $j]
  #   	set e3 [expr $j+1]
 
		# set a1 [atomselect top "index $e1" frame $i]
		# set a2 [atomselect top "index $e2" frame $i]
		# set a3 [atomselect top "index $e3" frame $i]
		# set q1 [lindex [$a1 get { x y z } ] 0]
		# set q2 [lindex [$a2 get { x y z } ] 0]
		# set q3 [lindex [$a3 get { x y z } ] 0]
		# set hd [vecsub $q1 $q2]
		# set ha [vecsub $q2 $q3]
		# set cosine [expr [vecdot $hd $ha] / ( [veclength $hd] * [veclength $ha])]
  #       lappend dlist [veclength [vecsub $c $com]]
  #   	# angle $q1 $q2 $q3 
  #   	$a1 delete
  #   	$a2 delete 
  #   	$a3 delete

  #   }

animate style rock
animate speed 0.8
animate forward