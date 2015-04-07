#!/usr/bin/env python
"""
An animated image
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import types 
fig = plt.figure()

# def f(x, y)
#     return np.sin(x) + np.cos(y)

x = np.linspace(0, 2 * np.pi, 120)
# y = np.linspace(0, 2 * np.pi, 100).reshape(-1, 1)
# ims is a list of lists, each row is a list of artists to draw in the
# current frame; here we are just animating one artist, the image, in
# each frame
ims = []
for i in range(60):
    x += np.pi / 15.
    # y += np.pi / 20.
    im = plt.plot(x,np.sin(i*x))
    def setvisible(self,vis): 
       for c in self.collections: c.set_visible(vis) 
    im.set_visible = types.MethodType(setvisible,im,None) 
    im.axes = plt.gca() 
    ims.append([im])

ani = animation.ArtistAnimation(fig, ims, interval=50, blit=True,
    repeat_delay=1000)

#ani.save('dynamic_images.mp4')


plt.show()