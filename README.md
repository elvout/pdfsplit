# pdfsplit

This package splits a PDF file into multiple PDF files.
It allows the user to extract specific page ranges from
a PDF and provides a very basic output file formatter.

## Installation

```shell
$ git clone https://github.com/elvout/pdfsplit.git
$ cd pdfsplit
$ pip3 install [--user] [--upgrade] .
```

This should install `pdfsplit` into:

- `/usr/local/bin` if `--user` is not provided to `pip3`.
- `~/.local/bin` if `--user` is provided to `pip3` (Linux).
- `~/Library/Python/3.[x]/bin` if `--user` is provided to `pip3` (macOS).

## Usage

```shell
pdfsplit [-h] [-o offset] infile pagefile out_fmt
```

- `infile`: the filename of the PDF file to split.
- `pagefile`: a text file containing 1-indexed page ranges to extract.
- `out_fmt`: a Python f-string containing a formatting recipe
for the filenames of output PDF files. The f-string should use
an integer `_i` representing the line number of each interval
in `pagefile`.
  - **This executes arbitrary Python code.** Use with caution.
- `offset`: the number of leading pages in the `infile` PDF to skip.

See [sample/](sample/) for an example usage.

### Pagefile Format

Each line of the `pagefile` should contain one space-delimited page
number range. The ranges should be 1-indexed. Ranges are inclusive
of the starting number and exclusive of the ending number.

e.g.

```text
1 15
15 42
42 67
70 75
```

#### Lazy Intervals

If a line contains only the starting point of the range, the parser
will set the endpoint of the range to the starting point of the next
range if it exists.

The previous example is thus equivalent to:

```text
1
15
42 67
70 75
```

as well as

```text
1
15
42 67
70
75
```
