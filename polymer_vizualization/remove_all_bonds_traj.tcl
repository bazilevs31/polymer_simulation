set sel [atomselect top "all"]
set n [molinfo top get numframes]
for {set i 0} {$i < $n} {incr i} {
	puts "here is the frame  = $i"
	$sel frame $i
	remove_long_bonds 5
}