import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import timeit

clock = timeit.default_timer

fig, ax = plt.subplots()

alphab = ['A', 'B', 'C', 'D', 'E', 'F']
frequencies = [1, 44, 12, 11, 2, 10]

pos = np.arange(len(alphab))
width = 1.0     # gives histogram aspect to the bar diagram
ax.set_xticks(pos + (width / 2))
ax.set_xticklabels(alphab)

rects = plt.bar(pos, frequencies, width, color='r')
start = clock()

def animate(arg, rects):
    frameno, frequencies = arg
    for rect, f in zip(rects, frequencies):
        rect.set_height(f)
    print("FPS: {:.2f}".format(frameno / (clock() - start))) 

def step():
    for frame, bin_idx in enumerate(np.linspace(0,1000000,100000000), 1):
        #Here we just change the first bin, so it increases through the animation.
        frequencies[0] = bin_idx
        yield frame, frequencies


ani = animation.FuncAnimation(fig, animate, step, interval=10,
                              repeat=False, blit=False, fargs=(rects,))
plt.show()