# compare effect of fictitious mass on fictitious vibronic DOS in CP dynamics
    package require specden
    package require multiplot

    set fp [open "ENERGIES-cp-200au" "r"]
    set dlist {}
    while { [gets $fp dat] >= 0 } {
        lappend dlist [list [lindex $dat 1] 0.0 0.0]
    }
    close $fp
    lassign [specden $dlist 4.0 20000.0] flist slist
    set ph [multiplot -x $flist -y $slist -title "EKINC Power Spectrum" -lines -linewidth 3 -marker points -plot]

    set fp [open "ENERGIES-cp-400au" "r"]
    set dlist {}
    while { [gets $fp dat] >= 0 } {
        lappend dlist [list [lindex $dat 1] 0.0 0.0]
    }
    lassign [specden $dlist 4.0 20000.0] flist slist
    close $fp
    $ph add $flist $slist -lines -linecolor red -linewidth 3 -plot 