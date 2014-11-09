set cl 20 

for {set imol 0} {$imol < $nmol} {incr imol} {
	for {set i 0} {$i < $n - 2} {incr i} {
		set j [expr $imol*$cl + $i]
		set c1 [expr $i]
		set c2 [expr $i+1]
		set c3 [expr $i+2]
		set c4 [expr $i+3]
		cos = measure dihedral $c1 $c2 $c3 $c4
		dlist append "cos"  # appending for the first atom c1
		dlist append "cos" 	# appendng for the second atom c2
	}	
	dlist append "something" #appending for the atom $c3
	dlist append "something" #appending for the atom $c4

}
