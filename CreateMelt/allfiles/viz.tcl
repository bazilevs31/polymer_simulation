
$sel set beta $mass
set sel [atomselect molid “selection text”]
residue 5
set firstRes 0
set lastRes 10
for {set r $firstRes} {$r <= $lastRes} {incr r} {
    set sela [atomselect $molid "resid $r"]
    set selb [atomselect $molid "resid $r"]
    $sela frame 0
    for {set f $firstFrame} {$f<=$lastFrame} {incr f} {
      $selb frame $f
      display update
      set val [measure rmsd $sela $selb]
      set resid $r
      puts $outDataFile "$resid $chain $seg $f $val"
    }
}