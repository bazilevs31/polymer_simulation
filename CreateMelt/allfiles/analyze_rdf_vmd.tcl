set psf kffedimer-wb.psf
set dcd T1.dcd
mol load psf $psf dcd $dcd
set outfile1 [open gdr-OH-50.dat w]
set sel1 [atomselect top "name OH2 and water and same residue as within 5.0 of protein"]
set sel2 [atomselect top "{name H1 or name H2} and water and same residue as within 5.0 of protein"]     
set gr0 [measure gofr $sel1 $sel2 delta 0.1 rmax 10.0 usepbc 1
selupdate 1 first 0 last -1 step 1]
set r [lindex $gr0 0]
set gr [lindex $gr0 1]
set igr [lindex $gr0 2]
set isto [lindex $gr0 3]
foreach j $r k $gr l $igr m $isto {
  puts $outfile1 [format "%.4f\t%.4f\t%.4f\t%.4f" $j $k $l $m]
}
close $outfile1
exit 
