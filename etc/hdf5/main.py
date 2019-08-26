import h5py
import numpy as np

with h5py.File('sample.h5', 'w') as f:
    a = np.array([[11,12], [13,14]])
    f.create_dataset('test', data=a)



f = h5py.File('sample.h5', 'r')

f.keys()
dset = f['test']

print(dset.shape)
print(dset.dtype)
print(dset[0][0])
print(dset[0][1])
print(dset.name)
