#!/usr/bin/env python

import numpy as np 
import matplotlib.pyplot as plt 
import os
from itertools import cycle,izip
import read_parameters

def del_end(x):
    """
    delete npz dimension of the file
    """
    if x[-4:] == '.npz':
        return ''.join(x.split())[:-4]
    else:
        return x
def is_valid_file(parser, arg):
    """
    Check if arg is a valid file 
    """
    argpath = os.path.abspath(arg)
    if not os.path.exists(argpath):
        parser.error("The file %s doesn't exist " % argpath)
    else:
        return arg


def main():
    """
    get files, filenames(without .npz), name_x,name_y, titlename 
    list a long file of lines(which represent different styles)
    the same with colors
    then use the itertools and plot them, switch to different style by next()
    """
    results = read_parameters.read_plot()
    files, filenames, name_x, name_y, titlename, boxes, legend = results.files,results.filenames, \
                results.name_x, results.name_y , results.titlename,\
                results.boxes, results.legend
    filenames = [del_end(x) for x in files]

    # filled_markers = (u'o', u'v', u'^', u'<', u'>', u'8', u's', u'p', u'*', u'h', u'H', u'D', u'd')
    lines = [u'D', u'o', u'^', u'>', u's', u'8', u'<', u'>',  u'*',  u'H', u'h', u'p', u'v', u'D', u'd',"-","--","-.",":"]
    # colors=['k','y','m','c','b','g','r','#aaaaaa']
    colors=['m','c','b','g','m','k']

    linecycler = cycle(lines)
    colorcycler = cycle(colors)

    # colors=('k','y','m','c','b','g','r','#aaaaaa')
    # linestyles=('-','--','-.',':')
    # styles=[(color,linestyle) for linestyle in linestyles for color in colors]

    plt.figure()
    plt.ylabel('$\mathrm{crystallinity}$')
    plt.xlabel('$\mathrm{time,}$')


    plt.title('$\mathrm{alignement\ crystallinity\ parameter\ <cos(2\phi)>}$')

    # color=styles[num][0],ls=styles[num][1]
    place = 10
    yoffset = -0.03
    for (i,j) in izip(files,filenames):
        npz=np.load(i)
        t = npz[name_x]
        p = npz[name_y]
        # plt.plot(t,p,next(linecycler),label=i)
        clr=next(colorcycler)
        plt.plot(t,p,next(linecycler),color=clr,linewidth=1.2,label=j)
        bbox_props = dict(boxstyle="round", fc=clr, ec="0.01", alpha=0.2)
        # plt.text(t[-10]-10.0, p[-10]+0.03, j, ha="center", va="center",rotation=15, size=10, bbox=bbox_props)
        if boxes:
            plt.text(t[place], p[place]+yoffset, j, ha="center", va="center",rotation=15, size=10, bbox=bbox_props)
        place += 10
        if place>40:
            yoffset = 0.03
            place = 20
    plt.plot((0, t[-1]), (0.2, 0.2), 'k--', alpha=0.6)
    if legend:
        plt.legend(loc='lower right')
    plt.savefig(titlename+".pdf")
    # plt.show()


    # y_sol = 0.13
    # x_idx = find_nearest(p40,y_sol)
    # x_sol = t[x_idx]


if __name__ == '__main__':
    main()