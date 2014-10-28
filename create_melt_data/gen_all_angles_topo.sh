#!/bin/sh


if [ "$#" != "2" ]; then
  echo "Error: two arguments are needed:  input_DATA_file  output_DATA_file" >&2
  exit 1
fi


# Extract the sections we need from the data file
extract_lammps_data.py Header < "$1" > tmp_data_header
extract_lammps_data.py -n Header < "$1" > tmp_data_remaining
extract_lammps_data.py Atoms < "$1" > tmp_data_atoms
extract_lammps_data.py Bonds < "$1" > tmp_data_bonds
#rm -f tmp_data_remaining
#cp -f "$1" tmp_data_remaining
rm -f "$2"


# Get rid of the sections we are going to replace.
# Save what remains in "tmp_data_remaining", and send this text to "$2"
if [ -s "angles_by_type.txt" ]; then
    extract_lammps_data.py -n Angles < tmp_data_remaining > tmp_data_remaining.tmp
    mv -f tmp_data_remaining.tmp tmp_data_remaining
fi

if [ -s "dihedrals_by_type.txt" ]; then
    extract_lammps_data.py -n Dihedrals < tmp_data_remaining > tmp_data_remaining.tmp
    mv -f tmp_data_remaining.tmp tmp_data_remaining
fi

if [ -s "impropers_by_type.txt" ]; then
    extract_lammps_data.py -n Impropers < tmp_data_remaining > tmp_data_remaining.tmp
    mv -f tmp_data_remaining.tmp tmp_data_remaining
fi

if [ -s "angles_by_type.txt" ]; then
    nbody_by_type.py Angles -atoms tmp_data_atoms -bonds tmp_data_bonds \
                      -nbodybytype angles_by_type.txt > tmp_data_angles

    #Optional: Next line removes duplicate interactions between same 3 atoms
    remove_duplicates_nbody.py 3 < tmp_data_angles > tmp_final_angles
    #Replace the number of angles in the header with the new number
    NANGLES=`awk 'END{print NR}' < tmp_final_angles`
    awk "BEGIN{found=0} {if ((NF >= 2) && (\$2 == \"angles\")) {found=1; printf(\"     %s  %s\n\",$NANGLES,\$2)} else print \$0} END{if (! found) {printf(\"     %s  angles\n\",$NANGLES)}}" < tmp_data_header > tmp_data_header.tmp
    mv -f tmp_data_header.tmp tmp_data_header
fi

if [ -s "dihedrals_by_type.txt" ]; then
    nbody_by_type.py Dihedrals -atoms tmp_data_atoms -bonds tmp_data_bonds \
                      -nbodybytype dihedrals_by_type.txt > tmp_data_dihedrals

    #Optional: Next line removes duplicate interactions between same 4 atoms
    remove_duplicates_nbody.py 4 < tmp_data_dihedrals > tmp_final_dihedrals
    #Replace the number of dihedrals in the header with the new number
    NDIHEDRALS=`awk 'END{print NR}' < tmp_final_dihedrals`
    awk "BEGIN{found=0} {if ((NF >= 2) && (\$2 == \"dihedrals\")) {found=1; printf(\"     %s  %s\n\",$NDIHEDRALS,\$2)} else print \$0} END{if (! found) {printf(\"     %s  dihedrals\n\",$NDIHEDRALS)}}" < tmp_data_header > tmp_data_header.tmp
    mv -f tmp_data_header.tmp tmp_data_header
fi

if [ -s "impropers_by_type.txt" ]; then
    nbody_by_type.py Impropers -atoms tmp_data_atoms -bonds tmp_data_bonds \
                      -nbodybytype impropers_by_type.txt > tmp_data_impropers
    #Optional: Next line removes duplicate interactions between same 4 atoms
    remove_duplicates_nbody.py 4 < tmp_data_impropers > tmp_final_impropers
    #Replace the number of impropers in the header with the new number
    NIMPROPERS=`awk 'END{print NR}' < tmp_final_impropers`
    awk "BEGIN{found=0} {if ((NF >= 2) && (\$2 == \"impropers\")) {found=1; printf(\"     %s  %s\n\",$NIMPROPERS,\$2)} else print \$0} END{if (! found) {printf(\"     %s  impropers\n\",$NIMPROPERS)}}" < tmp_data_header > tmp_data_header.tmp
    mv -f tmp_data_header.tmp tmp_data_header
fi

# Send the remaining sections of the data file to "$2"
cat tmp_data_header > "$2"
echo "" >> "$2"
cat tmp_data_remaining >> "$2"
rm -f tmp_data_header tmp_data_remaining

if [ -s "angles_by_type.txt" ]; then
    echo "" >> "$2"
    echo "Angles" >> "$2"
    echo "" >> "$2"
    cat tmp_final_angles >> "$2"
    rm -f tmp_final_angles tmp_data_angles
fi

if [ -s "dihedrals_by_type.txt" ]; then
    echo "" >> "$2"
    echo "Dihedrals" >> "$2"
    echo "" >> "$2"
    cat tmp_final_dihedrals >> "$2"
    rm -f tmp_final_dihedrals tmp_data_dihedrals
fi

if [ -s "impropers_by_type.txt" ]; then
    echo "" >> "$2"
    echo "Impropers" >> "$2"
    echo "" >> "$2"
    cat tmp_final_impropers >> "$2"
    rm -f tmp_final_impropers tmp_data_impropers
fi

rm -f tmp_data_atoms tmp_data_bonds

