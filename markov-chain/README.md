## Markov Chain - Poem Generation
## README

This program requires [abseil-cpp](https://github.com/abseil/abseil-cpp) to run.
Please install the Abseil C++ Common Libraries and update the `path` in the WORKSPACE file to the abseil-cpp directory.

### Components

The organization and descriptions of the project files are listed below:

- src/markov_main.cc: contains the starting code for poem generation using this Markov Chain implementation
- src/markov.h: contains the implementation of the encompassing class `Markov` that is used to traverse the chain
- src/state.h: contains the implementation of the subclass `State` that is used to manage nodes in the chain
- src/util.h: contains utility functions that read from file and generate random numbers
- data/\*.txt: contains text files from which poems can be made

### How to Run

To start poem generation, use the following command:

```
make markov-run
```
