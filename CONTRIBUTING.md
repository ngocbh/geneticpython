# Contributing to GeneticPython
Thank you for your interest in contributing to GeneticPython! Before you begin writing code, it is important that you share your intention to contribute with the team, based on the type of contribution:

If you want to propose a new feature and implement it. You should post about your intended feature in an [issue](https://github.com/ngocjr7/geneticpython/issues), and we shall discuss the design and implementation. Once we agree that the plan looks good, go ahead and implement it.
      
Once you implement and test your feature or bug-fix, please submit a Pull Request to
https://github.com/ngocjr7/geneticpython.

## Developing GeneticPython

To develop GeneticPython in your machine:

1. you should remove existing versions first:

```sh
pip uninstall geneticpython
```

2. clone a copy of GeneticPython from source:

```sh
git clone https://github.com/ngocjr7/geneticpython/
cd geneticpython
```

3. install GeneticPython in `develop` mode:

```sh
python setup.py develop
```

This mode will symlink the Python files from the current local source tree into the Python install. Hence, if you modify a Python file, you do not need to reinstall GeneticPython again and again. This is especially useful if you are only changing Python files.

## Unit testing
All tests suites are located in the `tests` folder and start with `test_`. Run the entire test suite with

```sh
python tests/run_test.py
```

or run individual test suites using the command `python tests/FILENAME.py`, where FILENAME represents the file containing the test suite you wish to run.

Note that I still cannot develop all test suite so far, it would be great help if you can develop some unit tests coupled with your implementation.

## Developing new examples

The examples of this project are still sketchy, we hope to be able to apply this project to more problems. Any new examples would be welcome to add to our example set.

We are looking for implementation in different classic NP-hard problem such as TSP, Graph Coloring, ...

