PyTSP
=====

[![Build Status](https://travis-ci.org/jvkersch/pytsp.svg?branch=master)](https://travis-ci.org/jvkersch/pytsp)

What is it?
-----

PyTSP is a Python wrapper around the [Concorde TSP solver](http://www.math.uwaterloo.ca/tsp/concorde.html).

PyTSP allows you to compute solutions to the Traveling Salesman Problem with just a few lines of Python code. It uses the state-of-the-art Concorde solver and provides a convenient Python layer around it.

<p align="center">
  <a href="examples/us_state_capitals.py">
	<img src="examples/us_state_capitals.png" alt="US state capital tour"/>
	</a>
</p>

How do I install it?
------

PyTSP runs under Python 2.7 and 3.4 and up. It needs the [Concorde TSP solver](http://www.math.uwaterloo.ca/tsp/concorde.html) and [QSOpt linear programming library](http://www.math.uwaterloo.ca/~bico/qsopt/). Further instructions on building/downloading those can be found below.

To build PyTSP, run

    pip install git+https://github.com/jvkersch/pytsp.git

If running `pip` fails with a message that Concorde or QSOpt cannot be found, set the environment variable `CONCORDE_DIR` (or `QSOPT_DIR`) to point to the folder where you installed Concorde (or QSOpt). This only needs to be done at build time: Concorde is distributed as a static library, so it will be pulled in to the Cython object file at link time.

What can I do with it?
-------

PyTSP is a very light-weight library. The main entry point is the `TSPSolver` class. Here we use it to read in the Berlin52 dataset, a dataset of 52 locations in Berlin (part of the TSPlib test data).

```python
    >>> from pytsp.tsp import TSPSolver
    >>> from pytsp.tests.data_utils import get_dataset_path
    >>> fname = get_dataset_path("berlin52")
    >>> solver = TSPSolver.from_tspfile(fname)
    Problem Name: berlin52
    Problem Type: TSP
    52 locations in Berlin (Groetschel)
    Number of Nodes: 52
    Rounded Euclidean Norm (CC_EUCLIDEAN)
```    

As you can see above, PyTSP (or rather, Concorde) is somewhat chatty and will print various message to the standard output. Now that we have a solver instance, let's compute a solution. On my machine this is almost instantaneous.
   
```python    
    >>> solution = solver.solve()
    (... output snipped for brevity ...)
```

Again, Concorde will display a variety of messages while it's running. The end result is a `ComputedTour` object called `solution` with information about the tour that we just computed:

```python
    
    >>> solution.found_tour
    True
    >>> solution.optimal_value
    7542.0
    >>> solution.tour
    array([ 0, 48, 31, 44, 18, 40,  7,  8,  9, 42, 32, 50, 10, 51, 13, 12, 46,
           25, 26, 27, 11, 24,  3,  5, 14,  4, 23, 47, 37, 36, 39, 38, 35, 34,
           33, 43, 45, 15, 28, 49, 19, 22, 29,  1,  6, 41, 20, 16,  2, 17, 30,
           21], dtype=int32)
    
```

How do I build Concorde/QSOpt?
-------

First, check if your platform provides packages for Concorde/QSOpt.

* **Linux/Mac OS**: You need to build Concorde from source, and download a packaged version of QSOpt. PyTSP comes with a [shell script](tools/build_concorde.sh) to build Concorde with the appropriate flags to automate this.

 **Note:** you must compile Concorde with position-independent symbols (the `-fPIC` flag in gcc) and download the PIC-enabled version of QSOpt.

* **Windows:** I haven't tried using PyTSP on Windows yet. If you get the library to work, please open a ticket to describe any tweaks.

License
-----

PyTSP is licensed under the [Modified BSD license](COPYING). Note that Concorde and QSOpt are released under different licenses, and that PyTSP does not include any code from these packages.
