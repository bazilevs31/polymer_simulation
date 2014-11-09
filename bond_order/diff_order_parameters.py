#!/usr/bin/env python
# Example script, part of MDAnalysis
"""
Calculates order parameters for a dictionary of bonds provided.

What this script does?
Take the pair of atoms connected by bonds (e.g. NC3-PO4) for all molecules in
the system. Calculate the vector connecting the two and the cos^2 of the angle
between the vector and Z-axis. Average all the bonds for a given snapshot.
Then repeat for all frames. Average the result for all frames.

Optional output 'graph.xvg' that can be used eg by g_analyze (from GROMACS)
to perform block averaging.

:Author: Jan Domanski
:Year: 2010
:Copyright: GNU Public License v3

"""

from MDAnalysis import *
from pylab import *
import numpy
import math

conf = "conf.gro"
traj = "traj.xtc"
skip = 0 # skip frames

"""
Name of the lipid and definition of bonds to be used
"""
resname = ""
bond_list = {}


def main():
    dupc_bond_list = {
    1: ["NC3", "PO4"], 2: ["PO4", "GL1"],
    3: ["GL1", "GL2"], 4: ["GL2", "C1B"],
    5: ["C1B", "D2B"], 6: ["D2B", "D3B"],
    7: ["D3B", "C4B"],
    8: ["GL1", "C1A"],
    9: ["C1A", "D2A"], 10: ["D2A", "D3A"],
    11: ["D3A", "C4A"],
    }

    dppc_bond_list = {
    1: ["NC3", "PO4"], 2: ["PO4", "GL1"],
    3: ["GL1", "GL2"], 4: ["GL2", "C1B"],
    5: ["C1B", "C2B"], 6: ["C2B", "C3B"],
    7: ["C3B", "C4B"],
    8: ["GL1", "C1A"],
    9: ["C1A", "C2A"], 10: ["C2A", "C3A"],
    11: ["C3A", "C4A"],
    }
   
    u = Universe(conf, traj)
    
    p2_dictionary, p2_table = calculate_P2(u, bond_list, resname, skip)
    
    plot_x, plot_y = [], []
    
    for bond_id, p2_list in p2_dictionary.items():
        p2 = numpy.average(p2_list)
        print "For bond %d, secondary order parameter P2 is %f" % (bond_id, p2)
        plot_x.append(bond_id)
        plot_y.append(p2)
        
    return x, y, average_list
    
    # average out the P2 values for two tails
    plot_x, plot_y = average_tails(plot_x, plot_y)

    store_graph(p2_table).replace(',',"\t")
    

def calculate_P2(u, bond_list, resname, skip):
    """
This function calculates P2 order parameters for a given residue and bonds
within it.
Returns:
(1) dictionary {bond-id: list-p2}, to use in processing/plots
(2) list [time, p2-for-bond-1, p2-for-bond-2, ...] to save in graph.xvg
"""
    #
    bond_p2_dictionary = {}

    # list
    table = []
        
    for ts in u.trajectory:
        if not ts.frame % skip == 0 and ts.frame != 1 : continue
        print "Stepping... Frame %d, time %d ns" % (ts.frame, ts.time/1000)
        
        row = []

        row.append(ts.time)

        for i, bond in bond_list.items():
            atom_group_a = u.selectAtoms("resname %s and (name %s)" % (resname, bond[0]))
            atom_group_b = u.selectAtoms("resname %s and (name %s)" % (resname, bond[1]))
            
            # calculate p2 for a bond at the given frame
            cos_2_list = order_for_bond(atom_group_a, atom_group_b)
            average_cos_theta = numpy.average(cos_2_list)
            p2 = 0.5 * (3 * average_cos_theta - 1)
            row.append(p2)
            
            # add p2 value to the dictionary
            if not bond_p2_dictionary.has_key(i): bond_p2_dictionary[i] = []
            bond_p2_dictionary[i].append(p2)
            
        table.append(row)
    return bond_p2_dictionary, table

def order_for_bond(atom_group_a, atom_group_b):
    l = len(atom_group_a)
    angle_list = []
    for i in numpy.arange(l):
        
        atom_a = atom_group_a[i]
        atom_b = atom_group_b[i]
        
        cos_theta = cos_to_z(atom_a.pos, atom_b.pos) # in degrees
        
        cos_theta_2 = numpy.power(cos_theta, 2)
        angle_list.append(cos_theta_2)
        
    return angle_list

def cos_to_z(position_a, position_b):
    z = [0, 0, 1]
    v = abs(numpy.array(position_a - position_b))
    a = angle(v, z) # take abs, since chol can be in one of two leaflets
    return a

def angle(v1, v2):
    c = numpy.dot(v1,v2) / numpy.linalg.norm(v1) / numpy.linalg.norm(v2)
    #angle_radians = numpy.arccos(c) # if you really want the angle
    return c #math.degrees(angle_radians)

def average_tails(x_o, y_o):
    """
Additional data processing function
"""
    x = x_o[:]
    y = y_o[:]
    
    for i in numpy.arange(3,7):
        y_new = numpy.average([y[i], y[i+4]])
        y[i] = y_new
        
    del x[7:]
    del y[7:]
        
    return x, y

def store_graph(average_list, filename="graph.xvg"):
    store = open(filename, 'a')
    
    for average in average_list:
        store.write('%s \n' % str(average)[1:-1].replace(',','\t'))
    store.write('& \n')

def plot(x,y1,y2, y3):
    fig = figure()
    ax = fig.add_subplot(111)
    l1 = ax.plot(x, y1,'gx-', linewidth = 3, markersize = 10)
    l2 = ax.plot(x, y2, 'rx-', linewidth = 3, markersize = 10)
    l3 = ax.plot(x, y3, 'yx-', linewidth = 3, markersize = 10)
    legend( (l1, l2, l3), ('DPPC', 'DUPC', 'DUPC+protein'), 'upper left', shadow=True)
    ylabel("P2 order parameter")
    xlabel("Bond number")
    show()

if __name__ == "__main__":
    main()