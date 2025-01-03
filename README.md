# Couple of Jacob comments
To run this on your machine (assuming linux ubuntu) it should be pretty simple as it only relies on the csv and math libraries in addition to the ones provided.
I was about to write a guide to setting up a venv and pip installing required modules, but then realized that obviously the ones I used (math, random, time, csv, unittest)
come standard with python! Should work using the "speedup" test below as well as using $python examples/simple_example.py or $python3 examples/simple_example.py.

Running inside of my vm (8192MB 3600MHz of memory 8 CPUs allocated on a 10850k @ 3.6GHz) i get a slow time of 0.84sec, new time of 0.01sec, and a speedup of 127.97x. 

Time complexity of original solution is O(mn) m being the number of queries and n being the number of points. My solution has a build time of O(nlogn) versus the originals O(1),
and a query time of O(m(logm)^2) for m queries.

Same space complexity for both: O(n).

References for time and space complexity:

https://johnlekberg.com/blog/2020-04-17-kd-tree.html

https://miro.medium.com/v2/resize:fit:1200/1*5ZLci3SuR0zM_QlZOADv8Q.jpeg gives a good representation of this but I am sure you are all familiar. 


# Developer Exercise

Please improve this stub project to calculate nearest neighbor values faster
than the naive example given in nearest_neighbor_index.py.

Nearest neighbor is a well studied problem and you should be able to find a
number of different approaches to solving this problem. We would like to see
approximately a 1.5x improvement in speed after you're done optimizing.

While in the "real world" we expect you will import scikit, numpy or similar to
index and query the data, we want to see how you code. So, please avoid using
any of these pre-canned solutions. That being said, be creative, there are many
ways to solve this problem.

The code here is for your convenience, but nothing here is sacred. Change the
interfaces, rename functions/files, link to code in another language, whatever.
Change as much or little as you like. That being said, your hypothetical end
user knowns Python so if your implementation is in COBOL, you should have a good
reason.

NOTE: Please read the Tasks section before _and after_ you are complete. It is
easy to forget some of the tasks.

# Getting Started

From Linux or anaconda, using Python 3.6 or higher, do this to run the existing
unit tests:

```
python -m pip install .
python -m unittest
```

This should create a result similar to:

```
$ python -m unittest
.slow time: 2.40sec
new time: 2.33sec
speedup: 1.03x
.
----------------------------------------------------------------------
Ran 2 tests in 4.741s

OK
```

Note that the exact times may be different on your computer, we're just worried
about the `speedup` value.

# Tasks

## Post your Code to GitHub

Create a fork of this repo and commit while you work. Please email us the URL
when you're done so we can see the final result as well as your commit history.

Please note the MIT license. This code is yours, show it to your Aunt Hilda, use 
it in another interview, whatever.

## Improve the Index Performance

Your goal is to get the `speedup` value to about 1.5 or higher.

## Impress Us with Code

In addition to getting a `speedup` over the existing implementation, we will be
looking for the following in your code:

* Code clarity and comments
* Code efficiency
* Test coverage
  - The existing test coverage is intentionally poor

## Provide References

If you use an algorithm from some blogger or Stack Overflow, include a link in
the comments along with why you chose it.

## Document for the End User

Your end user is a data scientist that would like to take advantage of this
nearest neighbor implementation. Please create an example in 
`examples/simple_example.py` that explains how to use the code and improve the
comments in `pynn/nearest_neighbor_index.py` as reference documentation.
