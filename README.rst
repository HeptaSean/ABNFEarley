# ABNFEarley – An Earley parser for ABNF grammars in Python
_ABNFEarley_ is a parser for Augmented Backus-Naur Form (ABNF) grammars.
It uses an adaption of the techniques given in Jay Earley's 1970
paper “An Efficient Context-Free Parsing Algorithm”
[[doi:10.1145/362007.362035]](https://doi.org/10.1145/362007.362035).
It can handle ABNF grammars as specified in [RFC 5234
“Augmented BNF for Syntax Specifications:
ABNF”](https://www.rfc-editor.org/info/rfc5234) and updated in [RFC 7405
“Case-Sensitive String Support in
ABNF”](https://www.rfc-editor.org/info/rfc7405).

## TODO
- [ ] Document, test, and implement the model for grammars
- [ ] Document, test, and implement the model for parse results
- [ ] Document, test, and implement the parser itself
- [ ] Add folder with example ABNF files and use them on test inputs
- [ ] Write a script for executing an ABNF grammar file on an input file

## Installation
The `abnfearley` package is implemented in Python 3.
If it is not already present on your system, it can be installed by, e.g.,
`sudo apt install python3` on Ubuntu and other Debian-based distributions
or by `sudo pacman -S python` on Arch Linux.

- [ ] Upload to PyPI and give installation instructions with pip and
easy_install.

## Basic Usage
- [ ] Give example with small toy grammar (loaded from file) in an
interactive python session.
- [ ] Create a demonstration script, which gets an ABNF grammar file and a
target file and shows the resulting abstract syntax graph or gives
meaningful errors.

## Further Documentation
- [Development Environment](docs/development.md)
