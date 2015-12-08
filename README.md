# BitSniffer: A tool for linkability analysis

Team Members: Ryan Anderson, Luke Gessler, and Sam Prestwood

This is the code repository for our final project for [CS 4501: Crypto Currency Cabal](http://bitcoin-class.org/).

## Overview:

BitSniffer is a tool for quantifying the linkability of Bitcoin addresses. The tool can perform two types of operations:

1. When one address sends BTC to a second address via a mixing service, the tool searches the blockchain for a transaction path between the addresses and calculates the size of the anonymity set for the output address.

2. For two arbitrary addresses, the tool calculates a set of metrics for estimating the linkability between the two addresses.

## Dependencies:

- Python 3.x
- [Bottle](http://bottlepy.org/docs/dev/index.html)
- [Requests](http://docs.python-requests.org/en/latest/)

## How to run:

Clone this repository, then, in the root code directory, run:

    python3 webapp.py

This will launch a web interface that can be accessed in your browser at [http://localhost:8080](http://localhost:8080)

## Write-up:

For more information about the theoretical aspects of this project, consult our [write-up](https://github.com/mrranderson/BitSniffer/raw/master/writeup.pdf).

## License

This project is licensed under the [MIT license](https://opensource.org/licenses/MIT):

Copyright (c) 2015 Ryan Anderson, Luke Gessler, and Sam Prestwood

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

