Fourier transforms
==================

Functions related to Fourier transforms can be called by importing the
``fft`` sub-module first.

``numpy``:
https://docs.scipy.org/doc/numpy/reference/generated/numpy.fft.ifft.html

fft
---

Since ``ulab``\ ’s ``ndarray`` does not support complex numbers, the
invocation of the Fourier transform differs from that in ``numpy``. In
``numpy``, you can simply pass an array or iterable to the function, and
it will be treated as a complex array:

.. code::

    # code to be run in CPython
    
    fft.fft([1, 2, 3, 4, 1, 2, 3, 4])



.. parsed-literal::

    array([20.+0.j,  0.+0.j, -4.+4.j,  0.+0.j, -4.+0.j,  0.+0.j, -4.-4.j,
            0.+0.j])



**WARNING:** The array that is returned is also complex, i.e., the real
and imaginary components are cast together. In ``ulab``, the real and
imaginary parts are treated separately: you have to pass two
``ndarray``\ s to the function, although, the second argument is
optional, in which case the imaginary part is assumed to be zero.

**WARNING:** The function, as opposed to ``numpy``, returns a 2-tuple,
whose elements are two ``ndarray``\ s, holding the real and imaginary
parts of the transform separately.

.. code::
        
    # code to be run in micropython
    
    import ulab as np
    from ulab import vector
    from ulab import fft
    
    x = np.linspace(0, 10, num=1024)
    y = vector.sin(x)
    z = np.zeros(len(x))
    
    a, b = fft.fft(x)
    print('real part:\t', a)
    print('\nimaginary part:\t', b)
    
    c, d = fft.fft(x, z)
    print('\nreal part:\t', c)
    print('\nimaginary part:\t', d)

.. parsed-literal::

    real part:	 array([5119.996, -5.004663, -5.004798, ..., -5.005482, -5.005643, -5.006577], dtype=float)
    
    imaginary part:	 array([0.0, 1631.333, 815.659, ..., -543.764, -815.6588, -1631.333], dtype=float)
    
    real part:	 array([5119.996, -5.004663, -5.004798, ..., -5.005482, -5.005643, -5.006577], dtype=float)
    
    imaginary part:	 array([0.0, 1631.333, 815.659, ..., -543.764, -815.6588, -1631.333], dtype=float)
    


ifft
----

The above-mentioned rules apply to the inverse Fourier transform. The
inverse is also normalised by ``N``, the number of elements, as is
customary in ``numpy``. With the normalisation, we can ascertain that
the inverse of the transform is equal to the original array.

.. code::
        
    # code to be run in micropython
    
    import ulab as np
    from ulab import vector
    from ulab import fft
    
    x = np.linspace(0, 10, num=1024)
    y = vector.sin(x)
    
    a, b = fft.fft(y)
    
    print('original vector:\t', y)
    
    y, z = fft.ifft(a, b)
    # the real part should be equal to y
    print('\nreal part of inverse:\t', y)
    # the imaginary part should be equal to zero
    print('\nimaginary part of inverse:\t', z)

.. parsed-literal::

    original vector:	 array([0.0, 0.009775016, 0.0195491, ..., -0.5275068, -0.5357859, -0.5440139], dtype=float)
    
    real part of inverse:	 array([-2.980232e-08, 0.0097754, 0.0195494, ..., -0.5275064, -0.5357857, -0.5440133], dtype=float)
    
    imaginary part of inverse:	 array([-2.980232e-08, -1.451171e-07, 3.693752e-08, ..., 6.44871e-08, 9.34986e-08, 2.18336e-07], dtype=float)
    


Note that unlike in ``numpy``, the length of the array on which the
Fourier transform is carried out must be a power of 2. If this is not
the case, the function raises a ``ValueError`` exception.

spectrogram
-----------

In addition to the Fourier transform and its inverse, ``ulab`` also
sports a function called ``spectrogram``, which returns the absolute
value of the Fourier transform. This could be used to find the dominant
spectral component in a time series. The arguments are treated in the
same way as in ``fft``, and ``ifft``.

.. code::
        
    # code to be run in micropython
    
    import ulab as np
    from ulab import vector
    from ulab import fft
    
    x = np.linspace(0, 10, num=1024)
    y = vector.sin(x)
    
    a = fft.spectrogram(y)
    
    print('original vector:\t', y)
    print('\nspectrum:\t', a)

.. parsed-literal::

    original vector:	 array([0.0, 0.009775015390171337, 0.01954909674625918, ..., -0.5275140569487312, -0.5357931822978732, -0.5440211108893639], dtype=float)
    
    spectrum:	 array([187.8635087634579, 315.3112063607119, 347.8814873399374, ..., 84.45888934298905, 347.8814873399374, 315.3112063607118], dtype=float)
    
    


As such, ``spectrogram`` is really just a shorthand for
``np.sqrt(a*a + b*b)``:

.. code::
        
    # code to be run in micropython
    
    import ulab as np
    from ulab import fft
    from ulab import vector
    
    x = np.linspace(0, 10, num=1024)
    y = vector.sin(x)
    
    a, b = fft.fft(y)
    
    print('\nspectrum calculated the hard way:\t', vector.sqrt(a*a + b*b))
    
    a = fft.spectrogram(y)
    
    print('\nspectrum calculated the lazy way:\t', a)

.. parsed-literal::

    
    spectrum calculated the hard way:	 array([187.8641, 315.3125, 347.8804, ..., 84.4587, 347.8803, 315.3124], dtype=float)
    
    spectrum calculated the lazy way:	 array([187.8641, 315.3125, 347.8804, ..., 84.4587, 347.8803, 315.3124], dtype=float)
    


Computation and storage costs
-----------------------------

RAM
~~~

The FFT routine of ``ulab`` calculates the transform in place. This
means that beyond reserving space for the two ``ndarray``\ s that will
be returned (the computation uses these two as intermediate storage
space), only a handful of temporary variables, all floats or 32-bit
integers, are required.

Speed of FFTs
~~~~~~~~~~~~~

A comment on the speed: a 1024-point transform implemented in python
would cost around 90 ms, and 13 ms in assembly, if the code runs on the
pyboard, v.1.1. You can gain a factor of four by moving to the D series
https://github.com/peterhinch/micropython-fourier/blob/master/README.md#8-performance.

.. code::
        
    # code to be run in micropython
    
    import ulab as np
    from ulab import vector
    from ulab import fft
    
    x = np.linspace(0, 10, num=1024)
    y = vector.sin(x)
    
    @timeit
    def np_fft(y):
        return fft.fft(y)
    
    a, b = np_fft(y)

.. parsed-literal::

    execution time:  1985  us
    


The C implementation runs in less than 2 ms on the pyboard (we have just
measured that), and has been reported to run in under 0.8 ms on the D
series board. That is an improvement of at least a factor of four.
