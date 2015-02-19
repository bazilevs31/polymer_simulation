#!/home/vasiliy/anaconda/bin/python

import numpy as np


def append_arrays(bigarray,smallarray):
	"""
	append a smallarray to a bigarray
	"""
	bigarray.append(smallarray)
	return None

def save_arrays(bigarray,name):
	"""
	save bigarray with a given name using npz compression
	
	smallarray=np.array([7,8,9])
	mainArray = [np.array([1,2,3]), np.array([4,5,6])]
	append_arrays(mainArray,smallarray)
	save_arrays(mainArray,'myfile')

	In [25]: npz = np.load('myfile.npz')
	In [26]: npz.items()
	Out[26]: 
	[('arr_1', array([4, 5, 6])),
	 ('arr_0', array([1, 2, 3])),
	 ('arr_2', array([7, 8, 9]))]
	"""
	N = len(bigarray)
	np.savez(name, *[bigarray[i] for i in range(N)])
	
def main():
	"""
	test run 
	"""
	smallarray=np.arange(100)
	mainArray = []

	append_arrays(mainArray,smallarray)
	append_arrays(mainArray,2*smallarray)
	append_arrays(mainArray,3*smallarray)
	append_arrays(mainArray,4*smallarray)
	append_arrays(mainArray,5*smallarray)
	append_arrays(mainArray,6*smallarray)
	save_arrays(mainArray,'myfile')

if __name__ == '__main__':
	main()